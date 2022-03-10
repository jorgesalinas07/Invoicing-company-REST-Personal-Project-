#Django Rest Framework
from django.http import HttpResponse
from rest_framework import viewsets,mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action

#Serializers
from users.serializers import (ClientModelSerializer,ClientSignupSerializer,ClientLoginSerializer, ClientVerificationSerializer)

#Permissions
from rest_framework.permissions import AllowAny, IsAuthenticated

#Models
from users.models import Client


class ClientViewSet(mixins.RetrieveModelMixin,
                viewsets.GenericViewSet,
                mixins.UpdateModelMixin):

    queryset = Client.objects.all()
    serializer_class = ClientModelSerializer
    lookup_field = "username"

    def get_permissions(self):
        """ Assign permissions based on action. """
        #Para las acciones ['signup', 'login', 'verify'] se tienen todos los permisos
        if self.action in ['signup', 'login', 'verify']:
            permissions = [AllowAny]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            permissions = [IsAuthenticated]
        else:
        #Para cualquier otro caso, es autenticado
            permissions = [IsAuthenticated]
        return [p() for p in permissions]
    
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

    @action(detail=False, methods=['post'])
    def verify(self, request):
        """ Accoun verification """
        serializer = ClientVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.save()
        data = {'Message' : 'Congratulation, now go create some invoices!'}
        return Response(data, status = status.HTTP_200_OK)
    
    @action(detail=True, methods=['put', 'patch'])
    def update_client(self, request, *args, **kwargs):
        """Update client data."""
        client = self.get_object()
        partial = request.method == 'PATCH' 
        serializer = ClientModelSerializer(
            #profile,
            client,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = ClientModelSerializer(client).data
        return Response(data)