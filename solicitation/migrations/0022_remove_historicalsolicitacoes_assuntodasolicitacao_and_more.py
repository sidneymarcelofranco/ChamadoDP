# Generated by Django 4.0.2 on 2022-03-29 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solicitation', '0021_historicalsolicitacoes_departamentosolicitante_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalsolicitacoes',
            name='AssuntoDaSolicitacao',
        ),
        migrations.RemoveField(
            model_name='historicalsolicitacoes',
            name='ConfirmacaoDeSolicitacao',
        ),
        migrations.RemoveField(
            model_name='historicalsolicitacoes',
            name='DepartamentoSolicitante',
        ),
        migrations.RemoveField(
            model_name='historicalsolicitacoes',
            name='DestinoDaSolicitacao',
        ),
        migrations.RemoveField(
            model_name='historicalsolicitacoes',
            name='DivisaoSolicitante',
        ),
        migrations.RemoveField(
            model_name='historicalsolicitacoes',
            name='DocumentosSolicitacao',
        ),
        migrations.RemoveField(
            model_name='historicalsolicitacoes',
            name='SecaoSolicitante',
        ),
    ]