# Generated by Django 4.0.2 on 2022-03-20 07:08

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RespostasProntas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TituloRespostaPronta', models.CharField(blank=True, max_length=150, null=True)),
                ('DescricaoRespostaPronta', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Resposta Pronta')),
            ],
            options={
                'verbose_name': 'RespostasProntas',
                'verbose_name_plural': 'RespostasProntass',
            },
        ),
    ]
