from django.urls import path

from . import views
from .views import indexPage

urlpatterns = [
    path('', views.index, name='index'),
    path('indexPage', indexPage.as_view(), name='indexPage'),
    path('ClaimToken', views.ClaimToken),


]
