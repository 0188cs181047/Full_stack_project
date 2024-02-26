from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

class AppNameBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, app_name=None, **kwargs):
        UserModel = get_user_model()

        # get the user model associated with the app name
        if app_name == 'myapp':
            user_model = UserModel.objects.filter(myappuser__username=username).first()
        elif app_name == 'hiring':
            user_model = UserModel.objects.filter(hiringuser__username=username).first()
            
        elif app_name == 'assetapp':
            user_model = UserModel.objects.filter(assetappuser__username=username).first()

        else:
            user_model = None

        if user_model is not None and user_model.check_password(password):
            return user_model
        else:
            return None
