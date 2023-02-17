from django.contrib import admin
from django.urls import path, re_path
from django.urls.conf import include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import RedirectView

urlpatterns = [
    re_path(r'^$', RedirectView.as_view(url='/Chamado/')),
    path('Chamado/', include('accounts.urls')), 
    path('Chamado/', include('solicitation.urls')), 
    path('Chamado/', include('administration.urls')), 
    path('Chamado/', include('help_pages.urls')), 
    path('Chamado/', include('notifications.urls')), 
    path('Administracao-Chamado-DP-TI/', admin.site.urls),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
] 

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
