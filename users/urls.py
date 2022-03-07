""" Users URLs."""

#Django
from django.urls import path, include

#Django REST Framework
from rest_framework.routers import DefaultRouter

#Views
from users import views

router = DefaultRouter()
router.register(r'users', views.ClientViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
#    path('users/', views.hello)
]
