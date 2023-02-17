from django import template
from django.db.models import Count, Q
from notifications.models import Notification

register = template.Library()

@register.inclusion_tag('notifications/partials/_popup_notification.html',  takes_context=True)
def popup_notification(context):
    request_user = context['request'].user
    
    query = Notification.objects.filter(to_user=request_user).order_by('-id')
    
    notifications = Notification.objects.filter(to_user=request_user).aggregate(
        total_notification=Count('id', Q(to_user=request_user)),
        unchecked=Count('id', Q(user_has_seen=0)),
        checked=Count('id', Q(user_has_seen=1)),
        checkednotachive=Count('id', Q(user_has_seen=1, user_has_archive=0)),
        archived=Count('id', Q(user_has_seen=1, user_has_archive=1))
    )

    context = {
        'query':query,
        'notifications':notifications,
    }
    return context