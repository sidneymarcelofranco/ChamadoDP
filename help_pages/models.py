from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify

from taggit.managers import TaggableManager

from ckeditor_uploader.fields import RichTextUploadingField

class TipoBlog(models.Model):
    TipoBlog = models.CharField(
        'Tipo de Blog',
        max_length=50,
        null=True, blank=True
    )

    class Meta:
        verbose_name = ("Tipo de Blog")
        verbose_name_plural = ("Tipo de Blog")
        ordering = ['id']

    def __str__(self):
        return f'{self.TipoBlog}'


class Categorias(models.Model):
    DescricaoCategoria = models.CharField(
        'Descricao da Categoria',
        max_length=50,
        null=True, blank=True
    )

    TipoBlog = models.ForeignKey(
        TipoBlog,
        verbose_name='Tipo de Blog',
        on_delete=models.DO_NOTHING,
        null=True, blank=True
    )

    SlugCategoria = models.SlugField(
        'Slug categoria',
        null=True, blank=True
    )

    Ativo = models.BooleanField(
        default=False
    )

    Importancia = models.PositiveIntegerField(
        'Ordem de Exibição',
        default=0,
    )

    class Meta:
        verbose_name = ("Categorias")
        verbose_name_plural = ("Categorias")
        ordering = ['id']
        unique_together = ('SlugCategoria','TipoBlog')

    def __str__(self):
        return f'{self.DescricaoCategoria} EM {str(self.TipoBlog)}'

    def save(self, *args, **kwargs):
        if self.SlugCategoria is None:
            self.SlugCategoria = slugify(
                f'{self.DescricaoCategoria}')
            super(Categorias, self).save(*args, **kwargs)
        else:
            super(Categorias, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("DescricaoCategoria_details", kwargs={"slugcategoria": self.SlugCategoria})


class ChamadoBlog(models.Model):
    TituloBlog = models.CharField(
        'Titulo',
        max_length=100,
        null=True, blank=True
    )

    CategoriaBlog = models.ForeignKey(
        Categorias,
        verbose_name='Categoria',
        on_delete=models.DO_NOTHING,
        related_name='CategoriaBlog'
    )

    AssuntoBlog = models.CharField(
        'Assunto',
        max_length=100,
        null=True, blank=True
    )

    IntroducaoBlog = RichTextUploadingField(
        'Introducção do Blog',
        null=True, blank=True
    )

    DescricaoBlog = RichTextUploadingField(
        'Descrição Blog',
        null=True, blank=True
    )

    SlugBlog = models.SlugField(
        'Slug Blog',
        unique=True,
        null=True, blank=True
    )

    Ativo = models.BooleanField(
        default=False,
        null=True, blank=True
        )

    AutorBlog = models.ForeignKey(
        User,
        verbose_name='Autor',
        on_delete=models.DO_NOTHING
    )

    LikesBlog = models.ManyToManyField(
        User, blank=True,
        related_name="likes"
    )

    TagsBlog = TaggableManager(
        'Tags'
    )

    DataCriacao = models.DateTimeField(
        'Criado em:',
        auto_now_add=True,
        auto_now=False,
        null=True, blank=True
    )

    ViewCount = models.IntegerField(
        'Visualizações',
        default=0,
        null=True, blank=True
    )

    class Meta:
        verbose_name = ("Chamado Blog")
        verbose_name_plural = ("Chamado Blog")

    def __str__(self):
        return self.TituloBlog

    @property
    def num_likes(self):
        return self.LikesBlog.all().count()

    def save(self, *args, **kwargs):
        if self.SlugBlog is None:
            self.SlugBlog = slugify(
                f'{self.TituloBlog}')
            super(ChamadoBlog, self).save(*args, **kwargs)
        else:
            super(ChamadoBlog, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog_details", kwargs={"SlugBlog": self.SlugBlog})


class VisualizacaoBlog(models.Model):

    Post_id = models.IntegerField(
        'Blog FK',
        default=0,
        null=True, blank=True
    )
    
    User_id = models.IntegerField(
        'User FK',
        default=0,
        null=True, blank=True
    )

    DataVisualizacao = models.DateTimeField(
        auto_now_add=True,
        null=True, blank=True
        ) 

    class Meta:
        verbose_name = ("Confirma Visualização")
        verbose_name_plural = ("Confirma Visualização")
        unique_together = ('Post_id', 'User_id',)

