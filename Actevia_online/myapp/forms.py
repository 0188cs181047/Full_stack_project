from django import forms
from .models import Policy,Upload
from multiupload.fields import MultiFileField


class PolicyForm(forms.ModelForm):
    upload_files = MultiFileField(min_num=1, max_num=20, max_file_size=1024*1024*5)
    policy_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter policy name'}))

    class Meta:
        model = Policy
        fields = ('policy_name', 'upload_files')
