from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField
from django.utils.translation import gettext_lazy as _

from santri_app.users.managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for Santri App.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    email = EmailField(_("email address"), unique=True)
    native_language = CharField(_("Native language"), max_length=2, default=settings.LANGUAGES[0][0])
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
