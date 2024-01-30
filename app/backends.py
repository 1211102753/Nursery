from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

# by TOH EE LIN
class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, username=None, password=None, **kwargs):

        # To support Django Admin login, (auto convert username to email)
        if username:
            email = username

        try:
            user = User.objects.get(email__exact=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
