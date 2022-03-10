""" Users URLs."""

#Django
from django.urls import path, include

#Django REST Framework
from rest_framework.routers import DefaultRouter

#Views
from invoicing import views

router = DefaultRouter()
router.register(r'invoicing', views.InvoiceViewSet, basename='invoicing')

urlpatterns = [
    path('', include(router.urls)),
]
