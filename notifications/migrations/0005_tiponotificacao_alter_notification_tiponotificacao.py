# Generated by Django 4.0.2 on 2022-03-14 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0004_notification_to_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoNotificacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DescricaoNotificacao', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'Tipos de Notificação',
                'verbose_name_plural': 'Tipos de Notificações',
            },
        ),
        migrations.AlterField(
            model_name='notification',
            name='TipoNotificacao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='notifications.tiponotificacao'),
        ),
    ]