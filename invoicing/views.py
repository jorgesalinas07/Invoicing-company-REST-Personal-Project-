""" Invicing view """


#Django Rest Framework
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

#Permissions
from rest_framework.permissions import IsAuthenticated, AllowAny

#Models
from invoicing.models import Bill
from users.models import Client

#Serializers
from invoicing.serializers import InvoiceModelSerializer, CreateBillSerializer


class InvoiceViewSet(viewsets.ModelViewSet):
    # mixins.RetrieveModelMixin,
    #             viewsets.GenericViewSet,
    #             mixins.UpdateModelMixin):

    queryset = Bill.objects.all()
    serializer_class = InvoiceModelSerializer
    lookup_field = "code"

    def get_permissions(self):
        ##Definir que todo se necesite que sea authenticado
        """ Assign permissions based on action. """
        if self.action in ['create_bill', 'list', 'update_bill']:
            permissions = [IsAuthenticated]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]
    
    @action(detail=False, methods=['post'])
    def create_bill(self, request):
        """ Create bill for a client """
        #client = self.get_object()
        #import ipdb;ipdb.set_trace()
        # serializer = CreateBillSerializer(
        #     data = request.data,
        #     context={'request': request.auth.key}
        # )
        serializer = InvoiceModelSerializer(
            data = request.data,
            #context={'request': request.auth.key}
        )
        serializer.is_valid(raise_exception=True)
        bill = serializer.save()
        data = InvoiceModelSerializer(bill).data
        return Response(data, status = status.HTTP_201_CREATED)

    def get_queryset(self):
        """ Restrict list to public-only """
        queryset = Bill.objects.all()
        if self.action == 'list':
            client_id = Client.objects.get(auth_token=self.request.auth.key)
            return queryset.filter(client_id = client_id )
        return queryset

    @action(detail=True, methods=['put', 'patch'])
    def update_bill(self, request, *args, **kwargs):
        """Update client data."""
        code = self.get_object()
        partial = request.method == 'PATCH' 
        serializer = InvoiceModelSerializer(
            #profile,
            code,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = InvoiceModelSerializer(code).data
        return Response(data)