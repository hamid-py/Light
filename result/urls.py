from django.contrib import admin
from django.urls import path, include
<<<<<<< HEAD
from django.views.generic import TemplateView, RedirectView
=======
from django.views.generic import TemplateView
>>>>>>> e3f679a6cb149506ee61418f79b367f57380e21a

from . import views, forms

urlpatterns = [
    path('', views.home, name='home'),
    # path('', TemplateView.as_view(template_name='result/home.html'), name='home'),
    path('user', views.UserListView.as_view(), name='user'),
    path('group', views.GroupLIstView.as_view(), name='group'),
    path('principal', views.principal_view, name='principal'),
    path('principal_update/<int:pk>', views.update_principal, name='update_principal'),
    path('rest', views.start_rest, name='start_rest'),
    path('end/<int:pk>', views.end_rest, name='end_rest'),
    path('membership', views.membership_view, name='membership'),
    path('membership_update/<int:pk>', views.update_membership_view, name='update_membership'),
    path('history', views.AgentHistoryView.as_view(), name='history'),
    path('login', views.LoginAdmin.as_view(), name='login'),
    path('change_password', views.change_password, name='change_password'),
    path('report', views.report_export, name='report'),
<<<<<<< HEAD
    path('excel_report', views.excelreport, name='excel'),

=======
    path('excel_report', views.excelreport, name='excel')
>>>>>>> e3f679a6cb149506ee61418f79b367f57380e21a

]
