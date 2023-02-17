from django.urls import path
from help_pages import views

app_name = 'help_pages'

urlpatterns = [
    path('Ajuda/Adicionar/', views.blog_create, name='blog_create'),  
    path('Ajuda/Atualizar/<slug:SlugBlog>', views.blog_update, name='blog_update'),  
    path('Ajuda/Duvidas-Frequentes/', views.blog_fac, name='blog_fac'),  
    path('Ajuda/Modelos-De-Chamado/', views.blog_modelos, name='blog_modelos'),  
    path('Ajuda/Tutoriais/', views.blog_tutoriais, name='blog_tutoriais'),
    
    path('Ajuda/Notificacoes/<int:id>/Post/<slug:SlugBlog>/', views.blog_details, name='blog_details'),
    path('Ajuda/Notificacoes/<int:notification_pk>/Post/<slug:SlugBlog>/', views.BlogNotification.as_view(), name='blog-notification'),
 
]

htmxurls = [
    path('Ajuda/Duvidas-Frequentes/Like/<int:id>/Post/<slug:SlugBlog>/', views.like, name='like'),
    path('Ajuda/Duvidas-Frequentes/Details/Like/<int:id>/Post/<slug:SlugBlog>/', views.like_details, name='like_details'),
]

urlpatterns += htmxurls