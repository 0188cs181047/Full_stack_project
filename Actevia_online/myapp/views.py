from django.http import JsonResponse
from django.shortcuts import render,HttpResponse,get_object_or_404

# Create your views here.
from django.shortcuts import render, redirect ,HttpResponseRedirect
from .models import Policy,Upload
from .forms import PolicyForm
from django.urls import reverse
from django.contrib import messages
from cridential.views import login_view , app_access_required
from django.contrib.auth.decorators import login_required
from cridential.models import CustomUser
from django.db.models import Q



@app_access_required('Organization Policy')
def home(request):
    registered_user_count = CustomUser.objects.exclude(
        Q(student_profile__isnull=False) | Q(teacher_profile__isnull=False)
    ).count()
    
    # Get the count of policies
    policy_count = Policy.objects.count()
    
    context = {
        'user_count': registered_user_count,
        'policy_count': policy_count
    }
    return render(request, 'policy/home.html', context)


@app_access_required('Organization Policy')
def policy_list(request):
    policies = Policy.objects.all()
    return render(request, 'policy/policy_list.html', {'policies': policies})


@login_required(login_url='/login/')
@app_access_required('Organization Policy')
def policy_list2(request):
    policies = Policy.objects.all()
    return render(request, 'policy/policy_list2.html', {'policies': policies})



@app_access_required('Organization Policy')
def policy_files(request, pk):
    policy = get_object_or_404(Policy, pk=pk)
    uploads = policy.upload_files.all()
    return render(request, 'policy/policy_files.html', {'policy': policy, 'uploads': uploads})


@login_required(login_url='/login/')
@app_access_required('Organization Policy')
def delete_file(request, policy_pk, upload_pk):
    upload = get_object_or_404(Upload, pk=upload_pk)
    policy = get_object_or_404(Policy, pk=policy_pk)
    
    # Delete file from the storage
    upload.file.delete()

    # Remove the upload file from the policy's list of uploads
    policy.upload_files.remove(upload)

    # Delete the FileUpload object from the database
    upload.delete()

    # Redirect back to the policy page
    return redirect('policy_files', pk=policy.pk)



@login_required(login_url='/login/')
@app_access_required('Organization Policy')
def policy_new(request):
    if request.method == "POST":
        form = PolicyForm(request.POST, request.FILES)
        if form.is_valid():
            policy = form.save(commit=False)
            policy.save()
            for f in request.FILES.getlist('upload_files'):
                policy.upload_files.create(file=f)
            return HttpResponseRedirect("/policy/policy_list")
    else:
        form = PolicyForm()
    return render(request, 'policy/policy_new.html', {'form': form})


@login_required(login_url='/login/')
@app_access_required('Organization Policy')
def policy_edit(request, pk):
    policy = Policy.objects.get(pk=pk)
    if request.method == "POST":
        form = PolicyForm(request.POST, request.FILES, instance=policy)
        if form.is_valid():
            policy = form.save(commit=False)
            policy.save()
            return redirect('policy_list')
    else:
        form = PolicyForm(instance=policy)
    return render(request, 'policy/policy_edit.html', {'form': form})


@login_required(login_url='/login/')
@app_access_required('Organization Policy')
def policy_delete(request):
    if request.method == 'POST':
        selected_policies = request.POST.getlist('selected_policies')
        if not selected_policies:
            messages.error(request, 'No policies selected for deletion.')
        else:
            Policy.objects.filter(pk__in=selected_policies).delete()
            messages.success(request, 'Selected policies deleted successfully.')
    return HttpResponseRedirect("/policy/policy_list")



