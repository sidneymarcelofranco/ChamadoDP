from django.urls import path
from solicitation import views

app_name = 'solicitation'

urlpatterns = [
    path('', views.index, name='index'),
    path('Solicitar/', views.make_request, name='make_request'),
    path('Meus-Chamados/', views.user_list_request, name='user_list_request'),
    path('Meus-Chamados/Detalhes/Chamado-N-<int:id>', views.details_request, name='datails_requests'),  
    path('Meus-Chamados/Editar/Chamado-N-<int:id>', views.update_request, name='update_request'), 
]