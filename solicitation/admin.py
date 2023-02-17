from re import search
from django.contrib import admin
from solicitation.models import AssuntoSolicitacao, CategoriaSolicitacao, ChamadoBackup, DestinoSolicitacao, RespostaSolicitacao, RespostaUsuario, Solicitacoes, StatusSolicitacao

@admin.register(Solicitacoes)
class SolicitacoesAdmin(admin.ModelAdmin):
    model = Solicitacoes
    list_display = [
        'PostoGradSolicitante', 'ReSolicitante', 'NomeGuerraSolicitante',
        'UnidadeSolicitante', 'StatusAtual', 'ReSolicitante',
        'DataDaSolicitacao', 'Responsavel',
        ]  
   
    list_filter = ['CategoriaDaSolicitacao', 'UnidadeSolicitante']
class CategoriaInline(admin.TabularInline):
    model = AssuntoSolicitacao
@admin.register(CategoriaSolicitacao)
class CategoriaAdmin(admin.ModelAdmin):
    model = CategoriaSolicitacao
    list_display = [
        'Categoria',
        ]  
   
    list_filter = ['Categoria',]
    inlines = [CategoriaInline] 


@admin.register(AssuntoSolicitacao)
class AssuntoSolicitacaoAdmin(admin.ModelAdmin):
    model = AssuntoSolicitacao
    list_display = [
        'Assunto',
        ]
    
   
    list_filter = ['Assunto',]


@admin.register(DestinoSolicitacao)
class DestinoSolicitacaoAdmin(admin.ModelAdmin):
    model = DestinoSolicitacao
    list_display = [
        'SecaoOPMCOD',
        ]  
   
    list_filter = ['SecaoOPMCOD',]


@admin.register(StatusSolicitacao)
class DestinoSolicitacaoAdmin(admin.ModelAdmin):
    model = StatusSolicitacao
    list_display = [
        'Status',
        'ClassStatus'
        ]  


@admin.register(ChamadoBackup)
class ChamadoBackupAdmin(admin.ModelAdmin):
    model = ChamadoBackup
    list_display = [
        'id', 'nome', 'unidade',
        'problema', 'data_sol', 'data_res', 'PM_res', 'situacao',
    ]

    search_fields = ['id','unidade']
    list_filter = ['situacao', 'unidade']


admin.site.register(RespostaSolicitacao)
admin.site.register(RespostaUsuario)