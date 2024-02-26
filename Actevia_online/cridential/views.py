from django.http import JsonResponse
from django.shortcuts import render,HttpResponse,get_object_or_404

# Create your views here.
from django.shortcuts import render, redirect ,HttpResponseRedirect
from .models import CustomUser,AppName
from .forms import CustomUserForm ,AutoGeneratePasswordForm ,CustomPasswordResetForm ,UpdateUserForm
from django.urls import reverse
from django.contrib import messages
import random
import string
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.contrib.auth import logout
from django.contrib.auth.tokens import default_token_generator
from django_otp.oath import totp
from django.contrib.auth.views import PasswordResetConfirmView
from django.utils.http import urlencode


from django.contrib.auth.models import User
from django.urls import reverse_lazy

from django.contrib.auth import get_user_model


from django.contrib.auth import get_user_model, views as auth_views
from myapp.models import Policy




from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.exceptions import PermissionDenied
from functools import wraps




def app_access_required(app_name):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if AppName.objects.filter(customuser=request.user, name=app_name).exists():
                return view_func(request, *args, **kwargs)
            else:
                error_message = 'You are not authorized to access this app'
                messages.error(request, error_message)
                raise PermissionDenied('You are not authorized to access this app')
        return wrapper
    return decorator



from django.db.models import Q

def home(request):
    try:
        # Get the STUDENT and TEACHER groups
        student_group = Group.objects.get(name='STUDENT')
        teacher_group = Group.objects.get(name='TEACHER')
    except ObjectDoesNotExist:
        student_group = None
        teacher_group = None

    # Exclude student and teacher users from the query
    registered_user_count = CustomUser.objects.exclude(
        Q(student_profile__isnull=False, groups=student_group) |
        Q(teacher_profile__isnull=False, groups=teacher_group)
    ).count()
    
    # Get the count of policies
    policy_count = Policy.objects.count()
    
    context = {
        'user_count': registered_user_count,
        'policy_count': policy_count
    }
    return render(request, 'policy/home.html', context)




def generate_random_password():
    # Generate a random password using a combination of letters and digits
    random_password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
    return random_password








# def register_user(request):
#     if request.method == 'POST':
#         generate_password = request.POST.get('generate_password')

#         if generate_password == 'auto':
#             form = AutoGeneratePasswordForm(request.POST)
#         else:
#             form = CustomUserForm(request.POST)

#         if form.is_valid():
#             user = form.save(commit=False)

#             if generate_password == 'auto':
#                 # Generate a random password
#                 password = _generate_random_password()
#                 user.set_password(password)
#             else:
#                 password = form.cleaned_data.get('password1')
#                 user.set_password(password)

#             user.save()

#             # Company name and employee name
#             company_name =  'Actevia Technology Servieces Pvt. Ltd'
#             employee_name = user.username
#             description = 'Welcome to our platform!'

#             # Get the home URL
#             home_url = request.build_absolute_uri(reverse('home'))

#             # Custom message for the recipient
#             custom_message = 'We are excited to have you on board. If you have any questions or need assistance, feel free to reach out to our support team.'

#             subject = 'Registration Confirmation'
#             message = f'Dear {employee_name},\n\nThank you for registering with {company_name}!\n\nYour username is: {employee_name}\nYour password is: {password}\nEmail: {user.email}\nIs Staff: {user.is_staff}\n\n{description}\n\n{custom_message}\n\nClick here to visit our home page: {home_url}'
#             send_mail(subject, message, 'sender@example.com', [user.email])

#             return redirect('show_all_user') # Redirect to the home page after registration
#     else:
#         form = CustomUserForm()

#     return render(request, 'register.html', {'form': form})




def register_user(request):
    if request.method == 'POST':
        form = AutoGeneratePasswordForm(request.POST)

        if form.is_valid():
            # Create a new user instance
            user = form.save(commit=False)

            # Set additional attributes for the user
            user.is_active = form.cleaned_data['is_active']
            user.is_staff = form.cleaned_data['is_staff']

            # Generate a random password for the user
            password = form.generate_random_password()
            user.set_password(password)

            # Save the user instance to the database
            user.save()

            # Add app_name to user instance
            app_names = form.cleaned_data['app_name']
            user.app_name.set(app_names)
            app_names_str = ", ".join(str(name) for name in app_names)

            # Prepare the email message to send to the user
            company_name = 'Actevia Technology Services Pvt. Ltd'
            employee_name = user.username
            description = 'Welcome to our platform!'
            home_url = request.build_absolute_uri(reverse('home'))
            custom_message = 'We are excited to have you on board. If you have any questions or need assistance, feel free to reach out to our support team.'

            subject = 'Registration Confirmation'
            message = f'Dear {employee_name},\n\nThank you for registering with {company_name}!\n\nYour username is: {employee_name}\nYour password is: {password}\nEmail: {user.email}\nIs Staff: {user.is_staff}\nApp Name: {app_names_str}\n\n{description}\n\n{custom_message}\n\nClick here to visit our home page: {home_url}'
            send_mail(subject, message, 'sender@example.com', [user.email])

            # Redirect to the page that shows all users
            return redirect('show_all_user')

        else:
            # If the form is not valid, display the error message
            error_message = "There was an error processing your request. Please try again later."
            if form.errors:
                error_message = "The following errors occurred: " + " ".join([error[0] for error in form.errors.values()])

            context = {'form': form, 'error_message': error_message}

    else:
        # If the request method is not POST, create a new form instance
        form = AutoGeneratePasswordForm()
        context = {'form': form}

    # Render the template with the context
    return render(request, 'policy/register.html', context)


from django.contrib.auth.models import Group

from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist



def show_all_user(request):
    try:
        # Get the STUDENT and TEACHER groups
        student_group = Group.objects.get(name='STUDENT')
        teacher_group = Group.objects.get(name='TEACHER')
    except ObjectDoesNotExist:
        student_group = None
        teacher_group = None

    # Exclude student and teacher users from the query
    users = CustomUser.objects.exclude(
        Q(student_profile__isnull=False, groups=student_group) |
        Q(teacher_profile__isnull=False, groups=teacher_group)
    )

    # Get the username filter from the request parameters
    username_filter = request.GET.get('username')

    # Apply the username filter if it exists
    if username_filter:
        users = users.filter(username__icontains=username_filter)

    return render(request, "policy/show_add_user.html", {"users": users})




def update_user_view(request, pk):
    user = get_object_or_404(CustomUser, id=pk)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('show_all_user')  # Replace with the appropriate URL name for your user list view
    else:
        form = UpdateUserForm(instance=user)
    return render(request, 'policy/update_user_views.html', {'form': form, 'user': user})


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Check if the user is a superuser
            if user.is_superuser:
                login(request, user)
                return redirect('show_all_user')
            else:
                login(request, user)
                return redirect('portal/')
        else:
            # Invalid credentials
            error_message = 'Invalid username or password'
            messages.error(request, error_message)
            return redirect('/')
    else:
        return render(request, 'cridential/login.html')  

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')



def delete_user(request):
    if request.method == 'POST':
        selected_users = request.POST.getlist('selected_users')
        if selected_users:
            num_deleted = CustomUser.objects.filter(id__in=selected_users).delete()[0]
            messages.success(request, f"{num_deleted} user(s) deleted successfully.")
        else:
            messages.warning(request, "No users selected for deletion.")
    return HttpResponseRedirect("/cridential/show_all_user")



User = get_user_model()

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            error_message = 'Invalid email address'
            return render(request, 'cridential/forgot_password.html', {'error_message': error_message})

        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = reverse('reset_password', kwargs={'uidb64': uidb64, 'token': token})
        reset_url = request.build_absolute_uri(reset_url)

        # Company name and description
        company_name = 'Actevia Technology Servieces Pvt. Ltd'
        description = 'Reset your password for accessing our platform.'

        # Email body with description and company name
        email_body = f"Dear user,<br/><br/>You have requested to reset your password. Please click the link below to reset your password:<br/><br/>" \
                     f"<strong>{description}</strong><br/><br/>" \
                     f"<a href='{reset_url}'>{reset_url}</a><br/><br/>" \
                     f"Thank you for using {company_name}!"

        subject = 'Password Reset'
        send_mail(subject, email_body, 'noreply@example.com', [email], html_message=email_body)

        success_message = 'A password reset link has been sent to your email address'
        return HttpResponseRedirect('/',{'success_message': success_message})

    return render(request, 'cridential/forgot_password.html')



def custom_password_reset_confirm(request, uidb64, token):
    # Decode uidb64 to get the user's primary key
    uid = force_bytes(urlsafe_base64_decode(uidb64))

    # Pass the uid to the PasswordResetConfirmView
    return PasswordResetConfirmView.as_view(
        template_name='cridential/reset_password.html',
        success_url=reverse_lazy('home_login')
    )(request, uidb64=uidb64, token=token)


