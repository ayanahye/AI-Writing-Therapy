from django.urls import path 
from django.views.generic import TemplateView
from . import views
from .views import handle_request

# base path loads index page
urlpatterns = [
    path("api/", handle_request, name='api_request'),
    path('', views.index, name='index'),
]

