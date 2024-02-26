from django import forms
from .models import Policy,Upload

class PolicyForm(forms.ModelForm):
    upload_files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    policy_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter policy name'}))

    class Meta:
        model = Policy
        fields = ('policy_name', 'upload_files')
