# Generated by Django 4.0.2 on 2022-02-09 14:36

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AssuntoSolicitacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Assunto', models.CharField(blank=True, max_length=100, null=True, verbose_name='Assunto')),
            ],
            options={
                'verbose_name': 'Assunto',
            },
        ),
        migrations.CreateModel(
            name='CategoriaSolicitacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Categoria', models.CharField(blank=True, max_length=100, null=True, verbose_name='Categoria')),
            ],
            options={
                'verbose_name': 'Categoria',
            },
        ),
        migrations.CreateModel(
            name='DestinoSolicitacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SecaoOPMCOD', models.CharField(blank=True, max_length=100, null=True, verbose_name='Código da Seção')),
            ],
            options={
                'verbose_name': 'Status',
            },
        ),
        migrations.CreateModel(
            name='StatusSolicitacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Status', models.CharField(blank=True, max_length=100, null=True, verbose_name='Status da Solicitação')),
            ],
            options={
                'verbose_name': 'Status',
            },
        ),
        migrations.CreateModel(
            name='Solicitacoes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PostoGradSolicitante', models.CharField(blank=True, max_length=100, null=True, verbose_name='Posto / Grad')),
                ('ReSolicitante', models.CharField(blank=True, max_length=100, null=True, verbose_name='Re')),
                ('NomeGuerraSolicitante', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nome de Guerra')),
                ('CpfSolicitante', models.CharField(blank=True, max_length=100, null=True, verbose_name='CPF')),
                ('FuncaoSolicitante', models.CharField(blank=True, max_length=100, null=True, verbose_name='Função')),
                ('CodOpmSolicitante', models.CharField(blank=True, max_length=10, null=True, verbose_name='Opm Cod')),
                ('GrandeComandoSolicitante', models.CharField(blank=True, max_length=50, null=True, verbose_name='Grande Comando')),
                ('UnidadeSolicitante', models.CharField(blank=True, max_length=50, null=True, verbose_name='Unidade')),
                ('TituloDaSolicitacao', models.CharField(blank=True, max_length=150, null=True, verbose_name='Titulo da Solicitação')),
                ('DataDaSolicitacao', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Criado em:')),
                ('DescricaoDoChamado', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Descrição do Chamado')),
                ('ConfirmacaoDeSolicitacao', models.BooleanField(blank=True, default=False, null=True)),
                ('AssuntoDaSolicitacao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='solicitation.assuntosolicitacao', verbose_name='Assunto')),
                ('CategoriaDaSolicitacao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='solicitation.categoriasolicitacao', verbose_name='Categoria')),
                ('DestinoDaSolicitacao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='solicitation.destinosolicitacao', verbose_name='Destino')),
                ('StatusAtual', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='status_solicitacao', to='solicitation.statussolicitacao', verbose_name='Status Atual')),
                ('Usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Usuário Solicitante')),
            ],
            options={
                'verbose_name': 'Solicitacoes',
                'verbose_name_plural': 'Solicitacoes',
                'ordering': ('-id',),
            },
        ),
        migrations.AddField(
            model_name='assuntosolicitacao',
            name='Categoria_Fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='solicitation.categoriasolicitacao'),
        ),
    ]
