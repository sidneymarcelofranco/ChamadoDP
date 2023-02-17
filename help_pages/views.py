from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from help_pages.forms import BlogForm, BlogFormUpdate
from help_pages.models import Categorias, ChamadoBlog, VisualizacaoBlog
from notifications.models import Notification

from django.contrib.auth.models import User

from django.db import IntegrityError, transaction

from solicitation.decorators import complete_tutorial


@staff_member_required(login_url='solicitation:index')
@login_required
def blog_create(request):
    template_name = 'help_pages/blog_create.html'

    form = BlogForm(
        request.POST or None,        
    )
    if request.method == "POST":
        if form.is_valid():
            data = form.save(commit=False)
            data.AutorBlog = request.user
            data.save()                       
          
            if data.Ativo == False:
                blog = ChamadoBlog.objects.last()
                return redirect('solicitation:index')                  
            else:
                blog = ChamadoBlog.objects.last()
                with transaction.atomic():
                    users = User.objects.filter(is_superuser=0, is_staff=0)
                    for user in users:                     
                        Notification.objects.create(
                        TipoNotificacao_id=9, 
                        from_user=request.user, 
                        to_user=user, to_admin=1, 
                        BlogPost=blog
                        )                
                    return redirect('solicitation:index') 
                        
    context = {       
        'form':form
    }
    return render(request, template_name, context)


@staff_member_required(login_url='solicitation:index')
@login_required
def blog_update(request, SlugBlog):
    template_name = 'help_pages/blog_update.html'
    obj = get_object_or_404(ChamadoBlog, SlugBlog=SlugBlog)
    form = BlogFormUpdate(
        request.POST or None,
        instance=obj        
    )
    if request.method == "POST":
        if form.is_valid():
            data = form.save(commit=False)
            data.AutorBlog = request.user
            data.save()

            if data.Ativo == False:
                blog = ChamadoBlog.objects.get(SlugBlog=SlugBlog)
                return redirect('solicitation:index')                  
            else:
                blog = ChamadoBlog.objects.get(SlugBlog=SlugBlog)
                with transaction.atomic():
                    users = User.objects.filter(is_superuser=0, is_staff=0)
                    for user in users:                     
                        Notification.objects.create(
                        TipoNotificacao_id=12, 
                        from_user=request.user, 
                        to_user=user, to_admin=1, 
                        BlogPost=blog
                        )                
                    return redirect('solicitation:index')                        
    context = {       
        'form':form
    }
    return render(request, template_name, context)

@complete_tutorial
@login_required
def blog_fac(request, *args, **kwargs):
    template_name = 'help_pages/fac.html'
    request_user = request.user
    users_notification = Notification.objects.filter(to_user=request_user, user_has_seen=0, user_has_archive=0).only('id').exists()

    categorias = Categorias.objects.all().filter(TipoBlog=1, Ativo=True).order_by('Importancia')
    query = ChamadoBlog.objects.select_related('CategoriaBlog').filter(
        CategoriaBlog_id__in=categorias, Ativo=True)
    
    resquestid = request.user.id
    completo = VisualizacaoBlog.objects.filter(User_id=resquestid)
    
    context = {
        'categorias': categorias,
        'query': query,
        'completo': completo,
        'users_notification': users_notification,
        
    }
    return render(request, template_name, context, *args, **kwargs)


@complete_tutorial
@login_required
def blog_modelos(request, *args, **kwargs):
    template_name = 'help_pages/solicitation_models.html'
    request_user = request.user
    users_notification = Notification.objects.filter(to_user=request_user, user_has_seen=0, user_has_archive=0).only('id').exists()

    categorias = Categorias.objects.all().filter(TipoBlog=2, Ativo=True).order_by('Importancia')
    query = ChamadoBlog.objects.select_related('CategoriaBlog').filter(
        CategoriaBlog_id__in=categorias, Ativo=True)
    
    resquestid = request.user.id
    completo = VisualizacaoBlog.objects.filter(User_id=resquestid)
    
    context = {
        'categorias': categorias,
        'query': query,
        'completo': completo,
        'users_notification': users_notification,
        
    }
    return render(request, template_name, context)


@login_required
def blog_tutoriais(request, *args, **kwargs):
    template_name = 'help_pages/tutorials.html'
    request_user = request.user
    users_notification = Notification.objects.filter(to_user=request_user, user_has_seen=0, user_has_archive=0).only('id').exists()

    categorias = Categorias.objects.all().filter(TipoBlog=3, Ativo=True).order_by('Importancia')
    query = ChamadoBlog.objects.select_related('CategoriaBlog').filter(
        CategoriaBlog_id__in=categorias, Ativo=True)
    
    resquestid = request.user.id
    completo = VisualizacaoBlog.objects.filter(User_id=resquestid)
    
    context = {
        'categorias': categorias,
        'query': query,
        'completo': completo,
        'users_notification': users_notification,
        
    }
    return render(request, template_name, context)


@login_required
def blog_details(request, id, SlugBlog, *args, **kwargs):
    template_name = 'help_pages/helpers_details.html'
    request_user = request.user
    users_notification = Notification.objects.filter(to_user=request_user, user_has_seen=0, user_has_archive=0).only('id').exists()


    try:        
        notification = Notification.objects.get(pk=id)        
        notification.user_has_seen = True
        notification.save()  
        
        try:    
            details = ChamadoBlog.objects.get(SlugBlog=SlugBlog)     
            try:
                VisualizacaoBlog.objects.create(
                            Post_id=details.id, 
                            User_id=request.user.id, 
                            )
            except IntegrityError:
                pass        
            details.ViewCount = details.ViewCount + 1
            details.save()
            context = {
                'details': details,
                'users_notification': users_notification,
            }
        except ChamadoBlog.DoesNotExist:
            return render(request, template_name='404.html')
        return render(request, template_name, context, *args, **kwargs)

    except Notification.DoesNotExist:      
        try:
            details = ChamadoBlog.objects.get(SlugBlog=SlugBlog)
            try:
                VisualizacaoBlog.objects.create(
                            Post_id=details.id, 
                            User_id=request.user.id, 
                            )
            except IntegrityError:
                pass 

            details.ViewCount = (details.ViewCount + 1)
            details.save()
            pass
            context = {
                'details': details,
                'users_notification': users_notification,
            }
        except ChamadoBlog.DoesNotExist:
            return render(request, template_name='404.html')
        return render(request, template_name, context, *args, **kwargs)


@login_required
def like(request, id, SlugBlog, *args, **kwargs):
    template_name = 'help_pages/partials/like_area.html'
    like = ChamadoBlog.objects.get(id=id)

    if request.method == "POST":
        tipo = like.CategoriaBlog.TipoBlog
        if like.LikesBlog.filter(id=request.user.id).exists():
            like.LikesBlog.remove(request.user)
        else:
            like.LikesBlog.add(request.user)

    categorias = Categorias.objects.all().filter(TipoBlog=tipo, Ativo=True)
    query = ChamadoBlog.objects.select_related('CategoriaBlog').filter(
        CategoriaBlog_id__in=categorias, Ativo=True)
    
    resquestid = request.user.id
    completo = VisualizacaoBlog.objects.filter(User_id=resquestid)
    context = {
        'query': query,
        'completo': completo,
    }
    return render(request, template_name, context)


@login_required
def like_details(request, id, SlugBlog, *args, **kwargs):
    template_name = 'help_pages/partials/_like_details.html'
    like = ChamadoBlog.objects.get(id=id)

    if request.method == "POST":
        tipo = like.CategoriaBlog.TipoBlog
        if like.LikesBlog.filter(id=request.user.id).exists():
            like.LikesBlog.remove(request.user)
        else:
            like.LikesBlog.add(request.user)

   
    context = {
        'details': like
    }
    return render(request, template_name, context)



class BlogNotification(View):
    def get(self, request, notification_pk, id, SlugBlog, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
     
        notification.user_has_seen = True
        notification.save()

        return redirect('solicitation:datails_requests', id=id)


