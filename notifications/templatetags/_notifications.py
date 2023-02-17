from django import template

from notifications.models import Notification

register = template.Library()


@register.inclusion_tag('notifications/nav_notifications.html',  takes_context=True)
def system_notification(context):
    request_user = context['request'].user
    
    notifications = Notification.objects.select_related('to_user').filter(
        to_user=request_user).exclude(
        user_has_seen=True
        ).order_by('-DataNotificacao')

    users_notification = Notification.objects.filter(to_user=request_user, user_has_seen=0).count()
    counts = (users_notification * 5) + 1
    context = {
        'notifications': notifications, 
        'users_notification':users_notification,
        'counts':counts
    }    
    return context