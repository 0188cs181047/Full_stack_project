from django import forms
from hiring.models import Recruiter,UploadedFile, onboarding_status,CompanyData
from django.forms import TextInput

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Recruiter
        fields = "__all__"
        labels = {
            "companyname": "Company Name",
            "Position": "Position",
            "resourcerequired": "Resource Required",
            "jd": "Job Description",
            "resourceremaining": "Resource Remaining",
            "r_status": "Resource Status",
            "Priority" : "Priority",
        }
        widgets = {
            "companyname": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter company name"}),
            "Position": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter position"}),
            "resourcerequired": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter resource required"}),
            "jd": forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter job description"}),
            "resourceremaining": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter resource remaining"}),
            "r_status": forms.Select(attrs={"class": "form-control"}),
            "Priority": forms.Select(attrs={"class": "form-control"}),
        }
        


class UploadFileForm(forms.ModelForm):
    status = forms.ChoiceField(choices=onboarding_status, initial="OnHold", label="Status",
                               widget=forms.Select(attrs={'class': 'form-select'}))
    job_id = forms.ModelChoiceField(queryset=Recruiter.objects.all(), label="Job ID",
                                    widget=forms.Select(attrs={'class': 'form-select'}))
    file = forms.FileField(label="File", widget=forms.FileInput(attrs={'class': 'form-control'}))
    candidate_name = forms.CharField(max_length=30, label="Candidate Name",
                                      widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter candidate name'}))
    contact = forms.CharField(max_length=20, label="Contact",
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter contact'}))
    experience = forms.CharField(max_length=4, label="Experience",
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter experience'}))
    owner_name = forms.CharField(max_length=30, label="Owner Name",
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter owner name'}))
    l1 = forms.CharField(max_length=30, label="L1",
                         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter L1'}))
    l2 = forms.CharField(max_length=30, label="L2",
                         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter L2'}))
    l3 = forms.CharField(max_length=30, label="L3",
                         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter L3'}))

    class Meta:
        model = UploadedFile
        fields = ['job_id', 'file', 'candidate_name', 'contact', 'experience', 'owner_name', 'l1', 'l2', 'l3', 'status']


class CompanyDataForm(forms.ModelForm):
    class Meta:
        model = CompanyData
        fields = ['company', 'experience', 'band', 'ctc']

    


