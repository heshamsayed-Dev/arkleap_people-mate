import io

import pyotp
import qrcode
from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver

from config.settings.base import EMAIL_HOST_USER

from .models import User


def generate_user_secret_key(user):
    # Generate a new secret key for the user
    secret_key = pyotp.random_base32()

    # Save the secret key in the user model
    user.otp_secret = secret_key
    user.save()


def generate_otp_qrcode(user):
    # generate provisioning URIs for use with the QR Code scanner
    otp_uri = pyotp.totp.TOTP(user.otp_secret).provisioning_uri(name=user.email, issuer_name="People Mate")

    # Generate a QR code image from the OTP URI
    qr = qrcode.make(otp_uri)
    # creates an in-memory byte stream
    image_stream = io.BytesIO()
    # saves the QR code image to the image_stream in PNG format
    qr.save(image_stream, "PNG")
    # sets the position of the image_stream buffer to the beginning
    image_stream.seek(0)

    return image_stream


def send_mail_to_user(email, image_stream):
    email = EmailMessage(
        "OTP QR Code",
        "Please scan the attached QR code using Google Authenticator to set up OTP.",
        EMAIL_HOST_USER,
        [email],
    )
    email.attach("qrcode.png", image_stream.getvalue(), "image/png")

    # Send the email
    email.send(fail_silently=False)


@receiver(post_save, sender=User)
def user_post_save_action(**kwargs):
    # check if user is created not updated
    if kwargs.get("created"):
        user = kwargs.get("instance")
        generate_user_secret_key(user)
        image_stream = generate_otp_qrcode(user)
        send_mail_to_user(user.email, image_stream)


#
