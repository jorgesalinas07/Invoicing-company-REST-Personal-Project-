""" Bill serializers """

#Django Res Framework
from rest_framework import serializers


#Models
from invoicing.models import Bill, Product
from users.models import Client


class InvoiceModelSerializer(serializers.ModelSerializer):
    """ Bill model serializer """

    #bill = Bill.product.objects.all()

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

class CreateBillSerializer(serializers.Serializer):
    """ Create bill serializer """

    company_name = serializers.CharField(min_length =3,max_length=20)
    nit = serializers.IntegerField()
    code = serializers.IntegerField()
    product_name1 = serializers.CharField(min_length =3,max_length=20)
    product_description1 = serializers.CharField(min_length =3,max_length=20)
    product_name2 = serializers.CharField(min_length =3,max_length=20)
    product_description2 = serializers.CharField(min_length =3,max_length=20)
    product_name3 = serializers.CharField(min_length =3,max_length=20)
    product_description3 = serializers.CharField(min_length =3,max_length=20)

    def create(self,data):
        """ Handle Bill creation """
        client = Client.objects.get(auth_token=self.context['request'])
        #import ipdb;ipdb.set_trace()
        new_bill = client.bill_set.create(
                            company_name = data['company_name'], 
                            nit = data['nit'],
                            code = data['code'],
                            )
        product1 = Product.objects.create(name = data['product_name1'], description = data['product_description1'])
        product2 = Product.objects.create(name = data['product_name2'], description = data['product_description2'])
        product3 = Product.objects.create(name = data['product_name3'], description = data['product_description3'])
        #import ipdb;ipdb.set_trace()
        #new_bill = Bill.objects.get(nit=data['code'])
        new_bill.product.add(product1, product2, product3)
        return new_bill