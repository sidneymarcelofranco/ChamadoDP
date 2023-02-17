from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class RespostasProntas(models.Model):

    TituloRespostaPronta = models.CharField(
        max_length=150,
        null=True, blank=True
    )

    DescricaoRespostaPronta =  RichTextUploadingField(
        'Resposta Pronta',
        null=True, blank=True
    )    

    class Meta:
        verbose_name = ("RespostasProntas")
        verbose_name_plural = ("RespostasProntass")

    def __str__(self):
        return self.TituloRespostaPronta
