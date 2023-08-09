from django.contrib.auth.models import AbstractUser
from django.db import models

from employee.models.company_model import Company

# from django.db.models import CharField
# from django.urls import reverse
# from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for people_mate.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    # name = CharField(_("Name of User"), blank=True, max_length=255)
    name = None
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    avatar = models.ImageField(upload_to="avatars/", default="avatars/default_avatar.jpg")
    is_active = models.BooleanField(default=False)
    role = models.CharField(max_length=150, null=True)
    email = models.EmailField(unique=True)
    otp_secret = models.CharField(max_length=150, blank=True, null=True)
    companies = models.ManyToManyField(Company, related_name="users", blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    # USERNAME_FIELD = 'email'

    # def get_absolute_url(self) -> str:
    #     """Get URL for user's detail view.

    #     Returns:
    #         str: URL for user detail.

    #     """
    #     return reverse("users:detail", kwargs={"username": self.username})
