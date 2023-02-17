from django.urls import path
from accounts import views
from accounts import views as accounts_view


app_name = 'accounts'

urlpatterns = [

    # path('login', accounts_view.user_login, name='login'),
    path('Contas/Login', accounts_view.user_authentication, name='login'),
    path('Contas/Logout', accounts_view.user_logout, name='logout'),   
    path('Contas/Lock-screen', views.lock_screen, name='lock-screen'),

    path('Contas/Novo-Usuario/<int:notification_pk>/User-ID/<int:id>/', views.UserNotification.as_view(), name='user-notification'),


]