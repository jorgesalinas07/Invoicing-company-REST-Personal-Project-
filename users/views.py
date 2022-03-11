#Python
import csv


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


class ClientViewSet(viewsets.ModelViewSet):

    queryset = Client.objects.all()
    serializer_class = ClientModelSerializer
    lookup_field = "username"

    def get_permissions(self):
        """ Assign permissions based on action. """
        #Para las acciones ['signup', 'login', 'verify'] se tienen todos los permisos
        if self.action in ['signup', 'login', 'verify']:
            permissions = [AllowAny]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
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

def downloadfile(request):
    """ Download a file with all clients information """

    response = HttpResponse(content_type = 'text/csv')
    writer = csv.writer(response)
    writer.writerow(['first_name','last_name', 'document', 'Bill_quantity'])

    bill_quantity = []
    for client in Client.objects.all():
        bill_quantity.append(len(client.bill_set.all()))
    main_values = Client.objects.all().values_list('first_name','last_name', 'document')
    present_values = []
    for value, quantity in zip(main_values,bill_quantity):
        present_values.append(value+(quantity,))

    for client in present_values:
        writer.writerow(client)
    
    response['Content-Disposition'] = ' attachment; filename ="clients.csv" '

    return response

def importfile(request):
    clients = []
    with open('clients.csv', 'r') as imported_clients:
        data = list(csv.reader(imported_clients, delimiter=','))
        
        for row in data[1:]:
            clients.append(
               Client(
                   first_name =     row[0],
                   last_name =      row[1],
                   email =          row[2],
                   username =       row[3],
                   document =       row[4],
                   password =       row[5],
               ) 
            )
    if len(clients)>0:
        Client.objects.bulk_create(clients)
    
    return HttpResponse('Successfully imported')