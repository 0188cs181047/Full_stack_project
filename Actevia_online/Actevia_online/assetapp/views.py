
from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
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

from .models import Asset_inform
from .forms import AssetInformForm, AssetFilterForm
from django.contrib import messages

def before_login(request):
    return render(request, "fixed/home.html")

def Asset_detail(request):
    asset_data = Asset_inform.objects.all()
    if request.method == 'POST':
        form = AssetFilterForm(request.POST)
        if form.is_valid():
            asset_id = form.cleaned_data.get('asset_id')
            asset_owner = form.cleaned_data.get('asset_owner')
            asset_type = form.cleaned_data.get('asset_type')
            asset_status = form.cleaned_data.get('asset_status')
            asset_data = asset_data.filter(
                Q(asset_id__icontains=asset_id) &
                Q(asset_owner__icontains=asset_owner) &
                Q(asset_type__icontains=asset_type) &
                Q(asset_status__icontains=asset_status)
            )
    else:
        form = AssetFilterForm()

    if request.method == 'POST':
        if 'delete_selected' in request.POST:
            selected_assets = request.POST.getlist('selected_assets[]')
            Asset_inform.objects.filter(pk__in=selected_assets).delete()
            return redirect('asset_detail')

        elif 'update_selected' in request.POST:
            selected_assets = request.POST.getlist('selected_assets[]')
            if len(selected_assets) == 0:
                messages.error(request, 'No assets selected to update.')
            elif len(selected_assets) > 1:
                messages.error(request, 'Please select only one asset to update.')
            else:
                return redirect('update_asset', pk=selected_assets[0])

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


def create_asset(request):
    form = AssetInformForm()
    if request.method == 'POST':
        form = AssetInformForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('asset_detail')
    else:
        form = AssetInformForm()
    return render(request, 'fixed/create_asset.html', {'form': form})


def Updata_asset(request, pk):
    asset = get_object_or_404(Asset_inform, pk=pk)
    form = AssetInformForm(instance=asset)
    if request.method == 'POST':
        form = AssetInformForm(request.POST, request.FILES, instance=asset)
        if form.is_valid():
            form.save()
            return redirect('asset_detail',)
    else:
        form = AssetInformForm(instance=asset)
    return render(request, 'fixed/updata_asset.html', {'asset': asset, 'form': form})


def Delete_asset(request, pk):
    asset = get_object_or_404(Asset_inform, id=pk)
    asset.delete()
    return redirect('asset_detail')


def asset_list(request):
    form = AssetFilterForm(request.GET or None)
    results = form.filter_data() if form.is_valid() else Asset_inform.objects.all()
    context = {'form': form, 'results': results}

    return render(request, 'fixed/sset_list.html', {'form': form, 'asset': results})


def qr_code_asset(request, pk):
    my_model = get_object_or_404(Asset_inform, pk=pk)
    data = f"Asset ID : {my_model.asset_id} "
    img = qrcode.make(data, box_size=10, border=4)
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response


def view_asset(request, pk):
    asset = get_object_or_404(Asset_inform, pk=pk)
    return render(request, 'asset_detail.html', {'asset': asset})

def export_assets_to_excel(request):
    # Get the assets from the database
    assets = Asset_inform.objects.all()
    # Create a new Excel workbook
    wb = openpyxl.Workbook()
    # Select the active worksheet
    ws = wb.active
    # Write the header row
    ws.append(['Asset Id', 'Asset Photo', 'Asset Owner', 'Asset Type', 'Asset Status'])
    # Write the data rows
    for asset in assets:
        ws.append([asset.asset_id, asset.asset_photo.url, asset.asset_owner, asset.asset_type, asset.asset_status])
    # Create a response object with the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=assets.xlsx'
    # Save the workbook to the response
    wb.save(response)

    return response

def admin_logout(request):
    logout(request)
    return HttpResponseRedirect("/")