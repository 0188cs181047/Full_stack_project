
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
from django.shortcuts import render, redirect,HttpResponse
from hiring.forms import ResourceForm,CompanyDataForm
#from hiring.forms import ResumeOwnershipForm ,Resume ,ResumeForm
from hiring.models import Recruiter
#from hiring.models import HR ,ResumeOwnership ,Phone,Candidate , Owner
from hiring.functions import handle_upload_file
from .filters import RecruiterFilter,UploadedFileFilter
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
import chardet
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import get_object_or_404
from .models import UploadedFile,Recruiter
from .forms import UploadFileForm
from django.contrib import messages
from django.urls import reverse
from django.db.models import Count
from django.db.models import F
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import EmailMessage
import mimetypes
from cridential.views import app_access_required , login_view
from django.db.models import Sum



@app_access_required('Hiring Management')
def home(request):
    total_resource_required = Recruiter.objects.aggregate(Sum('resourcerequired'))['resourcerequired__sum']
    total_resource_remaining = Recruiter.objects.aggregate(Sum('resourceremaining'))['resourceremaining__sum']
    context = {
        'page_title': 'Home',
        'total_resource_required': total_resource_required,
        'total_resource_remaining': total_resource_remaining,
    }
    return render(request, "hiring/home.html",context)

@app_access_required('Hiring Management')
def add_somthing(request ,pk):
    paginator = Paginator()
    page = paginator.get_page(pk)
    return render(request, "hiring/home.html",{"page":page} )

@app_access_required('Hiring Management')
def show(request):
    recruiter = Recruiter.objects.all()
    filters = RecruiterFilter(request.POST, queryset=recruiter)
    employees = filters.qs
    paginator = Paginator(employees, 10) # 10 employees per page
    page = request.GET.get('page')
    try:
        employees = paginator.page(page)
    except PageNotAnInteger:
        employees = paginator.page(1) # If page is not an integer, deliver first page.
    except EmptyPage:
        employees = paginator.page(paginator.num_pages)
    context = {'employees': employees, 'filters': filters,'page': page}
    return render(request, "hiring/show.html", context)




@login_required(login_url='/login/')
@app_access_required('Hiring Management')
def edit1(request, id):
    employee = Recruiter.objects.get(id=id)
    return render(request, "hiring/edit1.html", {'employee': employee})




@login_required(login_url='/login/')
@app_access_required('Hiring Management')
def update1(request, id):
    employee = Recruiter.objects.get(id = id)
    form = ResourceForm(instance=employee)
    if request.method == 'POST':
        form = ResourceForm(request.POST, instance= employee)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/hiring/show')    
    return render(request, "hiring/edit1.html", {'employee':employee ,"form":form})


@login_required(login_url='/login/')
@app_access_required('Hiring Management')
def delete1(request, id):
    employees = Recruiter.objects.get(id = id)
    employees.delete()
    return HttpResponseRedirect("/hiring/show")



@login_required(login_url='/login/')
@app_access_required('Hiring Management')
def recruiter(request):
    form1 = ResourceForm()
    if request.method == "POST":
        form1 = ResourceForm(request.POST)
        if form1.is_valid():
            try:
                form1.save()
                return HttpResponseRedirect("/hiring/show")
            except:
                pass
    else:
        form1 = ResourceForm()
    return render(request, "hiring/index1.html", {'form1':form1})



@login_required(login_url='/login/')
@app_access_required('Hiring Management')
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form data to the database
            job_id = form.cleaned_data['job_id']
            file = form.cleaned_data['file']
            candidate_name = form.cleaned_data['candidate_name']
            contact = form.cleaned_data['contact']
            experience = form.cleaned_data['experience']
            owner_name = form.cleaned_data['owner_name']
            l1 = form.cleaned_data['l1']
            l2 = form.cleaned_data['l2']
            l3 = form.cleaned_data['l3']
            status = form.cleaned_data['status']

            uploaded_file = UploadedFile.objects.create(
                job_id=job_id,
                file=file,
                candidate_name=candidate_name,
                contact=contact,
                experience=experience,
                owner_name=owner_name,
                l1=l1,
                l2=l2,
                l3=l3,
                status=status
            )

            url = reverse('job_file_counts')
            url += f'?job_id={job_id.id}'
            return redirect(url)
    else:
        form = UploadFileForm()
    return render(request, 'hiring/resource_upload.html', {'form': form})


@app_access_required('Hiring Management')
def view_files(request, job_id):
    files = UploadedFile.objects.filter(job_id=job_id)
    file_filter = UploadedFileFilter(request.POST, queryset=files)
    files = file_filter.qs
    return render(request, 'hiring/resource_list.html', {'files': files,'file_filter': file_filter})


@login_required(login_url='/login/')
@app_access_required('Hiring Management')
def edit_file(request, file_id):
    file = get_object_or_404(UploadedFile, pk=file_id)

    if request.method == 'POST':
        form = UploadFileForm(request.POST, instance=file)
        if form.is_valid():
            form.save()
            return redirect(reverse('resource_list', args=[file.job_id.id]))
    else:
        form = UploadFileForm(instance=file)  # Pass file instance to the context
    return render(request, 'hiring/edit_file.html',{"form":form ,'file':file})



@login_required(login_url='/login/')
@app_access_required('Hiring Management')
def delete_file(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id)
    if request.method == 'POST':
        file.delete()
        return HttpResponseRedirect('/hiring/job/file_counts')
    return render(request, 'hiring/delete_file.html', {'file': file})


@app_access_required('Hiring Management')
def detail_hr(request, id):
    recruiter = get_object_or_404(Recruiter, id=id)

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            job_id = form.cleaned_data['job_id']
            if Recruiter.objects.filter(id=job_id).exists():
                candidate_name = form.cleaned_data['candidate_name']
                contact = form.cleaned_data['contact']
                owner_name = form.cleaned_data['owner_name']
                l1 = form.cleaned_data['l1']
                l2 = form.cleaned_data['l2']
                l3 = form.cleaned_data['l3']
                status = form.cleaned_data['status']
                uploaded_file = form.save(commit=False)
                uploaded_file.job_id = Recruiter.objects.get(id=job_id)
                uploaded_file.save()

                return HttpResponseRedirect(reverse("detail_hr", kwargs={"id": recruiter.id}))
            else:
                form.add_error('job_id', 'Invalid Job ID.')
    else:
        form = UploadFileForm()

    uploaded_files = UploadedFile.objects.filter(job_id=id)
    uploaded_file_data = {}
    for uploaded_file in uploaded_files:
        uploaded_file_data[uploaded_file.id] = {
            'candidate_name': uploaded_file.candidate_name,
            'contact': uploaded_file.contact,
            'owner_name': uploaded_file.owner_name,
            'l1': uploaded_file.l1,
            'l2': uploaded_file.l2,
            'l3': uploaded_file.l3,
            'status': uploaded_file.status,
        }

    return render(request, "hiring/detail_hr.html", {'recruiter': recruiter ,'form':form ,'uploaded_files': uploaded_files,'uploaded_file_data': uploaded_file_data})



@app_access_required('Hiring Management')
def job_file_counts(request, job_id=None):
    if job_id is None:
        job_file_counts = UploadedFile.objects.values('job_id__job_id', 'job_id__id').annotate(count=Count('id'))
    else:
        job_file_counts = UploadedFile.objects.filter(job_id=job_id).values('job_id__job_id', 'job_id__id').annotate(count=Count('id'))
    # Paginate the results
    paginator = Paginator(job_file_counts, 10) # 10 job_file_counts per page
    page_number = request.GET.get('page')
    try:
        job_file_counts = paginator.page(page_number)
    except PageNotAnInteger:
        job_file_counts = paginator.page(1) # If page is not an integer, deliver first page.
    except EmptyPage:
        job_file_counts = paginator.page(paginator.num_pages)
    context = {
        'job_file_counts': job_file_counts,
    }
    return render(request, 'hiring/job_file_counts.html', context)




@login_required(login_url='/login/')
@app_access_required('Hiring Management')
def share_files(request):
    if request.method == 'POST':
        selected_files = request.POST.getlist('selected_files') # get the list of selected file IDs
        if selected_files:
            email = request.POST.get('email') # get the email address to send the files to
            uploaded_files = UploadedFile.objects.filter(id__in=selected_files) # get the selected files from the database
            if uploaded_files:
                subject = "Actevia Technology Service pvt ltd "
                body = "Candidata resume file "
                from_email = "acteviashiv@gmail.com" # replace with your own email address
                to_email = [email]
                email_message = EmailMessage(subject, body, from_email, to_email)
                for file in uploaded_files:
                    content_type, encoding = mimetypes.guess_type(file.file.name)
                    email_message.attach(file.file.name, file.file.read(), content_type) # attach each file to the email message
                email_message.send()
                return render(request, 'hiring/share_files.html', {'success_popup': True}) # show success popup
            else:
                return render(request, 'hiring/share_files.html', {'error_popup': True}) # show error popup
        else:
            return render(request, 'hiring/share_files.html', {'error_popup': True}) # show error popup
    else:
        return render(request, 'hiring/share_files.html')



def company_data(request):
    form = CompanyDataForm(request.POST or None)
    if form.is_valid():
        form.save()  # Save the form data to the database
        form = CompanyDataForm()  # Create a new form for the next entry

    context = {'form': form}
    return render(request, 'hiring/company_data.html', context)

