from django import forms
from django import forms
from django.contrib.auth.forms import UserCreationForm
from cridential.models import CustomUser, StudentUser

class StudentUserForm(UserCreationForm):
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


class StudentForm(forms.ModelForm):
    user_form = StudentUserForm()

    class Meta:
        model = StudentUser
        fields = ['address', 'mobile', 'is_eligible']
        labels = {
            'address': 'Address',
            'mobile': 'Mobile',
            'is_eligible': 'Is Eligible',
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
            'is_eligible': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'margin-left: 10px;',
            }),
        }
