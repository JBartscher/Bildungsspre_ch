"""Bildungsspre_ch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from Bildungsspre_chApplikation.views import views, api_views

router = routers.DefaultRouter()

# router.register(r'users', api_views.UserViewSet)
# router.register(r'groups', api_views.GroupViewSet)
router.register(r'words', api_views.WordViewSet)
router.register(r'fields', api_views.FieldViewSet)
router.register(r'description', api_views.DescriptionViewSet)
#router.register(r'random', views.RandomWordView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path(r'', include('Bildungsspre_chApplikation.urls')),

    path('api/', include(router.urls)),

]