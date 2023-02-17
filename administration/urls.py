from django.urls import path
from administration import views

app_name = 'administration'

urlpatterns = [
    path('Administracao/Pendencias/', views.admin_list_request, name='admin_list_request'),
    path('Administracao/Em-Analise/', views.admin_list_analyse_request, name='admin_list_analyse_request'),
    path('Administracao/Finalizados/', views.admin_list_finished_request, name='admin_list_finished_request'),
    path('Administracao/Pendencias/Responder/Chamado-N-<int:id>', views.admin_update_request, name='admin_update_request'),
    path('Administracao/Chamados-Antigos/', views.admin_list_chamados_antigos, name='admin_list_chamados_antigos'),
    path('Administracao/Chamados-Antigos/Detalhes/Chamado-N-<int:id>', views.admin_details_chamados_antigos, name='admin_details_chamados_antigos'),  
    path('Administracao/Auditoria/Logins/', views.admin_list_login_audit, name='admin_list_login_audit'),
    path('Administracao/Pesquisar/Resultados/', views.navbar_search, name='navbar_search'),
]