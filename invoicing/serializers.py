""" Bill serializers """

#Django Res Framework
from dataclasses import field
from itertools import product
from rest_framework import serializers


#Models
from invoicing.models import Bill, Product
from users.models import Client


class BillFieldsRequired(serializers.Serializer):

    company_name = serializers.CharField(min_length =3,max_length=20)
    nit = serializers.IntegerField()
    code = serializers.IntegerField()
    product_name1 = serializers.CharField(min_length =3,max_length=20)
    product_description1 = serializers.CharField(min_length =3,max_length=20)
    product_name2 = serializers.CharField(min_length =3,max_length=20)
    product_description2 = serializers.CharField(min_length =3,max_length=20)
    product_name3 = serializers.CharField(min_length =3,max_length=20)
    product_description3 = serializers.CharField(min_length =3,max_length=20)
    dicta = serializers.JSONField()


class ProductSerializer(serializers.ModelSerializer):
    """ Serializer for the products """
    class Meta:
        model = Product
        fields = ('name', 'description')


class InvoiceModelSerializer(serializers.ModelSerializer):
    """ Bill model serializer """
    product = ProductSerializer(many = True)
    # company_name = serializers.CharField(min_length =3,max_length=20)
    # code = serializers.IntegerField()


    class Meta:
        model = Bill
        #fields = '__all__'
        fields = (
            #'client_id',
            'company_name',
            'nit',
            'code',
            'product',
        )

class CreateBillSerializer(BillFieldsRequired, serializers.Serializer):
    """ Create bill serializer """

    def create(self,data):
        """ Handle Bill creation """
        client = Client.objects.get(auth_token=self.context['request'])
        new_bill = client.bill_set.create(
                            company_name = data['company_name'], 
                            nit = data['nit'],
                            code = data['code'],
                            )
        product1 = Product.objects.create(name = data['product_name1'], description = data['product_description1'])
        product2 = Product.objects.create(name = data['product_name2'], description = data['product_description2'])
        product3 = Product.objects.create(name = data['product_name3'], description = data['product_description3'])
        new_bill.product.add(product1, product2, product3)
        return new_bill
    
class UpdateBillSerializer(BillFieldsRequired, serializers.Serializer):

    def update(self,data):
        """ Handle update Bill requests """
        pass
