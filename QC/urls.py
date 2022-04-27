from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.qc, name='qc'),
    path('score/', views.qc_score, name='score'),
    path('voice/', views.voice, name='voice'),
    path('history/', views.score_history, name='score_history'),
    path('delete/<int:pk>/', views.delete_voice, name='delete_voice'),
    path('detail_socre/<int:pk>/', views.detail_score, name='detail_score'),
    path('agent/', views.agent_history, name='agent'),
    path('agent_detail/<int:pk>', views.agent_history_detail, name='agent_detail'),
    path('policy/', views.set_policy, name='policy'),
    path('excel/', views.excel_report, name='qc_excel'),
    path('plot/', views.plot, name='plot'),
    path('extra/', views.extra_voice, name='extra'),
    path('complete/<int:pk>', views.complete_extra_voice, name='complete'),
    path('outscore/', views.output_qc_score, name='outscore'),
    path('refscore/', views.ref_qc_score, name='refscore')

]
