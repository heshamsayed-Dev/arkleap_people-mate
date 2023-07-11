
def set_authentication_token(instance):
    access_token=instance.client.post('/api/token/',{
        "username" : instance.user.username,
        "password" : '123'
    }).data.get('access')
    instance.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')