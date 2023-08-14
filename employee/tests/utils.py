def set_authentication_token(instance):
    access_token = instance.client.post(
        "/api/login",
        {
            "email": instance.user.email,
            "password": "123Aa$bb",
            "otp": instance.totp.now(),
        },
    ).data.get("access")

    instance.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
