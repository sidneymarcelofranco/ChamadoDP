from django.urls import path
from notifications import views  


app_name = 'notifications'

urlpatterns = [
    path('Notificacoes/<int:notification_pk>/Solicitacao/<int:id>', views.PostNotification.as_view(), name='post-notification'),
    path('Notificacoes/Minhas-Notificacoes/', views.list_notifications, name='list_notifications'),
    path('Notificacoes/Minhas-Notificacoes/Partials', views.partial_notifications, name='partial_notifications'),
    
    path('Notificacoes/Minhas-Notificacoes/Arquivadas/', views.list_notifications_archive, name='list_notifications_archive'),
    path('Notificacoes/Minhas-Notificacoes/Partials/Arquivadas', views.partial_notifications_archive, name='partial_notifications_archive'),

    path('Notificacoes/Minhas-Notificacoes/Marcar-Como-Lida/<int:notification_pk>/', views.mark_as_read, name='mark_as_read'),
    path('Notificacoes/Minhas-Notificacoes/Marcar-Como-Nao-Lida/<int:notification_pk>/', views.mark_as_unread, name='mark_as_unread'),
    path('Notificacoes/Minhas-Notificacoes/Marcar-Todas-Como-Lidas/', views.mark_all_read, name='mark_all_read'),

    path('Notificacoes/Minhas-Notificacoes/Arquivar-Notificacao/<int:notification_pk>/', views.mark_archive, name='mark_archive'),
    path('Notificacoes/Minhas-Notificacoes/Marcar-Todas-Como-Arquivadas/', views.mark_all_archive, name='mark_all_archive'),

    path('Notificacoes/Minhas-Notificacoes/Desarquivar-Notificacao/<int:notification_pk>/', views.mark_unarchive, name='mark_unarchive'),
    path('Notificacoes/Minhas-Notificacoes/Marcar-Todas-Como-Desarquivadas/', views.mark_all_unarchive, name='mark_all_unarchive'),

    path('Notificacoes/Minhas-Notificacoes/Deletar-Notificacao/<int:notification_pk>/', views.delete_notification, name='delete_notification'),
    path('Notificacoes/Minhas-Notificacoes/Deletar-Notificacao/Arquivada/<int:notification_pk>/', views.delete_notification_achive, name='delete_notification_achive'),
    path('Notificacoes/Minhas-Notificacoes/Deletar-Todas-Notificacoes/', views.delete_all_notifications, name='delete_all_notifications'),
    path('Notificacoes/Minhas-Notificacoes/Deletar-Todas-Notificacoes/Arquivadas/', views.delete_all_archive, name='delete_all_archive'),
]