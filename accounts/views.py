from base64 import b64encode
from xml.etree import ElementTree

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views import View
from notifications.models import Notification
from requests.sessions import Session
from utils.validacpf import valida_cpf
from zeep.client import Client
from zeep.transports import Transport

from accounts.models import LoginAudit
from accounts.xml_to_dict import XmlDictConfig


def user_authentication(request):
    _msSis = 'PROTOCOLO'
    _msSubSis = 'PROTOCOLO'
    _cpf = ''
    _sen = ''
    _fun_tip = 'M'
    URL = 'http://sistemas.intranet.policiamilitar.sp.gov.br/MS/aws_permxml.aspx?WSDL'

    if request.method == 'POST' and 'btnauth' in request.POST:
        import re
        _cpf = request.POST.get('username')
        _cpf = valida_cpf(_cpf)
        _sen = request.POST.get('password')

        try:
            session = Session()
            session.proxies = {
                'http': 'http://proxy.policiamilitar.sp.gov.br:3128',
                'https': 'http://proxy.policiamilitar.sp.gov.br:3128',
            }

            transport = Transport(session=session)
            client = Client(URL, transport=transport)

            response = client.service.Execute(
                _msSis, _msSubSis, _cpf, _fun_tip, _sen
            )

            root = ElementTree.XML(response)
            xmldict = XmlDictConfig(root)
            status = xmldict['{MSU_Oficial}Status']
            opm = xmldict['{MSU_Oficial}OPM']

            if status == '0' and opm != 0:

                client = Client(
                    'http://sistemas.intranet.policiamilitar.sp.gov.br/WSSCPM/Service.asmx?WSDL')
                busca = client.service.procuraPMPorCPF(_cpf)               

                nomeguerra = request.session['nomeguerra'] = busca.nomeGuePM.strip(
                )
                posto = busca.codigoPostoGraduacaoPM.descricaoPostoGraduacaoPM.strip()
                postoo = request.session['postoo'] = posto.strip()
                re = request.session['re'] = busca.Documentos.FuncionarioDocumento[0].RE
                fotoencoded = client.service.procuraFotoPorRE(re)
                request.session['fotodecoded'] = b64encode(fotoencoded).decode('ascii')
                cpf = request.session['cpf'] = busca.Documentos.FuncionarioDocumento[0].Numero
                dig = request.session['dig'] = busca.Documentos.FuncionarioDocumento[0].DigitoDocumento
                opmcod = request.session['opmcod'] = busca.codigoOPMAtualPM.codigoOPM
                opmco1 = request.session['opmco1'] = busca.codigoOPMAtualPM.descricaoNivel02OPMCPA.strip(
                )
                opmco2 = request.session['opmco2'] = busca.codigoOPMAtualPM.descricaoNivel03OPMBatalhao.strip(
                )
                opmco3 = request.session['opmco3'] = busca.codigoOPMAtualPM.descricaoNivel04OPMCIA.strip(
                )
                opmco4 = request.session['opmco4'] = busca.codigoOPMAtualPM.descricaoNivel05OPMGrupamento.strip(
                )
                opmco5 = request.session['opmco5'] = busca.codigoOPMAtualPM.descricaoNivel06OPMPelotao.strip(
                )
                emailpm = request.session['email'] = busca.dadosContatoFuncionario.FuncionarioContato[0].emailContato

                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[-1].strip()
                    ip_usuario = ip                    
                else:
                    ip = request.META.get('REMOTE_ADDR')
                    ip_usuario = ip
                

                funcao = busca.funcoesPM.Funcao
                for funcao_principal in funcao:
                    if funcao_principal.Principal == 'S':
                        funcao = request.session['funcao'] = funcao_principal.descricaoFuncaoPM

                if request.method == 'POST' and nomeguerra and cpf != '':
                    log = LoginAudit(
                        NomeDeGuerra=nomeguerra,
                        CpfDoUsuario=cpf+dig,
                        PostoGraduacao=postoo,
                        ReUsuario=re,
                        OpmCod=opmcod,
                        OpmCod1=opmco1,
                        OpmCod2=opmco2,
                        OpmCod3=opmco3,
                        OpmCod4=opmco4,
                        OpmCod5=opmco5,
                        IpDoUsuario=ip_usuario
                    )
                    log.save()

                    if request.method == 'POST':
                        import re
                        username = request.POST.get('username')
                        username = valida_cpf(username)
                        password = request.POST.get('password')
                        email = emailpm

                        user = User.objects.filter(username=username).exists()
                        if user:
                            alterpass = User.objects.get(username=username)
                            alterpass.first_name = postoo
                            alterpass.last_name = nomeguerra
                            alterpass.set_password(password)
                            alterpass.save()
                            
                            user = authenticate(
                                username=username, password=password)
                            login(request, user)

                            messages.success(
                                request,
                                f'OLÁ {postoo} {nomeguerra}'
                            )
                            return redirect('solicitation:index')

                        else:
                            user = User.objects.create(
                                username=username,
                                password=password,
                                first_name=postoo,
                                last_name=nomeguerra,
                                email=email
                            )
                            user.set_password(user.password)
                            user.save()
                            user = authenticate(
                                username=username, password=password)
                            messages.success(
                                request,
                                f'OLÁ {postoo} {nomeguerra}'
                            )
                            login(request, user)                        

                            for staff in User.objects.filter(is_staff=True):            
                                Notification.objects.create(
                                    TipoNotificacao_id=11, from_user=request.user, to_user_id=staff.id, to_admin=1, NovoUser=user)

                        return redirect('solicitation:index')

                    return render(request, 'accounts/login2.html')
                    
            elif status == '2' or status == '3':
                messages.error(
                    request,
                    'CREDENCIAIS INVÁLIDAS'
                )
        except:
            messages.error(
                request,
                'Verifique suas Configurações de PROXY!'
             )
    return render(request, 'accounts/login2.html')

class UserNotification(View):
    def get(self, request, notification_pk, id, *args, **kwargs):        
        
        notification = Notification.objects.get(pk=notification_pk)
        user_id = request.user.id

        notification.user_has_seen = True
        notification.save()

        return redirect('notifications:list_notifications')


def user_logout(request):
    logout(request)
    return render(request, 'accounts/logout.html')


def lock_screen(request):
    return render(request, 'accounts/lock-screen.html')


