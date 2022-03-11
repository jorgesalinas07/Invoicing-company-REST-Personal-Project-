#Django
from django.contrib import admin

#Local
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """ Administrator of client model """
    
    list_display =          ( 'pk', 'first_name', 'last_name', 'email', 'document', 'is_active' ,)
    list_display_links =    ('pk', 'document',)
    list_editable =         ( 'first_name', 'last_name' ,)
    search_fields =         ('first_name', 'last_name', 'document',)
    list_filter =           ('document', 'first_name',)