from django.urls import path, include

from . import views

urlpatterns = [
    path('score/', views.qc_score, name='score')

]
