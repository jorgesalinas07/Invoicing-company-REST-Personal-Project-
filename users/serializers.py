#Django
from django.contrib.auth import password_validation, authenticate
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.conf import settings


#Django Rest Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token

#Models
from users.models import Client

#Utilities
import jwt
from datetime import timedelta

class ClientModelSerializer(serializers.ModelSerializer):
    """ User model serializer """

    class Meta:
        model = Client
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'document',
            'date_joined',
        )

class ClientSignupSerializer(serializers.Serializer):
    """ User sign up serializer 
    Handle sign up data validation and user/profile creation.
    """

    #Principal field
    email =                 serializers.EmailField(validators = [UniqueValidator(queryset=Client.objects.all())])
    username =              serializers.CharField(   min_length =4,
                                        max_length=20,
                                        validators = [
                                            UniqueValidator(queryset = Client.objects.all())
                                        ]
    )

    #Name
    first_name =            serializers.CharField(min_length = 4, max_length = 20)
    last_name =             serializers.CharField(min_length = 4, max_length = 20)

    #Document
    document =              serializers.IntegerField()

    #Password
    password =              serializers.CharField(min_length = 8, max_length=64)
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
        client = Client.objects.create_user(**data, is_verified = False, is_active = True)
        self.send_confirmation_email(client)
        return(client)

    def send_confirmation_email(self, client):
        """ Send account verification link to given user. """
        verification_token = self.gen_verification_token(client)
        subject = 'WElcome @{}! Verify your account to start using Comparte Ride'.format(client.first_name)
        from_email = "Company email <noreply@company.com>"
        text_content = render_to_string(
            'emails/users/account_verification.html',
            {'token': verification_token, 'client': client}
        )
        msg = EmailMultiAlternatives(subject, text_content, from_email, [client.email])
        msg.attach_alternative(text_content, "text/html")
        msg.send()
    
    def gen_verification_token(self, client):
        """ Create JWT token that the user can use to verify its account. """
        exp_date = timezone.now() + timedelta(days=3)
        payload = {
            'client':client.email,
            'exp':int(exp_date.timestamp()),
            'type':'email_confirmation'
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm = 'HS256')
        return token.decode()
        
class ClientLoginSerializer(serializers.Serializer):
    """ Client login serializer.
    Handle the login request data. """

    email =         serializers.EmailField()
    password =      serializers.CharField(min_length = 8, max_length = 64)

    def validate(self, data):
        """ Check credentials. """
        client = authenticate(username = data['email'], password = data['password'])
        if not client:
            raise serializers.ValidationError('Invalid credentials')
        if not client.is_verified:
            raise serializers.ValidationError("Account is not active yet :(")
        self.context['client'] = client
        return data
    
    def create(self, date):
        """ Generate or retrive new token """
        token, created = Token.objects.get_or_create(user = self.context['client'])
        return self.context['client'], token.key

class ClientVerificationSerializer(serializers.Serializer):
    """ Account Verification serializer """
    token = serializers.CharField()

    def validate_token(self, data):
        """ Verify token is valid """
        try:
            payload = jwt.decode(data,settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Verification link has expired.')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid token') 
        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Invalid token')

        self.context['payload'] = payload
        return data

    def save(self):
        """ Update user's verified status. """
        payload = self.context['payload']
        client = Client.objects.get(email = payload['client'])
        client.is_verified = True
        client.save()

