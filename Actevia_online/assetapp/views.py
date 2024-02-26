from django.shortcuts import redirect, get_object_or_404,render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.models import User
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from qrcode import *
import qrcode
from io import BytesIO
import openpyxl
from django.contrib.auth import logout

from .models import Asset_inform,asset_Notification
from .forms import AssetInformForm, AssetFilterForm,UpdateAssetForm
from django.contrib import messages
from cridential.views import login_view , app_access_required
from cridential.models import CustomUser
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from urllib.parse import urlencode
from django.contrib.auth import get_user_model


@login_required
@app_access_required('Asset Management')
def before_login(request):
    user = request.user  # Assuming you have authentication enabled
    user_email = user.email  # Assuming the email field exists in your user model
    if user.is_superuser:
        total_assets_in_use = Asset_inform.objects.filter(asset_status='IN-USE').count()
        total_assets_in_buffer = Asset_inform.objects.filter(asset_status='BUFFER').count()
    else:
        total_assets_in_use = Asset_inform.objects.filter(asset_status='IN-USE', email=user_email).count()
        total_assets_in_buffer = Asset_inform.objects.filter(asset_status='BUFFER', email=user_email).count()
    context = {
        'page_title':'Home',
        'total_assets_in_use': total_assets_in_use,
        'total_assets_in_buffer': total_assets_in_buffer,
    }
    return render(request, "fixed/home.html",context)


@app_access_required('Asset Management')
@login_required
def Asset_detail(request):
    # Fetching the logged-in user's email
    user_email = request.user.email
    
    # Retrieving assets for the logged-in user or staff
    if request.user.is_staff:
        asset_data = Asset_inform.objects.all()
    else:
        asset_data = Asset_inform.objects.filter(email=user_email)
    
    if request.method == 'POST':
        form = AssetFilterForm(request.POST)
        if form.is_valid():
            asset_data = form.filter_queryset(asset_data)
    else:
        form = AssetFilterForm()
    
    if request.method == 'POST':
        if 'delete_selected' in request.POST:
            # Delete selected assets
            selected_assets = request.POST.getlist('selected_assets[]')
            Asset_inform.objects.filter(pk__in=selected_assets).delete()
            return redirect("/asset/new_asset_detail")
        
        elif 'update_selected' in request.POST:
            # Update a single selected asset
            selected_assets = request.POST.getlist('selected_assets[]')
            if len(selected_assets) == 0:
                messages.error(request, 'No assets selected to update.')
            elif len(selected_assets) > 1:
                messages.error(request, 'Please select only one asset to update.')
            else:
                return redirect(f"/asset/update_asset/{selected_assets[0]}/")
        
        elif 'generate_qr' in request.POST:
            selected_assets = request.POST.getlist('selected_assets[]')
            if len(selected_assets) == 0:
                messages.error(request, 'No assets selected to generate QR code.')
            elif len(selected_assets) > 1:
                messages.error(request, 'Please select only one asset to generate QR code.')
            else:
                asset = Asset_inform.objects.get(pk=selected_assets[0])
                qr_data = f"Asset ID: {asset.asset_id}"
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr.add_data(qr_data)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                response = HttpResponse(content_type="image/png")
                img.save(response, "PNG")
                return response
        
    return render(request, "fixed/see_both_detail.html", {"asset": asset_data, "form": form})


@login_required(login_url='/login/')
@app_access_required('Asset Management')
def create_asset(request):
    form = AssetInformForm()

    if request.method == 'POST':
        form = AssetInformForm(request.POST, request.FILES)
        if form.is_valid():
            asset = form.save(commit=False)
            asset.Asset_date = form.cleaned_data['Asset_date']
            asset.save()
            return HttpResponseRedirect("/asset/new_asset_detail")
    else:
        form = AssetInformForm()

    return render(request, 'fixed/create_asset.html', {'form': form})



@login_required(login_url='/login/')
@app_access_required('Asset Management')
def Updata_asset(request, pk):
    asset = get_object_or_404(Asset_inform, pk=pk)
    form = UpdateAssetForm(instance=asset)
    if request.method == 'POST':
        form = UpdateAssetForm(request.POST, request.FILES, instance=asset)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/asset/new_asset_detail")
    else:
        form = UpdateAssetForm(instance=asset)
    return render(request, 'fixed/updata_asset.html', {'asset': asset, 'form': form})



@login_required(login_url='/login/')
@app_access_required('Asset Management')
def Delete_asset(request, pk):
    asset = get_object_or_404(Asset_inform, id=pk)
    asset.delete()
    return HttpResponseRedirect("/asset/new_asset_detail")


@app_access_required('Asset Management')
def asset_list(request):
    form = AssetFilterForm(request.GET or None)
    results = form.filter_data() if form.is_valid() else Asset_inform.objects.all()
    context = {'form': form, 'results': results}

    return render(request, 'fixed/sset_list.html', {'form': form, 'asset': results})



@login_required(login_url='/login/')
@app_access_required('Asset Management')
def qr_code_asset(request, pk):
    my_model = get_object_or_404(Asset_inform, pk=pk)
    data = f"Asset ID : {my_model.asset_id} "
    img = qrcode.make(data, box_size=10, border=4)
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response




@app_access_required('Asset Management')
def view_asset(request, pk):
    asset = get_object_or_404(Asset_inform, pk=pk)
    return render(request, 'asset_detail.html', {'asset': asset})

from django.utils import timezone
@login_required(login_url='/login/')
@app_access_required('Asset Management')
def export_assets_to_excel(request):
    # Get the assets from the database
    assets = Asset_inform.objects.all()
    # Create a new Excel workbook
    wb = openpyxl.Workbook()
    # Select the active worksheet
    ws = wb.active
    # Write the header row
    ws.append(['Asset Id', 'Asset Owner', 'Asset Type', 'Asset Status', 'Asset Date'])
    # Write the data rows
    for asset in assets:
        asset_date = asset.Asset_date.astimezone(timezone.utc).replace(tzinfo=None) if asset.Asset_date else None
        formatted_date = asset_date.strftime("%B %d, %Y") if asset_date else None
        # Convert the formatted date to a string
        ws.append([asset.asset_id, asset.asset_owner, asset.asset_type, asset.asset_status, formatted_date])
    # Create a response object with the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=assets.xlsx'
    # Save the workbook to the response
    wb.save(response)
    return response


@app_access_required('Asset Management')
def admin_logout(request):
    logout(request)
    return HttpResponseRedirect("/")

@app_access_required('Asset Management')
def send_approval_request_email(request):
    if request.method == 'POST':
        selected_assets = request.POST.getlist('selected_assets')
        approval_email = request.POST.get('approval_email')

        if not selected_assets:
            messages.error(request, 'No Asset selected.')
            return redirect('/asset/asset_detail/')

        # Check if the approval email is registered in CustomUser
        user = CustomUser.objects.filter(email=approval_email).first()
        if not user:
            messages.error(request, 'The provided email is not registered.')
            return redirect('/asset/asset_detail/')

        # Process the selected policies
        policy_data = []
        for Asset_inform_id in selected_assets:
            policy = Asset_inform.objects.filter(pk=Asset_inform_id).first()

            if policy:
                if policy.approved:
                    policy.approved=False
                policy.request_approval()

                # Save additional data in the policy or user object if needed
                asset_informs = Asset_inform.objects.filter(pk__in=selected_assets)
                # file_names = [upload for upload in Asset_inform.asset_id]
                file_names = [asset.asset_id for asset in asset_informs]
                policy.additional_data = ', '.join(file_names)
                policy.save()

                # Create a notification for the user and policy
                notification = asset_Notification(user=user, Asset_inform=policy)
                notification.save()

                # Add policy data to the list
                policy_data.append({
                    'policy_name': policy.asset_id,
                    'email': policy.email,
                    'username': user.get_username(),
                    'file_names': policy.asset_owner,
                })

        # Send email notification to the approval email address
        message = """Hello,<br>
                    you have received the request to accept the asset.<br><br>
                     Please review the following details in the application which is received from 
                     Username: {username}<br><br>
                     regards,<br>
                    Asset Management System
                     """.format(username=user.get_username())
                    
        html_message = message
        plain_message = message
        send_mail(
            'Asset Approval Request',
            plain_message,
            'acteviashiv@gmail.com',
            [approval_email],
            html_message=html_message,
        )

        # Send email notification to the sender
        sender_message = """Hello,<br>
                           The recipient has received the asset approval request.<br>
                           Please wait for their response.<br><br>
                           Regards,<br>
                           Asset Management System
                        """
        sender_html_message = sender_message
        sender_plain_message = sender_message
        sender_email = 'acteviashiv@gmail.com'  # Replace with the actual sender's email address
        send_mail(
            'Asset Approval Request Sent',
            sender_plain_message,
            sender_email,
            [request.user.email],  # Assuming the sender's email is stored in the user object
            html_message=sender_html_message,
        )

        # Prepare query parameters for the redirect URL
        query_params = {'policy_id': selected_assets, 'username': user.get_username()}
        redirect_url = reverse('show_approval_notification') + '?' + urlencode(query_params)

        messages.success(request, 'Approval request sent successfully.')
        return redirect(redirect_url)

    else:
        messages.error(request, 'Invalid request method.')
        return redirect('/asset/asset_detail/')


@app_access_required('Asset Management')
def show_approval_notification(request):
    notifications = asset_Notification.objects.filter(user=request.user)
    filtered_notifications=[]
    for notification in notifications:
        policy = notification.Asset_inform
        if policy.requested_approval and not policy.approved:
            filtered_notifications.append(notification)
    return render(request, 'fixed/approval_notification.html', {'notifications': filtered_notifications})


@app_access_required('Asset Management')
def accept_approval(request, Asset_inform_id, user_id):
    policy = get_object_or_404(Asset_inform, pk=Asset_inform_id)
    sender_user = get_object_or_404(CustomUser, pk=user_id)
    sender_email = policy.email
    
    if policy.requested_approval and not policy.approved:
        # Save the policy data for the receiver user who accepted the approval
        receiver_user = request.user
        receiver_user.Asset_inform.add(policy)
        receiver_user.save()
                
        # Delete the policy from the sender user
        sender_user.Asset_inform.remove(policy)
        sender_user.save()
                
        # Update policy email and save
        policy.email = receiver_user.email
        policy.asset_owner = receiver_user.username
        policy.save()
                
        # Approve the policy and send email notification
        policy.approve_approval(receiver_user.email)

        notification = asset_Notification.objects.filter(user=request.user,Asset_inform=policy).first()
        if notification:
            notification.delete()

        #send email notification to sender 
        subject = "File Approval Notification"
        message = f"Your Request '{policy.asset_id}' has been approved by {receiver_user.username}."
        send_mail(
            subject,
            message,
            sender_user.email,  # Use the sender's email address
            [sender_email],  # Send the email to the sender's email address
        )

        return HttpResponse('Approval granted!')        
    return HttpResponse('Invalid request.')


@app_access_required('Asset Management')
def reject_approval(request, Asset_inform_id, user_id):
    policy = get_object_or_404(Asset_inform, pk=Asset_inform_id)
    sender_user = get_object_or_404(CustomUser, pk=user_id)
    sender_email = policy.email
    
    if policy.requested_approval and not policy.approved:
        policy.reject_approval()
        policy.save()

        notification = asset_Notification.objects.filter(user=request.user, Asset_inform=policy).first()
        if notification:
            notification.delete()

        # Send notification email to the sender
        subject = 'File Rejection Notification'
        message = f"Your file '{policy.asset_id}' has been rejected by {request.user.username}."
        send_mail(
            subject,
            message,
            sender_user.email,  # Use the sender's email address
            [sender_email],  # Send the email to the sender's email address
        )

        return HttpResponse('Approval rejected!')        
    return HttpResponse('Invalid request.')


@app_access_required('Asset Management')
@login_required
def New_Asset_detail(request):
    # Fetching the logged-in user's email
    user_email = request.user.email
    
    # Retrieving assets for the logged-in user or staff
    if request.user.is_staff:
        asset_data = Asset_inform.objects.all()
    else:
        asset_data = Asset_inform.objects.filter(email=user_email)
    
    if request.method == 'POST':
        form = AssetFilterForm(request.POST)
        if form.is_valid():
            asset_data = form.filter_queryset(asset_data)
    else:
        form = AssetFilterForm()
    
    if request.method == 'POST':
        if 'delete_selected' in request.POST:
            # Delete selected assets
            selected_assets = request.POST.getlist('selected_assets[]')
            Asset_inform.objects.filter(pk__in=selected_assets).delete()
            return redirect("/asset/new_asset_detail")
        
        elif 'update_selected' in request.POST:
            # Update a single selected asset
            selected_assets = request.POST.getlist('selected_assets[]')
            if len(selected_assets) == 0:
                messages.error(request, 'No assets selected to update.')
            elif len(selected_assets) > 1:
                messages.error(request, 'Please select only one asset to update.')
            else:
                return redirect(f"/asset/update_asset/{selected_assets[0]}/")
        
        elif 'generate_qr' in request.POST:
            selected_assets = request.POST.getlist('selected_assets[]')
            if len(selected_assets) == 0:
                messages.error(request, 'No assets selected to generate QR code.')
            elif len(selected_assets) > 1:
                messages.error(request, 'Please select only one asset to generate QR code.')
            else:
                asset = Asset_inform.objects.get(pk=selected_assets[0])
                qr_data = f"Asset ID: {asset.asset_id}"
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr.add_data(qr_data)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                response = HttpResponse(content_type="image/png")
                img.save(response, "PNG")
                return response
        
    return render(request, "fixed/new_see_both_detail.html", {"asset": asset_data, "form": form})
    