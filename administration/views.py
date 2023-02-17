# from datetime import datetime
from base64 import b64encode
from django.http import HttpResponseRedirect
from django.utils import timezone
from zeep import Client
from accounts.models import LoginAudit
from administration.models import RespostasProntas
from notifications.models import Notification

from django.contrib import messages
from django.contrib.auth.models import User

from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from solicitation.forms import (
    RespostaSolicitacaoForm,
    RespostaUsuarioForm,
    SerResponsavelForm,
)

from solicitation.models import (
    ChamadoBackup,
    RespostaSolicitacao,
    RespostaUsuario,
    Solicitacoes
)


@staff_member_required(login_url='solicitation:index')
@login_required
def admin_list_request(request):
    template_name = 'administration/admin_list_requests.html'
    chamados = Solicitacoes.objects.only('id').filter(StatusAtual__in=(1, 5))

    context = {
        'chamados': chamados,
    }
    return render(request, template_name, context)

@staff_member_required(login_url='solicitation:index')
@login_required
def admin_list_analyse_request(request):
    template_name = 'administration/admin_list_requests.html'
    chamados = Solicitacoes.objects.only('id').filter(StatusAtual=2)

    context = {
        'chamados': chamados,
    }
    return render(request, template_name, context)

@staff_member_required(login_url='solicitation:index')
@login_required
def admin_list_finished_request(request):
    template_name = 'administration/admin_list_requests.html'
    chamados = Solicitacoes.objects.only('id').filter(StatusAtual__in=(3, 4))

    context = {
        'chamados': chamados,
    }
    return render(request, template_name, context)

@staff_member_required(login_url='solicitation:index')
@login_required
def admin_list_chamados_antigos(request):
    template_name = 'administration/admin_list_chamados_antigos.html'
    
    chamado_list = ChamadoBackup.objects.values(
        'id',
        'nome',
        're_ch',
        'unidade',
        'data_sol',
        'data_res',
        'PM_res',
        'situacao',
    ).all().order_by('-id')
    
    context = {
        'chamados': chamado_list,
    }
    return render(request, template_name, context)

@staff_member_required(login_url='solicitation:index')
@login_required
def admin_details_chamados_antigos(request, id):
    template_name = 'administration/admin_details_chamados_antigos.html'

    details = ChamadoBackup.objects.get(id=id)
    context = {
        'details': details,
    }
    return render(request, template_name, context)

@staff_member_required(login_url='solicitation:index')
def admin_list_login_audit(request):
    template_name = 'administration/admin_list_login_audit.html'
    
    login_list = LoginAudit.objects.all().order_by('-id')
    
    context = {
        'logins': login_list,
    }
    return render(request, template_name, context)

@staff_member_required(login_url='solicitation:index')
@login_required
def admin_update_request(request, id):    
    template_name = 'administration/admin_update_request.html'
    obj = get_object_or_404(Solicitacoes, id=id)           
    
    # Pega o Usuário solicitante para poder mandar a notificação.
    cpf = obj.CpfSolicitante
    usuario_solicitante = User.objects.get(username=cpf)

    form = SerResponsavelForm(request.POST or None, instance=obj)
    if request.method == "POST" and 'responsavel' in request.POST:
        if form.is_valid():
            add_status = form.save(commit=False)
            add_status.Responsavel_id = request.user.id
            add_status.StatusAtual_id = 2
            add_status.save()
            # Cria a notificação para o Usuário
            Notification.objects.create(
            TipoNotificacao_id=2, from_user=request.user, to_user=usuario_solicitante, Solicitacao_id=id)
            # Cria a Mensagem de Sucesso
            messages.success(
                            request,
                            f'Agora você é responsável pelo Chamado N° - {obj.id}'
                        )
        return redirect('administration:admin_update_request', id=id)

    if request.method == "POST" and 'pendencia' in request.POST:
        if form.is_valid():
            add_status = form.save(commit=False)
            add_status.Responsavel_id = None
            add_status.StatusAtual_id = 1
            add_status.save()

            Notification.objects.create(
            TipoNotificacao_id=3, from_user=request.user, to_user=usuario_solicitante, Solicitacao_id=id)
           
            messages.warning(
                            request,
                            f'Você colocou o chamado N° - {obj.id} na Pendência.',                            
                        )
        return redirect('administration:admin_update_request', id=id)

    if request.method == "POST" and 'fechar' in request.POST:
        if form.is_valid():
            add_status = form.save(commit=False)
            add_status.Responsavel_id = request.user.id
            add_status.StatusAtual_id = 4
            # add_status.DataDoEncerramento = datetime.now()            
            add_status.save()

            Notification.objects.create(
            TipoNotificacao_id=4, from_user=request.user, to_user=usuario_solicitante, Solicitacao_id=id)
            messages.info(
                            request,
                            f'O Chamado N° - {obj.id} Foi marcado como FECHADO!',                            
                        )
        return redirect('administration:admin_update_request', id=id)

    if request.method == "POST" and 'resolvidoo' in request.POST:
        if form.is_valid():
            add_status = form.save(commit=False)
            add_status.Responsavel_id = request.user.id
            add_status.StatusAtual_id = 3
            add_status.save()

            Notification.objects.create(
            TipoNotificacao_id=5, from_user=request.user, to_user=usuario_solicitante, Solicitacao_id=id)
            messages.success(
                            request,
                            f'O Chamado N° - {obj.id} Foi marcado como RESOLVIDO!',                            
                        )
        return redirect('administration:admin_update_request', id=id)
       

    if request.method == "POST" and 'reabrir' in request.POST:
        if form.is_valid():
            add_status = form.save(commit=False)
            add_status.Responsavel_id = request.user.id
            add_status.StatusAtual_id = 5
            add_status.save()
            
            Notification.objects.create(
            TipoNotificacao_id=6, from_user=request.user, to_user=usuario_solicitante, Solicitacao_id=id)
            messages.info(
                            request,
                            f'O Chamado N° - {obj.id} Foi marcado como REABERTO!',                            
                        )
        return redirect('administration:admin_update_request', id=id)

    his = Solicitacoes.Historico.all().filter(id=id).order_by('history_date')

    form_resposta = RespostaSolicitacaoForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and 'resolver' in request.POST:        
        
        if form_resposta.is_valid():
            add_resposta = form_resposta.save(commit=False)
            add_resposta.RespostaResponsavel_id = request.user.id
            add_resposta.Solicitacao_id = id            
            add_resposta.save()
            
            resposta = RespostaSolicitacao.objects.last().id 
            Notification.objects.create(
            TipoNotificacao_id=7, from_user=request.user, to_user=usuario_solicitante, to_admin=1, Solicitacao_id=id, RespostaAdmin_id=resposta)
            messages.success(
                            request,
                            f'Resposta Enviada!',                            
                        )            
            Solicitacoes.objects.filter(id=id).update(DataDoEncerramento = timezone.now())            
    
    respostas = RespostaSolicitacao.objects.filter(
        Solicitacao=id).order_by('RespostaData')

    respostaresponsavel = None
    try:
        respostaresponsavel = RespostaSolicitacao.objects.get(Solicitacao=id)
    except:
        respostaresponsavel
    try:
        notificationid = Notification.objects.get(TipoNotificacao_id=7, Solicitacao_id=id)
        getrespostaid = notificationid.RespostaAdmin_id
        visualizou_a_resposta = Notification.objects.get(TipoNotificacao_id=7, RespostaAdmin_id=getrespostaid)
        verificaresposta = RespostaSolicitacao.objects.get(
        Solicitacao_id=id).id
    except:
        visualizou_a_resposta = None
        verificaresposta = None

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
            
            if request.user.is_staff:
                Notification.objects.create(
                TipoNotificacao_id=8, from_user=responsavel, to_user=solicitante_user, to_admin=1, Solicitacao_id=id, RespostaUser_id=resposta)
                messages.success(
                            request,
                            f'Resposta Enviada!',                            
                        )
    respostasUsuarios = RespostaUsuario.objects.all()
    ultimostatus = obj.StatusAtual

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

    prontas = RespostasProntas.objects.all() 

    context = {
        'details': obj,
        'historico': his,
        'respostas': respostas,
        'respostaresponsavel': respostaresponsavel,
        'form_resposta': form_resposta,
        'form_resposta_user': form_resposta_user,
        'respostasUsuarios': respostasUsuarios,
        'ultimostatus': ultimostatus,
        'tempo_atendimento': tempo_atendimento,
        'prontas': prontas,
        'visualizou_a_resposta': visualizou_a_resposta,
        'verificaresposta': verificaresposta,
        'dia': dias,
        'hora': horas,
        'minuto': minutos,
        'segundo': tempo_atendimento,
    }
    return render(request, template_name, context)

@staff_member_required(login_url='solicitation:index')
@login_required
def navbar_search(request):
    template_name_full = 'administration/partials/_search_results_full.html'
    template_name = 'administration/partials/_search_results.html'
    
    full_search = request.GET.get('query')

    if full_search.isdigit() and len(full_search) > 5:
        client = Client(
            'http://sistemas.intranet.policiamilitar.sp.gov.br/WSSCPM/Service.asmx?WSDL')

        try:
            busca = client.service.procuraPMPorRE(full_search)
            foto = client.service.procuraFotoPorRE(full_search)

            nomeguerra = busca.nomeGuePM.strip(
            )
            posto = busca.codigoPostoGraduacaoPM.descricaoPostoGraduacaoPM.strip()
            postoo  = posto.strip()
            re = busca.Documentos.FuncionarioDocumento[0].RE
            cpf = busca.Documentos.FuncionarioDocumento[0].Numero
            dig = busca.Documentos.FuncionarioDocumento[0].DigitoDocumento
            opmcod = busca.codigoOPMAtualPM.codigoOPM
            opmco1 = busca.codigoOPMAtualPM.descricaoNivel02OPMCPA.strip(
            )
            opmco2 = busca.codigoOPMAtualPM.descricaoNivel03OPMBatalhao.strip(
            )
            opmco3 = busca.codigoOPMAtualPM.descricaoNivel04OPMCIA.strip(
            )
            opmco4 = busca.codigoOPMAtualPM.descricaoNivel05OPMGrupamento.strip(
            )
            opmco5 = busca.codigoOPMAtualPM.descricaoNivel06OPMPelotao.strip(
            )
            emailpm = busca.dadosContatoFuncionario.FuncionarioContato[0].emailContato

            funcao = busca.funcoesPM.Funcao
            for funcao_principal in funcao:
                if funcao_principal.Principal == 'S':
                    funcao = request.session['funcao'] = funcao_principal.descricaoFuncaoPM

            try:
                decoded = b64encode(foto).decode('ascii')
            except TypeError:
                decoded = None

            jsonresponse = {
            'nomeguerra': nomeguerra, 'postoo': postoo, 're': re, 'cpf': cpf,
            'dig': dig, 'opmcod': opmcod, 'opmco1': opmco1, 'opmco2': opmco2,
            'opmco3': opmco3, 'opmco4': opmco4, 'opmco5': opmco5, 'emailpm': emailpm,
            'foto': decoded, 'funcao': funcao
            }

            chamado_results = Solicitacoes.objects.filter(
            ReSolicitante__icontains=full_search
            ).select_related('Responsavel')

            total = chamado_results.count()
            totalpluspolicia = total + 1
            
            if chamado_results:
                full_search = full_search

            context = {
                'full_search':full_search,
                'jsonresponse':jsonresponse,
                'chamado_results':chamado_results,
                'total':total,
                'totalpluspolicia':totalpluspolicia,
            }
            return render(request, template_name_full, context)    
        except AttributeError: 
            messages.error(
                    request, f'RE {full_search} não Encontrado!'                         
                    )
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        chamado_results = Solicitacoes.objects.filter(
            TituloDaSolicitacao__icontains=full_search
            ).select_related('Responsavel')

        total = chamado_results.count()

        context = {
            'chamado_results':chamado_results, 
            'full_search':full_search,
            'total':total
            }


        return render(request, template_name, context) 