from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import math
from solicitation.models import (
    Solicitacoes,
    RespostaSolicitacao,
    RespostaUsuario,
)

from help_pages.models import (
    ChamadoBlog
)

class TipoNotificacao(models.Model):
    DescricaoNotificacao = models.CharField(
        max_length=50,
        null=True, blank=True
    )
    

    class Meta:
        verbose_name = ("Tipos de Notificação")
        verbose_name_plural = ("Tipos de Notificações")

    def __str__(self):
        return self.DescricaoNotificacao
    



class Notification(models.Model):
    
    TipoNotificacao = models.ForeignKey(
        TipoNotificacao,
        on_delete=models.DO_NOTHING,
        null=True, blank=True
    )

    to_user = models.ForeignKey(
        User,
        related_name='notification_to',
        on_delete=models.CASCADE,
        null=True
    )

    from_user = models.ForeignKey(
        User,
        related_name='notification_from',
        on_delete=models.CASCADE,
        null=True
    )

    to_admin = models.IntegerField(
        null=True
    )

    Solicitacao = models.ForeignKey(
        Solicitacoes,
        on_delete=models.CASCADE,
        related_name='+',
        blank=True, null=True
    )

    RespostaAdmin = models.ForeignKey(
        RespostaSolicitacao,
        on_delete=models.CASCADE,
        related_name='+',
        blank=True, null=True
    )

    RespostaUser = models.ForeignKey(
        RespostaUsuario,
        on_delete=models.CASCADE,
        related_name='+',
        blank=True, null=True
    )

    BlogPost = models.ForeignKey(
        ChamadoBlog,
        on_delete=models.CASCADE,
        related_name='+',
        blank=True, null=True
    )

    NovoUser = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='+',
        blank=True, null=True
    )

    DataNotificacao = models.DateTimeField(
        'Criado em:',
        auto_now_add=True,
        auto_now=False,
        null=True, blank=True
    )

    DataVisualizacao = models.DateTimeField(
        'Visuzaliada em:',
        null=True, blank=True
    )

    user_has_seen = models.BooleanField(default=False)

    user_has_archive = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Tipo de Notificação: {self.TipoNotificacao}'
    
    def whenpublished(self):
        now = timezone.now()
        
        diff= now - self.DataNotificacao

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
    
    def whenview(self):
        now = timezone.now()
        
        diff= now - self.DataVisualizacao

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

    class Meta:
        ordering = ('-id',)
        verbose_name = ("Notificação")
        verbose_name_plural = ("Notificações")
