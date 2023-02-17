from django import forms
from django.forms.models import ModelChoiceField

from solicitation.models import (
    AssuntoSolicitacao,
    DestinoSolicitacao, 
    RespostaSolicitacao, 
    RespostaUsuario, 
    Solicitacoes, 
    CategoriaSolicitacao, 
    StatusSolicitacao,
    )

from ckeditor.widgets import CKEditorWidget
class SolicitacoesForm(forms.ModelForm):    
    
    PostoGradSolicitante = forms.CharField(
        max_length=60,
        required=False,        
    )

    ReSolicitante = forms.CharField(
        max_length=10,
        required=False,
    )

    NomeGuerraSolicitante = forms.CharField(
        max_length=60,
        required=False,
    )

    CpfSolicitante = forms.CharField(
        max_length=11,
        required=False,
    )

    FuncaoSolicitante = forms.CharField(
        max_length=80,
        required=False,
    )

    CodOpmSolicitante = forms.CharField(
        max_length=9,
        required=False,
    )

    GrandeComandoSolicitante = forms.CharField(
        max_length=60,
        required=False,
    )

    UnidadeSolicitante = forms.CharField(
        max_length=60,
        required=False,
    )

    TituloDaSolicitacao = forms.CharField(
        max_length=60,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite um título para sua solicitação',
        })
    )
    
    CategoriaDaSolicitacao = ModelChoiceField(
        queryset=CategoriaSolicitacao.objects.all(),        
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select',
         
        })
    )


    DestinoDaSolicitacao = ModelChoiceField(
        queryset=DestinoSolicitacao.objects.all(),
        required=True,
        help_text='Escolha a Seção Responsável',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'placeholder': 'Escolha a Seção Responsável',
        })
    )

    DescricaoDoChamado = forms.CharField(widget=CKEditorWidget())

    confirmasolicitacao = forms.BooleanField(
        required= True,
        help_text='Confirme a solicitação',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    DocumentosSolicitacao = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control form-control-sm',
            'type': 'file'
        }        )
    )

    
    class Meta:
        model = Solicitacoes
        fields = [
            'PostoGradSolicitante', 'ReSolicitante', 'NomeGuerraSolicitante',
            'CpfSolicitante', 'FuncaoSolicitante', 'CodOpmSolicitante',
            'GrandeComandoSolicitante', 'UnidadeSolicitante', 'CodOpmSolicitante',
            'TituloDaSolicitacao', 'CategoriaDaSolicitacao','DestinoDaSolicitacao', 
            'DescricaoDoChamado', 'confirmasolicitacao', 'DocumentosSolicitacao'
            ]



class SolicitacoesUpdateForm(forms.ModelForm):
    TituloDaSolicitacao = forms.CharField(
        max_length=60,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite um título para sua solicitação',
        })
    )
    

    CategoriaDaSolicitacao = ModelChoiceField(
        queryset=CategoriaSolicitacao.objects.all(),
        required=True,
        help_text='Escolha uma categoria', 
        widget=forms.Select(attrs={
            'class': 'form-select',
            'placeholder': 'Selecione uma Categoria',
        })
    )

    DestinoDaSolicitacao = ModelChoiceField(
        queryset=DestinoSolicitacao.objects.all(),
        required=True,
        help_text='Escolha a Seção Responsável',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'placeholder': 'Escolha a Seção Responsável',
        })
    )

    DescricaoDoChamado = forms.CharField(
        required= True,
        widget=CKEditorWidget())

    DocumentosSolicitacao = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control form-control-sm',
            'type': 'file'
        })
    )

    class Meta:
        model = Solicitacoes
        fields = [
            'TituloDaSolicitacao', 'CategoriaDaSolicitacao', 'DestinoDaSolicitacao',
            'DescricaoDoChamado', 'DocumentosSolicitacao',
            ]


class SerResponsavelForm(forms.ModelForm):
    StatusAtual = ModelChoiceField(
        queryset=StatusSolicitacao.objects.all(),
        required=False,
    )   

    Responsavel = forms.IntegerField(
        required=False,
    )

    class Meta:
        model = Solicitacoes
        fields = [
            'StatusAtual', 'Responsavel',
            ]


class RespostaSolicitacaoForm(forms.ModelForm):
    RespostaDaSolicitacao = forms.CharField(
        widget=CKEditorWidget()
    )

    RespostaAnexo = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control form-control-sm',
            'type': 'file'
        }        )
    )
    
    class Meta:
        model = RespostaSolicitacao
        fields = [
            'RespostaDaSolicitacao', 'RespostaAnexo'
            ]


class RespostaUsuarioForm(forms.ModelForm):
    RespostaDoUsuario= forms.CharField(
        widget=CKEditorWidget()
    )
    
    class Meta:
        model = RespostaUsuario
        fields = [
            'RespostaDoUsuario',
            ]
