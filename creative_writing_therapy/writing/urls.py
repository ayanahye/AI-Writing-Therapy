from django.urls import path 
from django.views.generic import TemplateView
from . import views
from .views import handle_request, generate_poem_line

# base path loads index page
urlpatterns = [
    path("api/", handle_request, name='api_request'),
    path("api/poem/", generate_poem_line, name="generate_poem_line"),
    path('', views.index, name='index'),
]

