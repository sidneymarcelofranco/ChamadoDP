# Generated by Django 4.0.2 on 2022-03-18 20:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('help_pages', '0008_alter_chamadoblog_assuntoblog_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='categorias',
            unique_together={('SlugCategoria', 'TipoBlog')},
        ),
    ]