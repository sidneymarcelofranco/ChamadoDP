from django import template
from accounts.models import LoginAudit
from help_pages.models import ChamadoBlog

from django.db.models import Sum

from solicitation.models import ChamadoBackup, Solicitacoes
from django.contrib.auth.models import User

register = template.Library()

@register.inclusion_tag('administration/partials/_counters.html')
def admin_counters():
    chamadostotal = Solicitacoes.objects.all().count()
    usuarios = User.objects.all()
    analise = Solicitacoes.objects.filter(StatusAtual=2)
    resolvidos = Solicitacoes.objects.filter(StatusAtual__in=(3, 4))
    pendentes = Solicitacoes.objects.filter(StatusAtual__in=(1, 5))
    views = ChamadoBlog.objects.aggregate(Sum('ViewCount'))
    contagemdeviews = views['ViewCount__sum']
    likes = ChamadoBlog.LikesBlog.through.objects.count()
    acessos = LoginAudit.objects.all().count()
    chamadostotalbkup = ChamadoBackup.objects.all().count()

    fullcount = chamadostotalbkup + chamadostotal


    context = {
        'chamadostotal': chamadostotal,
        'analise': analise,
        'resolvidos': resolvidos,
        'pendentes': pendentes,
        'usuarios': usuarios,
        'likes': likes,
        'acessos': acessos,
        'chamadostotalbkup': chamadostotalbkup,
        'fullcount': fullcount,
        'views': contagemdeviews,
    }
    return context
