# Generated by Django 4.0.2 on 2022-03-16 01:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solicitation', '0016_alter_solicitacoes_responsavel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalsolicitacoes',
            name='DescricaoDoChamado',
        ),
        migrations.RemoveField(
            model_name='historicalsolicitacoes',
            name='TituloDaSolicitacao',
        ),
    ]
