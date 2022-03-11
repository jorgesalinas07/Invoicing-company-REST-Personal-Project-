""" Bill serializers """

#Django Res Framework
from dataclasses import field
from itertools import product
from rest_framework import serializers

#Exceptions
from django.db import IntegrityError

#Models
from invoicing.models import Bill, Product
from users.models import Client


class BillFieldsRequired(serializers.Serializer):

    company_name = serializers.CharField(min_length =3,max_length=20)
    nit = serializers.IntegerField()
    code = serializers.IntegerField()
    product_data = serializers.JSONField()


class ProductSerializer(serializers.ModelSerializer):
    """ Serializer for the products """
    class Meta:
        model = Product
        fields = ('name', 'description')


class InvoiceModelSerializer(serializers.ModelSerializer):
    """ Bill model serializer """
    product = ProductSerializer(many = True)

    class Meta:
        model = Bill
        fields = (
            'company_name',
            'nit',
            'code',
            'product',
        )

class CreateBillSerializer(BillFieldsRequired, serializers.Serializer):
    """ Create bill serializer """

    def validate(self,data):
        """ Validate product data has name and description keys """
        available_words = ['name', 'description']
        for index in data['product_data']:
            for key in index.keys():
                if not key in available_words:
                    raise serializers.ValidationError("Expecting name and description in the product data")
        return data

    def create(self,data):
        """ Handle Bill creation """
        client = Client.objects.get(auth_token=self.context['token'])
        try: 
            new_bill = client.bill_set.create(
                                company_name = data['company_name'], 
                                nit = data['nit'],
                                code = data['code'],
                                )
        except IntegrityError:
            raise serializers.ValidationError("Code already been used")

        names = []
        descriptions = []
        for index in data['product_data']:
            for index2, value in enumerate(index.values()):
                if index2%2==0:
                    names.append(value)
                else:
                    descriptions.append(value)

        for name, description in zip(names,descriptions):
            new_product = Product.objects.create(name = name, description = description)
            new_bill.product.add(new_product)
        return new_bill
    
    
class UpdateBillSerializer(BillFieldsRequired, serializers.Serializer):
    """ Update Bill serializer """

    def validate(self,data):
        """ Validate product data has name and description keys and size of dict is same as first one """
        try:
            available_words = ['name', 'description']
            for index in data['product_data']:
                for key in index.keys():
                    if not key in available_words:
                        raise serializers.ValidationError("Expecting name and description in the product data")
            return data
        except KeyError:
            return data

    def update(self,data):
        """ Handle update Bill requests """
        bill = self.context['invoice']
        bill.company_name = data['company_name']
        bill.nit = data['nit']
        try:
            bill.code = data['code']
        except IntegrityError:
            raise serializers.ValidationError("Code already been used")
        names = []
        descriptions = []
        for index in data['product_data']:
            for index2, value in enumerate(index.values()):
                if index2%2==0:
                    names.append(value)
                else:
                    descriptions.append(value)

        for name, description, product in zip(names,descriptions, bill.product.all()):
            product.name = name
            product.description = description
            product.save()
        bill.save()
        return bill
    
    def partial_update(self,data):
        """ Handle partial bill update resquests """
        bill = self.context['invoice']

        try:
            bill.company_name = data['company_name']
        except KeyError:
            pass
        try:
            bill.nit = data['nit']
        except KeyError:
            pass
        try:
            try:
                bill.code = data['code']
            except IntegrityError:
                raise serializers.ValidationError("Code already been used")
        except KeyError:
            pass
        try:
            names = []
            descriptions = []
            for index in data['product_data']:
                for index2, value in enumerate(index.values()):
                    if index2%2==0:
                        names.append(value)
                    else:
                        descriptions.append(value)

            for name, description, product in zip(names,descriptions, bill.product.all()):
                product.name = name
                product.description = description
                product.save()
        except KeyError:
            pass
        bill.save()
        return bill