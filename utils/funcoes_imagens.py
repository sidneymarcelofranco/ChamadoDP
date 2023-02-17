# pega o caminho das imagens de profile e concatena com o ID do usuário para
# fazer um caminho único para cada usuário

# def upload_documentos(self, filename):
#     return f'/{self.GrandeComandoSolicitante}/{self.UnidadeSolicitante}/{self.ReSolicitante}'


from datetime import datetime


def upload_documentos(self, filename):
        # extension se quiser pegar a EXTENSÃO PURA DO ARQUIVO
        # extension = os.path.splitext(filename)[-1]
        today = datetime.now()
        upload_day = today.strftime("ANO-%Y/MES-%m/DIA-%d")
        return f'Documentos/{self.GrandeComandoSolicitante}/{self.UnidadeSolicitante}/RE-{self.ReSolicitante}/{upload_day}/{filename}'


def upload_documentos_resposta(self, filename):
        # extension se quiser pegar a EXTENSÃO PURA DO ARQUIVO
        # extension = os.path.splitext(filename)[-1]
        return f'Respostas/Anexos/Responsavel-{self.RespostaResponsavel}/Chamado-N-{self.Solicitacao.id}-{filename}'

# def imagem_profile_padrao():
#     return 'default/ProfilePadrao.png'


# def caminho_capa_profile(self, filename):
#     return f'capas/{self.user.id}/{"capa_profile.png"}'


# def capa_profile_padrao():
#     return 'default/capaPadrao.png'

# def caminho_img_orgsuperior(self, filename):
#     return f'brasoes/grandecomando/brasao{self.sluggrandecomando}.png'

# def imagem_brasao_padrao():
#     return 'default/Brasaopadrao.png'