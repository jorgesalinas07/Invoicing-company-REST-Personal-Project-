#Django
from django.contrib.auth import password_validation


#Django Rest Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

#Models
from users.models import Client

class ClientModelSerializer(serializers.ModelSerializer):
    """ User model serializer """
    class Meta:
        model = Client
        fields = '__all__'

class ClientSignupSerializer(serializers.Serializer):
    """ User sign up serializer 
    Handle sign up data validation and user/profile creation.
    """
    #Principal field
    email = serializers.EmailField(
        validators = [UniqueValidator(queryset=Client.objects.all())]
    )

    #Name
    first_name = serializers.CharField(min_length = 4, max_length = 20)
    last_name = serializers.CharField(min_length = 4, max_length = 20)

    #Document
    document = serializers.IntegerField(min_length = 10)

    #Password
    password = serializers.CharField(min_length = 8, max_length=64)
    password_confirmation = serializers.CharField(min_length = 8, max_length=64)

    def validate(self, data):
        """ Verify password match. """
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError("Passwords do not match")
        password_validation.validate_password(passwd)
        return data
    
    def create(self,data):
        """ Handle user and profule creation """
        data.pop("password_confirmation")
        client = Client.objects.create_user(**data, is_verified = False, is_active = False)
        self.send_confirmation_email(client)
        return(client)

    def send_confirmation_email(self, client):
        """ Send account verification link to given user. """
        verification_token = self.gen_verification_token(client)
        subject = 'WElcome @{}! Verify your account to start using Comparte Ride'.format(client.first_name)
        from_email = "Company email <noreply@company.com>"