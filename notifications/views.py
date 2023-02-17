from django.db.models import Count, Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import View
from django.core.paginator import Paginator
from django.contrib import messages

from django.utils import timezone
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

from notifications.models import Notification
from solicitation.decorators import complete_tutorial
from solicitation.models import Solicitacoes

class PostNotification(View):
    def get(self, request, notification_pk, id, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)

        notification.user_has_seen = True
        if notification.DataVisualizacao == None:
            notification.DataVisualizacao = timezone.now()                        
        notification.save()


        if notification.TipoNotificacao_id == 7:
            solicitacao = Solicitacoes.objects.get(id=id)
            solicitacao = solicitacao.id
            for user in User.objects.filter(is_staff=True):
                    Notification.objects.create(
                        TipoNotificacao_id=13, from_user=request.user, to_user_id=user.id, to_admin=1, Solicitacao_id=solicitacao)
                
        if request.user.is_staff == True:
            return redirect('administration:admin_update_request',id=id)
        else:
            return redirect('solicitation:datails_requests', id=id)

@login_required
def list_notifications(request):
    template = 'notifications/base_notifications.html'

    user = request.user
    request_user = user.id
    query = Notification.objects.filter(to_user=user).order_by('-id')

    notifications = Notification.objects.filter(to_user=request_user).aggregate(
        total_notification=Count('id'),
        unchecked=Count('id', Q(user_has_seen=0)),
        checked=Count('id', Q(user_has_seen=1)),
        checkednotachive=Count('id', Q(user_has_seen=1, user_has_archive=0)),
        archived=Count('id', Q(user_has_seen=1, user_has_archive=1))
    )

    query = Paginator(query, 20)

    page_number = request.GET.get('page')
    query = query.get_page(page_number)


    context = {
        'query':query,
        'notifications':notifications,
    }
    return render(request, template, context)

    
@login_required
def partial_notifications(request):
    template = 'notifications/partials/_list_notifications.html'

    user = request.user
    query = Notification.objects.filter(to_user=user).order_by('-id')    

    query = Paginator(query, 20)

    page_number = request.GET.get('page')
    query = query.get_page(page_number)
    context = {
        'query':query
    }
    return render(request, template, context)


@login_required
def list_notifications_archive(request):
    template = 'notifications/base_notifications_archive.html'

    user = request.user
    request_user = user.id
    query = Notification.objects.filter(to_user=user, user_has_archive=1).order_by('-id')

    notifications = Notification.objects.filter(to_user=request_user).aggregate(
        total_notification=Count('id'),
        unchecked=Count('id', Q(user_has_seen=0)),
        checked=Count('id', Q(user_has_seen=1)),
        checkednotachive=Count('id', Q(user_has_seen=1, user_has_archive=0)),
        archived=Count('id', Q(user_has_seen=1, user_has_archive=1))
    )
    query = Paginator(query, 20)

    page_number = request.GET.get('page')
    query = query.get_page(page_number)

    context = {
        'query':query,
        'notifications':notifications,
    }
    return render(request, template, context)

    
@login_required
def partial_notifications_archive(request):
    template = 'notifications/partials/_list_notifications_archive.html'

    user = request.user
    query = Notification.objects.filter(to_user=user).order_by('-id')    

    query = Paginator(query, 20)

    page_number = request.GET.get('page')
    query = query.get_page(page_number)
    context = {
        'query':query
    }
    return render(request, template, context)


@login_required
def mark_as_read(request, notification_pk, *args, **kwargs): 
    notification = Notification.objects.get(pk=notification_pk)
    notification.user_has_seen = True
    if notification.DataVisualizacao == None:
        notification.DataVisualizacao = timezone.now()
    notification.save()    
    messages.success(
                    request, f'Notificação Marcada como Lida!'                         
                    )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def mark_as_unread(request, notification_pk, *args, **kwargs): 
    notification = Notification.objects.get(pk=notification_pk)
    notification.user_has_seen = False
    notification.save()
    messages.info(
                    request, f'Notificação Marcada como Não Lida!'                         
                    )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def mark_all_read(request, *args, **kwargs): 
    user = request.user
    count = Notification.objects.only('id').filter(to_user=user, user_has_seen=0).count()
    Notification.objects.filter(to_user=user, user_has_seen=0).exclude(TipoNotificacao_id=7).update(user_has_seen=1)
    Notification.objects.filter(DataVisualizacao=None).exclude(TipoNotificacao_id=7).update(DataVisualizacao=timezone.now())
    messages.info(
                    request, f'{count} Notificações Marcadas como Lidas!'                         
                    )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def mark_archive(request, notification_pk, *args, **kwargs):
    template_name = 'notifications/list_notifications.html'
    if request.method == "POST":
        user = request.user
    notification = Notification.objects.get(pk=notification_pk)
    notification.user_has_archive = True
    notification.save()
    messages.success(
                    request, f'Notificação Arquivada!'                         
                    )
    request_user = user.id
    query = Notification.objects.filter(to_user=user).order_by('-id')

    query = Paginator(query, 20)

    page_number = request.GET.get('page')
    query = query.get_page(page_number)
    notifications = Notification.objects.filter(to_user=request_user).aggregate(
        total_notification=Count('id'),
        unchecked=Count('id', Q(user_has_seen=0)),
        checked=Count('id', Q(user_has_seen=1)),
        checkednotachive=Count('id', Q(user_has_seen=1, user_has_archive=0)),
        archived=Count('id', Q(user_has_seen=1, user_has_archive=1))
    )

    context = {
        'query':query,
        'notifications':notifications,
    }
    return render(request, template_name, context)


@login_required
def mark_all_archive(request):
    template_name = 'notifications/list_notifications.html'
    if request.method == "POST":
        user = request.user
    count = Notification.objects.only('id').filter(to_user=user, user_has_seen=1, user_has_archive=0).count()
    Notification.objects.filter(to_user=user, user_has_seen=1, user_has_archive=0).update(user_has_archive=1)
    messages.warning(
                    request, f'{count} Notificações Arquivadas!'                         
                    )
    request_user = user.id
    query = Notification.objects.filter(to_user=user).order_by('-id')

    query = Paginator(query, 20)

    page_number = request.GET.get('page')
    query = query.get_page(page_number)
    notifications = Notification.objects.filter(to_user=request_user).aggregate(
        total_notification=Count('id'),
        unchecked=Count('id', Q(user_has_seen=0)),
        checked=Count('id', Q(user_has_seen=1)),
        checkednotachive=Count('id', Q(user_has_seen=1, user_has_archive=0)),
        archived=Count('id', Q(user_has_seen=1, user_has_archive=1))
    )

    context = {
        'query':query,
        'notifications':notifications,
    }
    return render(request, template_name, context)

@login_required
def mark_unarchive(request, notification_pk, *args, **kwargs):
    template_name = 'notifications/list_notifications_archive.html'
    if request.method == "POST":
        user = request.user
    notification = Notification.objects.get(pk=notification_pk)
    notification.user_has_archive = False
    notification.save()
    messages.success(
                    request, f'Notificação Desarquivada!'                         
                    )
    request_user = user.id
    query = Notification.objects.filter(to_user=user).order_by('-id')

    notifications = Notification.objects.filter(to_user=request_user).aggregate(
        total_notification=Count('id'),
        unchecked=Count('id', Q(user_has_seen=0)),
        checked=Count('id', Q(user_has_seen=1)),
        checkednotachive=Count('id', Q(user_has_seen=1, user_has_archive=0)),
        archived=Count('id', Q(user_has_seen=1, user_has_archive=1))
    )
    query = Paginator(query, 20)

    page_number = request.GET.get('page')
    query = query.get_page(page_number)

    context = {
        'query':query,
        'notifications':notifications,
    }
    return render(request, template_name, context)
    

@login_required
def mark_all_unarchive(request):
    template_name = 'notifications/list_notifications.html'
    if request.method == "POST":
        user = request.user
    count = Notification.objects.only('id').filter(to_user=user, user_has_archive=1).count()
    Notification.objects.filter(to_user=user, user_has_seen=1, user_has_archive=1).update(user_has_archive=0)
    messages.info(
                request, f'{count} Notificações Desarquivadas!'                         
                )
    request_user = user.id
    query = Notification.objects.filter(to_user=user).order_by('-id')

    query = Paginator(query, 20)

    page_number = request.GET.get('page')
    query = query.get_page(page_number)
    notifications = Notification.objects.filter(to_user=request_user).aggregate(
        total_notification=Count('id'),
        unchecked=Count('id', Q(user_has_seen=0)),
        checked=Count('id', Q(user_has_seen=1)),
        checkednotachive=Count('id', Q(user_has_seen=1, user_has_archive=0)),
        archived=Count('id', Q(user_has_seen=1, user_has_archive=1))
    )

    context = {
        'query':query,
        'notifications':notifications,
    }
    return render(request, template_name, context)
    

@login_required
def delete_notification(request, notification_pk, *args, **kwargs):
    template_name = 'notifications/list_notifications.html'
    user = request.user
    notification = Notification.objects.get(pk=notification_pk)
    notification.delete()
    messages.error(
                    request, f'Notificação Deletada!'                         
                    )  
    request_user = user.id
    query = Notification.objects.filter(to_user=user).order_by('-id')

    query = Paginator(query, 20)

    page_number = request.GET.get('page')
    query = query.get_page(page_number)
    notifications = Notification.objects.filter(to_user=request_user).aggregate(
        total_notification=Count('id'),
        unchecked=Count('id', Q(user_has_seen=0)),
        checked=Count('id', Q(user_has_seen=1)),
        checkednotachive=Count('id', Q(user_has_seen=1, user_has_archive=0)),
        archived=Count('id', Q(user_has_seen=1, user_has_archive=1))
    )

    context = {
        'query':query,
        'notifications':notifications,
    }
    return render(request, template_name, context)

@login_required
def delete_notification_achive(request, notification_pk, *args, **kwargs):
    template_name = 'notifications/list_notifications_archive.html'
    user = request.user
    notification = Notification.objects.get(pk=notification_pk)
    notification.delete()
    messages.error(
                    request, f'Notificação Deletada!'                         
                    )  
    request_user = user.id
    query = Notification.objects.filter(to_user=user).order_by('-id')

    query = Paginator(query, 20)

    page_number = request.GET.get('page')
    query = query.get_page(page_number)
    notifications = Notification.objects.filter(to_user=request_user).aggregate(
        total_notification=Count('id'),
        unchecked=Count('id', Q(user_has_seen=0)),
        checked=Count('id', Q(user_has_seen=1)),
        checkednotachive=Count('id', Q(user_has_seen=1, user_has_archive=0)),
        archived=Count('id', Q(user_has_seen=1, user_has_archive=1))
    )

    context = {
        'query':query,
        'notifications':notifications,
    }
    return render(request, template_name, context)

@login_required
def delete_all_notifications(request):
    template_name = 'notifications/list_notifications.html'
    user = request.user
    count = Notification.objects.only('id').filter(to_user=user, user_has_seen=1, user_has_archive=0).exclude(TipoNotificacao_id=7).count()
    Notification.objects.filter(to_user=user, user_has_seen=1, user_has_archive=0).exclude(TipoNotificacao_id=7).delete()
    messages.error(
                    request, f'{count} Notificações Deletadas!'                                             
                                                                         
                    )
    messages.info( request, f'As Notificações de RESPOSTA não podem ser Deletadas, apenas Arquivadas.')
    request_user = user.id
    query = Notification.objects.filter(to_user=user).order_by('-id')

    query = Paginator(query, 20)

    page_number = request.GET.get('page')
    query = query.get_page(page_number)
    notifications = Notification.objects.filter(to_user=request_user).aggregate(
        total_notification=Count('id'),
        unchecked=Count('id', Q(user_has_seen=0)),
        checked=Count('id', Q(user_has_seen=1)),
        checkednotachive=Count('id', Q(user_has_seen=1, user_has_archive=0)),
        archived=Count('id', Q(user_has_seen=1, user_has_archive=1))
    )

    context = {
        'query':query,
        'notifications':notifications,
    }
    return render(request, template_name, context)

@login_required
def delete_all_archive(request):
    template_name = 'notifications/list_notifications_archive.html'
    user = request.user
    count = Notification.objects.only('id').filter(to_user=user, user_has_archive=1).exclude(TipoNotificacao_id=7).count()
    Notification.objects.filter(to_user=user, user_has_archive=1).exclude(TipoNotificacao_id=7).delete()
    messages.error(
                    request, f'{count} Notificações Deletadas!'                         
                    )
    messages.info( request, f'As Notificações de RESPOSTA não podem ser Deletadas, apenas Arquivadas.')
    request_user = user.id
    query = Notification.objects.filter(to_user=user).order_by('-id')

    query = Paginator(query, 20)

    page_number = request.GET.get('page')
    query = query.get_page(page_number)
    notifications = Notification.objects.filter(to_user=request_user).aggregate(
        total_notification=Count('id'),
        unchecked=Count('id', Q(user_has_seen=0)),
        checked=Count('id', Q(user_has_seen=1)),
        checkednotachive=Count('id', Q(user_has_seen=1, user_has_archive=0)),
        archived=Count('id', Q(user_has_seen=1, user_has_archive=1))
    )

    context = {
        'query':query,
        'notifications':notifications,
    }
    return render(request, template_name, context)
