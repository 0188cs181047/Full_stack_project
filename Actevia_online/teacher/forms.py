from django import forms
from onlinexam.models import Course
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from .models import Teacher
from cridential.models import CustomUser,TeacherUser

class TeacherUserForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter a password',
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password',
        })
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'email']
        labels = {
            'username': 'Username',
            'password1': 'Password',
            'password2': 'Confirm Password',
            'email': 'Email',
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a username',
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email',
            }),
        }

class TeacherForm(forms.ModelForm):
    user_form = TeacherUserForm

    class Meta:
        model = TeacherUser
        fields = ['address', 'mobile']
        labels = {
            'address': 'Address',
            'mobile': 'Mobile',
        }
        widgets = {
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your address',
            }),
            'mobile': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your mobile number',
            }),
           
        }



class UploadForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all())
    file = forms.FileField()
    def clean_file(self):
        file = self.cleaned_data['file']
        if file.content_type not in ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
            raise forms.ValidationError('Invalid file format. Only Excel files are allowed.')
        return file