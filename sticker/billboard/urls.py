from django.urls import path
from . import views

urlpatterns = [

    path('', views.billboard, name='billboard'),
    path('message', views.create_message, name='create_message'),
    path('delete/<int:pk>', views.delete_message, name='delete'),
    path('config', views.add_config, name='config')

]

