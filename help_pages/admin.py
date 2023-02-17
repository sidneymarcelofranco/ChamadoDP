from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from .models import (
    Categorias,
    ChamadoBlog,
    TipoBlog,
)


@admin.register(Categorias)
class CategoriasAdmin(admin.ModelAdmin):
    model = Categorias
    list_display = [ 'TipoBlog', 'DescricaoCategoria', 'SlugCategoria','Ativo', 'Importancia']  
    list_filter = ['TipoBlog',]
    list_display_links =['DescricaoCategoria']

@admin.register(TipoBlog)
class TipoBlogAdmin(admin.ModelAdmin):
    model = TipoBlog
    list_display = ['TipoBlog',]
    list_filter = ['TipoBlog',]


@admin.register(ChamadoBlog)
class ChamadoBlogAdmin(admin.ModelAdmin):

    model = ChamadoBlog
    list_display = ['TituloBlog', 'CategoriaBlog', 'AssuntoBlog', 'AutorBlog', 'Ativo']  
    list_filter = ['CategoriaBlog',]
    list_display_links = ['TituloBlog', 'CategoriaBlog', 'AssuntoBlog', 'AutorBlog', 'Ativo']
    
    def get_form(self, request, obj, **kwargs):
        form = super(ChamadoBlogAdmin,self).get_form(request, obj, **kwargs)
        form.base_fields['AutorBlog'] = forms.ModelChoiceField(queryset=User.objects.filter(is_superuser=True))
        return form

class MyModelAdmin(admin.ModelAdmin):
    list_display = ['tag_list']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())