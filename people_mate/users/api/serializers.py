from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ["username", "name", "url",'password','password_confirm']

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"},
            'password' : {'write_only':True},
        }


    def validate(self, data):
        if(data.get('password') != data.get('password_confirm')):
            raise  serializers.ValidationError({'details':'passwords didnt match'})

        return data

    def create(self,validated_data,**kwargs):
        user = User.objects.create_user(
            username=validated_data['username'],
        )

        user.set_password(validated_data['password'])
        user.save()
        return user    
