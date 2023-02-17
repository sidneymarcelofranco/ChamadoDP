import math
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import CharField
from django.urls import reverse

from django.utils import timezone

from ckeditor_uploader.fields import RichTextUploadingField

from simple_history.models import HistoricalRecords

from utils.funcoes_imagens import upload_documentos, upload_documentos_resposta

class StatusSolicitacao(models.Model):
    Status = CharField(
        'Status da Solicitação',
        max_length=100,
        null=True, blank=True
    )

    ClassStatus = CharField(
        'Class',
        max_length=20,
        null=True, blank=True
    )

    class Meta:
        verbose_name = ('Status das Solicitações')

    def __str__(self):
        return self.Status


class CategoriaSolicitacao(models.Model):
    Categoria = CharField(
        'Categoria',
        max_length=100,
        null=True, blank=True
    )

    class Meta:
        verbose_name = ('Categorias de Solicitações')

    def __str__(self):
        return self.Categoria


class AssuntoSolicitacao(models.Model):
    Categoria_Fk = models.ForeignKey(
        CategoriaSolicitacao, 
        on_delete=models.DO_NOTHING
        )

    Assunto = CharField(
        'Assunto',
        max_length=100,
        null=True, blank=True
    )

    class Meta:
        verbose_name = ('Assuntos das Solicitações')

    def __str__(self):
        return self.Assunto


class DestinoSolicitacao(models.Model):
    SecaoOPMCOD = CharField(
        'Código da Seção',
        max_length=100,
        null=True, blank=True
    )


    class Meta:
        verbose_name = ('Destinos das Solicitações')

    def __str__(self):
        return self.SecaoOPMCOD
        

class Solicitacoes(models.Model):
    PostoGradSolicitante = models.CharField(
        'Posto / Grad',
        max_length=100,
        null=True, blank=True
    )

    ReSolicitante = models.CharField(
        'Re',
        max_length=100,
        null=True, blank=True
    )

    NomeGuerraSolicitante = models.CharField(
        'Nome de Guerra',
        max_length=100,
        null=True, blank=True
    )

    CpfSolicitante = models.CharField(
        'CPF',
        max_length=100,
        null=True, blank=True
    )

    FuncaoSolicitante = models.CharField(
        'Função',
        max_length=100,
        null=True, blank=True
    )

    CodOpmSolicitante = models.CharField(
        'Opm Cod',
        max_length=10,
        null=True, blank=True
    )

    GrandeComandoSolicitante = models.CharField(
        'Grande Comando',
        max_length=50,
        null=True, blank=True
    )

    UnidadeSolicitante = models.CharField(
        'Unidade',
        max_length=50,
        null=True, blank=True
    )

    DepartamentoSolicitante = models.CharField(
        'Unidade',
        max_length=50,
        null=True, blank=True
    )

    DivisaoSolicitante = models.CharField(
        'Unidade',
        max_length=50,
        null=True, blank=True
    )

    SecaoSolicitante = models.CharField(
        'Unidade',
        max_length=50,
        null=True, blank=True
    )

    StatusAtual = models.ForeignKey(
        StatusSolicitacao,
        verbose_name='Status Atual',
        default=1,
        related_name='status_solicitacao',
        on_delete=models.DO_NOTHING,
        null=True, blank=True
    )

    DestinoDaSolicitacao = models.ForeignKey(
        DestinoSolicitacao,
        verbose_name='Destino',
        on_delete=models.DO_NOTHING,
        null=True, blank=True
    )

    TituloDaSolicitacao = models.CharField(
        'Titulo da Solicitação',
        max_length=150,
        null=True, blank=True        
    )

    CategoriaDaSolicitacao = models.ForeignKey(
        CategoriaSolicitacao,
        verbose_name='Categoria',
        on_delete=models.DO_NOTHING,
        null=True, blank=True
    )

    AssuntoDaSolicitacao = models.ForeignKey(
        AssuntoSolicitacao,
        verbose_name='Assunto',
        on_delete=models.DO_NOTHING,
        null=True, blank=True
    )

    DataDaSolicitacao = models.DateTimeField(
        'Criado em:',
        auto_now_add=True,
        auto_now=False,
        null=True, blank=True
    )

    DataDoEncerramento = models.DateTimeField(
        'Criado em:',
        null=True, blank=True
    )

    DescricaoDoChamado = RichTextUploadingField(
        'Descrição do Chamado',
        null=True, blank=True
    )

    ConfirmacaoDeSolicitacao = models.BooleanField(
        default=False,
        null=True, blank=True
    )

    Responsavel = models.ForeignKey(
        User,
        related_name='+',
        verbose_name='Policial Responsável',
        on_delete=models.DO_NOTHING,
        null=True, blank=True
    )

    DocumentosSolicitacao = models.FileField(
    'documentos',
    upload_to=upload_documentos,
    null=True, blank=True
    )

    Historico = HistoricalRecords(
        excluded_fields=[
            'DescricaoDoChamado', 'TituloDaSolicitacao', 'DepartamentoSolicitante',
            'DivisaoSolicitante', 'SecaoSolicitante', 'DestinoDaSolicitacao', 'DocumentosSolicitacao',
            'AssuntoDaSolicitacao', 'ConfirmacaoDeSolicitacao',
            ])

    class Meta:
        ordering = ('-id',)
        verbose_name = ("Solicitacoes")
        verbose_name_plural = ("Solicitacoes")

    def __str__(self):
        return f'{self.NomeGuerraSolicitante}-{self.ReSolicitante}-{self.UnidadeSolicitante}'

    def whensolicited(self):
        now = timezone.now()
        
        diff= now - self.RespostaData

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds == 1:
                return str(seconds) +  "segundo atrás"
            
            else:
                return str(seconds) + " segundos atrás"

            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minuto atrás"
            
            else:
                return str(minutes) + " minutos atrás"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hora atrás"

            else:
                return str(hours) + " horas atrás"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + " dia atrás"

            else:
                return str(days) + " dias atrás"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + " mês atrás"

            else:
                return str(months) + " meses atrás"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " ano atrás"

            else:
                return str(years) + " anos atrás"    

    def get_absolute_url(self):
        return reverse("solicitacao_details", kwargs={"id": self.id})

class RespostaSolicitacao(models.Model):    
    
    RespostaDaSolicitacao = RichTextUploadingField(
        'Descrição do Chamado',
        null=True, blank=True
    )
    
    RespostaResponsavel = models.ForeignKey(
        User,
        related_name='+',
        verbose_name='Policial Responsável',
        on_delete=models.DO_NOTHING,
        null=True, blank=True
    )

    Solicitacao = models.ForeignKey(
        Solicitacoes,
        related_name='replies',
        verbose_name='Chamado',
        on_delete=models.DO_NOTHING,
        null=True, blank=True
    )

    RespostaAnexo = models.FileField(
    'documentos',
    upload_to=upload_documentos_resposta,
    null=True, blank=True
    )
    
    RespostaData = models.DateTimeField(
        auto_now_add=True,
        null=True, blank=True)    

    class Meta:
        verbose_name = ("RespostaSolicitacao")
        verbose_name_plural = ("RespostaSolicitacaos")

    def __str__(self):
        return self.RespostaDaSolicitacao

    
    def whenreplyed(self):
        now = timezone.now()
        
        diff= now - self.RespostaData

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds == 1:
                return str(seconds) +  "segundo atrás"
            
            else:
                return str(seconds) + " segundos atrás"

            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minuto atrás"
            
            else:
                return str(minutes) + " minutos atrás"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hora atrás"

            else:
                return str(hours) + " horas atrás"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + " dia atrás"

            else:
                return str(days) + " dias atrás"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + " mês atrás"

            else:
                return str(months) + " meses atrás"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " ano atrás"

            else:
                return str(years) + " anos atrás"

    def get_absolute_url(self):
        return reverse("RespostaSolicitacao_detail", kwargs={"id": self.id})


class RespostaUsuario(models.Model):    
    
    RespostaDoUsuario = RichTextUploadingField(
        'Resposta do Usuário',
        null=True, blank=True
    )
    
    RespostaUsuarioResponsavel = models.ForeignKey(
        User,
        verbose_name='Policial Responsável',
        related_name='user',
        on_delete=models.DO_NOTHING,
        null=True, blank=True
    )

    RespostaDaSolicitacao = models.ForeignKey(
        RespostaSolicitacao,
        related_name='user_reply',
        verbose_name='Chamado',
        on_delete=models.DO_NOTHING,
        null=True, blank=True
    )
    
    RespostaUsuarioData = models.DateTimeField(
        auto_now_add=True,
        null=True, blank=True)    

    class Meta:
        verbose_name = ("RespostaDoUsuario")
        verbose_name_plural = ("RespostaDoUsuarios")

    def __str__(self):
        return self.RespostaDoUsuario

    def whenuserreplyed(self):
        now = timezone.now()
        
        diff= now - self.RespostaUsuarioData

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds == 1:
                return str(seconds) +  "segundo atrás"
            
            else:
                return str(seconds) + " segundos atrás"

            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minuto atrás"
            
            else:
                return str(minutes) + " minutos atrás"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hora atrás"

            else:
                return str(hours) + " horas atrás"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + " dia atrás"

            else:
                return str(days) + " dias atrás"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + " mês atrás"

            else:
                return str(months) + " meses atrás"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " ano atrás"

            else:
                return str(years) + " anos atrás"

    def get_absolute_url(self):
        return reverse("RespostaDoUsuario_detail", kwargs={"id": self.id})



class ChamadoBackup(models.Model):
    nome = models.CharField(
        max_length=50,
        null=True, blank=True
    )

    unidade = models.CharField(
        max_length=30,
        null=True, blank=True
    )

    problema = models.TextField(        
        null=True, blank=True
    )

    data_sol = models.DateField(
        null=True, blank=True
    )

    data_res = models.DateField(
        max_length=50,
        null=True, blank=True
    )

    id = models.IntegerField(
        primary_key=True,
        blank=True
    )

    situacao = models.CharField(
        max_length=50,
        null=True, blank=True
    )

    PM_res = models.CharField(
        max_length=50,
        null=True, blank=True
    )

    obs = models.TextField(
        null=True, blank=True
    )

    re_ch = models.CharField(
        max_length=9,
        null=True, blank=True
    )

    data_atu = models.DateField(
        max_length=50,
        null=True, blank=True
    )

    PM_atu = models.CharField(
        max_length=50,
        null=True, blank=True
    )

    OPM = models.CharField(
        max_length=50,
        null=True, blank=True
    )

    

    class Meta:
        verbose_name = ("Chamado Legado Backup")
        verbose_name_plural = ("Chamado Legado Backup")

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse("ChamadoBackup_detail", kwargs={"pk": self.pk})
