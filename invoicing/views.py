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
    lookup_field = "username"

    def get_permissions(self):
        """ Assign permissions based on action. """
        if self.action in ['create_bill', 'list']:
            permissions = [IsAuthenticated]
        else:
            permissions = [AllowAny]
        return [p() for p in permissions]
    
    @action(detail=False, methods=['post'])
    def create_bill(self, request):
        """ Create bill for a client """
        #client = self.get_object()
        #import ipdb;ipdb.set_trace()
        serializer = CreateBillSerializer(
            data = request.data,
            context={'request': request.auth.key}
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