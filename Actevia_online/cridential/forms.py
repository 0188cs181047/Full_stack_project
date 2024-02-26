from django import forms
from .models import CustomUser ,AppName
import random
import string
from django.contrib.auth.forms import SetPasswordForm





class CustomUserForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'is_active', 'is_staff')
        labels = {
            'username': 'Username',
            'email': 'Email',
            'password1': 'Password',
            'password2': 'Confirm Password',
            'is_active': 'Active',
            'is_staff': 'Staff',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    





class AutoGeneratePasswordForm(forms.ModelForm):
    generate_password = forms.CharField(
        label='Generate Password',
        widget=forms.Select(choices=(('auto', 'Automatic'), ('manual', 'Manual'))),
    )

    app_name = forms.ModelMultipleChoiceField(
        queryset=AppName.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Enter app name'}),
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'is_active', 'is_staff', 'app_name')
        labels = {
            'username': 'Username',
            'email': 'Email',
            'is_active': 'Active',
            'is_staff': 'Staff',
            'app_name': 'App Name',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def generate_random_password(self):
        # Generate a random password using a combination of letters and digits
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))

    def save(self, commit=True, app_name=None):
        user = super().save(commit=False)
        user.is_active = self.cleaned_data['is_active']
        user.is_staff = self.cleaned_data['is_staff']
        if app_name is not None:
            user.app_name.set(app_name) # set app_name if passed
        user.set_password(self.generate_random_password())
        if commit:
            user.save()
        return user


    

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email','is_staff', 'is_active', 'app_name']
        labels = {
            'username': 'Username',
            'email': 'Email',
            'is_staff': 'User',
            'is_active': 'Active',
            'app_name': 'App Name',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input' ,'style': 'margin-left: 20px;'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input' ,'style': 'margin-left: 10px;'}),
            'app_name': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Enter app name'}),
        }

        

class CustomPasswordResetForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Retrieve the user argument from kwargs
        super().__init__(user, *args, **kwargs)
        # Customize form fields if needed

    def save(self, commit=True):
        user = super().save(commit=False)
        user.otp_secret_key = None  # Reset the OTP secret key
        if commit:
            user.save()
        return user