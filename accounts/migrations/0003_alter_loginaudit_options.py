# Generated by Django 4.0.3 on 2022-04-07 02:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_loginaudit_opmcod5'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='loginaudit',
            options={'verbose_name': 'Auditoria de login', 'verbose_name_plural': 'Auditoria de logins'},
        ),
    ]
