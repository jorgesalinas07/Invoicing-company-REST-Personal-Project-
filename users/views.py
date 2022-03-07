#Django Rest Framework
from rest_framework import viewsets,mixins

#Serializers
from empresa_de_facturacion.users.serializers import ClientModelSerializer

#Models
from users.models import Client


class UserViewSet(mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):

    queryset = Client.objects.filter(is_active=True)
    serializer_class = ClientModelSerializer
    lookup_field = "first_name"

    # @action(detail=False, methods = ['post'])
    # def signup(self, request):
    #     """ Client Signup """
    #     pass