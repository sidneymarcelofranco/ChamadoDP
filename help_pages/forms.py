from django import forms
from help_pages.models import Categorias, ChamadoBlog
from ckeditor.widgets import CKEditorWidget


class BlogForm(forms.ModelForm):
    TituloBlog = forms.CharField(        
        max_length=100,
        required=True,
        error_messages={'required': 'O Titulo é Obrigatório!','invalid':'Titulo Inválido!'},      
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )

    AssuntoBlog = forms.CharField(
        max_length=100,
        required=True,
        error_messages={'required': 'O Assunto é Obrigatório!','invalid':'Assunto Inválido!'},      
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    

    CategoriaBlog = forms.ModelChoiceField(
        queryset=Categorias.objects.all(),
        required=True,
        help_text='Escolha uma categoria', 
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )

    Ativo = forms.BooleanField(
        required= False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    IntroducaoBlog = forms.CharField(
        required=True,
        error_messages={'required': 'A Introdução é Obrigatória!','invalid':'Introdução Inválida!'},     
        widget=CKEditorWidget())

    DescricaoBlog = forms.CharField(
        required=True,
        error_messages={'required': 'A Descrição é Obrigatória!','invalid':'Descrição Inválida!'},     
        widget=CKEditorWidget())

    class Meta:
        model = ChamadoBlog
        fields = [
            'TituloBlog', 'CategoriaBlog', 'AssuntoBlog',
            'IntroducaoBlog', 'DescricaoBlog', 'Ativo',
            ]


class BlogFormUpdate(forms.ModelForm):
    TituloBlog = forms.CharField(        
        max_length=100,
        required=True,
        error_messages={'required': 'O Titulo é Obrigatório!','invalid':'Titulo Inválido!'},      
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )

    AssuntoBlog = forms.CharField(
        max_length=100,
        required=True,
        error_messages={'required': 'O Assunto é Obrigatório!','invalid':'Assunto Inválido!'},      
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    

    CategoriaBlog = forms.ModelChoiceField(
        queryset=Categorias.objects.all(),
        required=True,
        help_text='Escolha uma categoria', 
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )

    IntroducaoBlog = forms.CharField(
        required=True,
        error_messages={'required': 'A Introdução é Obrigatória!','invalid':'Introdução Inválida!'},     
        widget=CKEditorWidget())

    DescricaoBlog = forms.CharField(
        required=True,
        error_messages={'required': 'A Descrição é Obrigatória!','invalid':'Descrição Inválida!'},     
        widget=CKEditorWidget())

    Ativo = forms.BooleanField(
        required= False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = ChamadoBlog
        fields = [
            'TituloBlog', 'CategoriaBlog', 'AssuntoBlog',
            'IntroducaoBlog', 'DescricaoBlog', 'Ativo',
            ]