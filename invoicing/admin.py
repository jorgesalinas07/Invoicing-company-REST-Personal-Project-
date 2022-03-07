#Django
from django.contrib import admin

#Local
from .models import Bill, Product

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    """ Administrator of the bill model """
    list_display = ( 'pk', 'client_id', 'company_name', 'nit', 'code',)
    list_display_links = ('pk',)
    list_editable = ( 'company_name', 'nit', 'code',)
    search_fields = ('company_name', 'nit',)
    list_filter = ('nit', 'company_name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """ Administrator of the product model """
    list_display = ( 'pk', 'name', 'description')
    list_display_links = ('pk',)
    list_editable = ( 'name', 'description')
    search_fields = ('name',)
    list_filter = ('name',)