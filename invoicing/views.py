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
from invoicing.serializers import InvoiceModelSerializer, CreateBillSerializer, UpdateBillSerializer


class InvoiceViewSet(mixins.ListModelMixin,
                   viewsets.GenericViewSet,
                    mixins.DestroyModelMixin):
    # mixins.RetrieveModelMixin,
    #             viewsets.GenericViewSet,
    #             mixins.UpdateModelMixin):

    queryset = Bill.objects.all()
    serializer_class = InvoiceModelSerializer
    lookup_field = "code"

    def get_permissions(self):
        ##Definir que todo se necesite que sea authenticado
        """ Assign permissions based on action. """
        if self.action in ['create_bill', 'list', 'edit']:
            permissions = [IsAuthenticated]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]
    
    @action(detail=False, methods=['post'])
    def create_bill(self, request):
        """ Create bill for a client """
        #import ipdb;ipdb.set_trace()
        serializer = CreateBillSerializer(
            data = request.data,
            context={'token': request.auth.key}
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
    def edit(self, request, *args, **kwargs):
        """Update client data."""
        invoice = self.get_object()
        partial = request.method == 'PATCH' 
        #import ipdb;ipdb.set_trace()
        serializer = UpdateBillSerializer(
            data=request.data,
            partial=partial,
            context={'invoice': invoice}
        )
        serializer.is_valid(raise_exception=True)
        if partial:
            serializer.partial_update(request.data)
        else:
            serializer.update(request.data)
        #serializer.save()
        data = InvoiceModelSerializer(invoice).data
        return Response(data)

    