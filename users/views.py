#Django Rest Framework
from django.http import HttpResponse
from rest_framework import viewsets,mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action

#Serializers
from users.serializers import ClientModelSerializer, ClientSignupSerializer, ClientLoginSerializer

#Models
from users.models import Client


class ClientViewSet(mixins.RetrieveModelMixin,
                viewsets.GenericViewSet,
                mixins.UpdateModelMixin):

    queryset = Client.objects.all()
    serializer_class = ClientModelSerializer
    lookup_field = "first_name"

    @action(detail=False, methods = ['post'])
    def signup(self, request):
        """ Client Signup """
        serializer = ClientSignupSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        client = serializer.save()
        data = ClientModelSerializer(client).data
        return Response(data, status = status.HTTP_201_CREATED)

    @action(detail=False, methods = ['post'])
    def login(self, request):
        """ Client login. """
        serializer = ClientLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        user, token = serializer.save()
        data = {
            'user': ClientLoginSerializer(user).data,
            'access_token' : token,
        }
        return Response(data, status = status.HTTP_201_CREATED)