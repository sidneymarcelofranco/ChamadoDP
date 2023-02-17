from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from help_pages.models import ChamadoBlog
from notifications.models import Notification

from solicitation.decorators import complete_tutorial
from solicitation.forms import (RespostaUsuarioForm, SerResponsavelForm,
                                SolicitacoesForm, SolicitacoesUpdateForm)
from solicitation.models import (RespostaSolicitacao, RespostaUsuario,
                                 Solicitacoes)


@login_required
def index(request):
    template_name = 'solicitation/index.html'
    re = request.session['re']

    dashboard = Solicitacoes.objects.only('id').filter(
        ReSolicitante=re).aggregate(
        analise=Count('id', Q(StatusAtual=2)),
        resolvidos=Count('id', Q(StatusAtual__in=(3, 4))),
        pendentes=Count('id', Q(StatusAtual__in=(1, 5)))
    )

    admindash = Solicitacoes.objects.only('id').all().aggregate(
        analise=Count('id', Q(StatusAtual=2)),
        resolvidos=Count('id', Q(StatusAtual__in=(3, 4))),
        pendentes=Count('id', Q(StatusAtual__in=(1, 5)))
    )
  
    request_user = request.user
    users_notification = Notification.objects.filter(to_user=request_user, user_has_seen=0, user_has_archive=0).only('id').exists()   

    context = {          
        #USER SECTION
        'dashboard': dashboard,
        'admindash': admindash,
        'users_notification': users_notification
    }
    return render(request, template_name, context)

@login_required
def make_request(request):
    template_name = 'solicitation/make_request.html'
    
    request_user = request.user
    users_notification = Notification.objects.filter(to_user=request_user, user_has_seen=0, user_has_archive=0).only('id').exists() 

    form = SolicitacoesForm(
        request.POST or None,
        request.FILES or None
    )
    if request.method == "POST":
        if form.is_valid():
            data = form.save(commit=False)
            data.PostoGradSolicitante = request.POST.get('nposto')
            data.ReSolicitante = request.POST['nre']
            data.NomeGuerraSolicitante = request.POST['nnomeguerra']
            data.CpfSolicitante = request.POST['ncpf']
            data.FuncaoSolicitante = request.POST['nfuncao']
            data.CodOpmSolicitante = request.POST['nopmcod']
            data.GrandeComandoSolicitante = request.POST['nopmcod1']
            data.UnidadeSolicitante = request.POST['nopmcod2']
            data.DepartamentoSolicitante = request.POST['nopmcod3']
            data.DivisaoSolicitante = request.POST['nopmcod4']
            data.SecaoSolicitante = request.POST['nopmcod5']
            data.save()

            for user in User.objects.filter(is_staff=True):            
                Notification.objects.create(
                    TipoNotificacao_id=1, from_user=request.user, to_user_id=user.id, to_admin=1, Solicitacao_id=data.id)                

            messages.success(
                request,
                f'Solicitação realizada com sucesso'
            )
        return redirect('solicitation:user_list_request')

    context = {
        'form': form,
        'users_notification': users_notification,
    }
    return render(request, template_name, context)

@login_required
def details_request(request, id):
    template_name = 'solicitation/details_request.html'

    request_user = request.user
    users_notification = Notification.objects.filter(to_user=request_user, user_has_seen=0, user_has_archive=0).only('id').exists() 

    username = request.user.username
    obj = Solicitacoes.objects.get(id=id)
    his = Solicitacoes.Historico.all().filter(id=id).order_by('history_date')

    if obj.DataDoEncerramento == None:
        tempo_atendimento = '24 Horas'
    else:
        tempo_atendimento = obj.DataDoEncerramento - obj.DataDaSolicitacao
        tempo_atendimento = str(tempo_atendimento).split(".")[0]

    respostas = RespostaSolicitacao.objects.select_related(
        'RespostaResponsavel').select_related(
            'Solicitacao').filter(
        Solicitacao=obj.id).order_by('RespostaData')


    respostasUsuarios = RespostaUsuario.objects.all().select_related(
        'RespostaUsuarioResponsavel').select_related(
            'RespostaDaSolicitacao')

    if request.user.is_authenticated and username != obj.CpfSolicitante:
        return redirect('solicitation:user_list_request')

    form_resposta_user = RespostaUsuarioForm(request.POST or None)
    if request.method == "POST" and 'resposta_user' in request.POST:
        resposta_user_id = int(request.POST.get('resposta_id'))
        respostaSolicitacaoid = RespostaSolicitacao.objects.get(
            id=resposta_user_id)

        if form_resposta_user.is_valid():
            add_resposta_user = form_resposta_user.save(commit=False)
            add_resposta_user.RespostaUsuarioResponsavel_id = request.user.id
            add_resposta_user.RespostaDaSolicitacao_id = respostaSolicitacaoid.id
            add_resposta_user.save()

            solicitante = obj.CpfSolicitante
            solicitante_user = User.objects.get(username=solicitante)
            resposta = RespostaUsuario.objects.last().id    
            responsavel = obj.Responsavel  
            
            Notification.objects.create(
            TipoNotificacao_id=8, from_user=solicitante_user, to_user=responsavel, to_admin=1, Solicitacao_id=id, RespostaUser_id=resposta)

            return redirect('solicitation:datails_requests', id=id)

    form = SerResponsavelForm(request.POST or None, instance=obj)
    if request.method == "POST" and 'resolvidoo' in request.POST:
        if form.is_valid():
            add_status = form.save(commit=False)
            add_status.Responsavel_id = request.user.id
            add_status.StatusAtual_id = 3
            add_status.save()

            solicitacao = Solicitacoes.objects.first().id

            for user in User.objects.filter(is_staff=True):            
                Notification.objects.create(
                    TipoNotificacao_id=10, from_user=request.user, to_user_id=user.id, to_admin=1, Solicitacao_id=solicitacao)            
            
        return redirect('solicitation:datails_requests', id=id)

    try:
        notificationid = Notification.objects.get(TipoNotificacao_id=7, Solicitacao_id=id)
        getrespostaid = notificationid.RespostaAdmin_id
        visualizou_a_resposta = Notification.objects.get(TipoNotificacao_id=7, RespostaAdmin_id=getrespostaid)
        verificaresposta = RespostaSolicitacao.objects.get(
        Solicitacao_id=id).id 
    except:
        visualizou_a_resposta = None
        verificaresposta = None

    ultimostatus = obj.StatusAtual

    ultres = None
    testeultres = RespostaSolicitacao.objects.only('id').filter(Solicitacao=obj.id).exists()
    if testeultres == False:
        ultres = False
    else:
        ultres = RespostaSolicitacao.objects.filter(
            Solicitacao=obj.id).order_by("-id")[0]

    re = request.session['re']
    dashboard = Solicitacoes.objects.only('id').filter(
        ReSolicitante=re).aggregate(
        analise=Count('id', Q(StatusAtual=2)),
        resolvidos=Count('id', Q(StatusAtual__in=(3, 4))),
        pendentes=Count('id', Q(StatusAtual__in=(1, 5)))
    )

    respostaresponsavel = None
    try:
        respostaresponsavel = RespostaSolicitacao.objects.get(Solicitacao=id)
    except:
        respostaresponsavel


    if obj.DataDoEncerramento == None:
        tempo_atendimento = '24 Horas'
        dias = 0
        horas = 0
        minutos = 0
    else:
        tempo_atendimento = obj.DataDoEncerramento - obj.DataDaSolicitacao
        tempo_atendimento = tempo_atendimento.seconds 
        dias, tempo_atendimento = divmod(tempo_atendimento, 86400)
        horas, tempo_atendimento = divmod(tempo_atendimento, 3600)
        minutos, tempo_atendimento = divmod(tempo_atendimento, 60)

    context = {
        'details': obj,
        'historico': his,
        'respostas': respostas,
        'respostaresponsavel': respostaresponsavel,
        'form_resposta_user': form_resposta_user,
        'respostasUsuarios': respostasUsuarios,
        'tempo_atendimento': tempo_atendimento,
        'ultimostatus': ultimostatus,
        'visualizou_a_resposta': visualizou_a_resposta,
        'verificaresposta': verificaresposta,
        'dia': dias,
        'hora': horas,
        'minuto': minutos,
        'segundo': tempo_atendimento,    
        'users_notification': users_notification,    

        'ultres': ultres,
        # DASH
        'dashboard': dashboard,


    }
    return render(request, template_name, context)

@login_required
def update_request(request, id):
    template_name = 'solicitation/update_request.html'
    obj = get_object_or_404(Solicitacoes, id=id)

    request_user = request.user
    users_notification = Notification.objects.filter(to_user=request_user, user_has_seen=0, user_has_archive=0).only('id').exists() 

    username = request.user.username

    if request.user.is_authenticated and username != obj.CpfSolicitante:
        return redirect('solicitation:user_list_request')

    form = SolicitacoesUpdateForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        add_user = form.save(commit=False)
        add_user.usuario_id = request.user.id
        add_user.save()

        return redirect('solicitation:user_list_request')

    context = {
        'form': form,
        'users_notification': users_notification,
    }
    return render(request, template_name, context)

@login_required
def user_list_request(request):
    template_name = 'solicitation/user_list_requests.html'

    request_user = request.user
    users_notification = Notification.objects.filter(to_user=request_user, user_has_seen=0, user_has_archive=0).only('id').exists() 

    re = request.session['re']

    chamados = Solicitacoes.objects.filter(
        ReSolicitante=re).only(
            'TituloDaSolicitacao', 'CategoriaDaSolicitacao',
            'DataDaSolicitacao', 'StatusAtual')
   
    dashboard = Solicitacoes.objects.only('id').filter(
        ReSolicitante=re).aggregate(
        analise=Count('id', Q(StatusAtual=2)),
        resolvidos=Count('id', Q(StatusAtual__in=(3, 4))),
        pendentes=Count('id', Q(StatusAtual__in=(1, 5)))
    )

    context = {
        'chamados': chamados,
        'dashboard': dashboard,        
        'users_notification': users_notification,
    }
    return render(request, template_name, context)
