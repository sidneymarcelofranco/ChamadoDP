# Generated by Django 4.0.2 on 2022-03-14 18:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('solicitation', '0015_alter_respostasolicitacao_respostaresponsavel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitacoes',
            name='Responsavel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Policial Responsável'),
        ),
    ]
