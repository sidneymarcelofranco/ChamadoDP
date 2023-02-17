from django.contrib import admin

from notifications.models import Notification, TipoNotificacao


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    model = Notification
    list_display = [
        'TipoNotificacao', 'to_user', 'user_has_seen',
        ]
    list_filter = ['user_has_seen', 'TipoNotificacao']


admin.site.register(TipoNotificacao)


