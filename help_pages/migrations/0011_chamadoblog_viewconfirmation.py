# Generated by Django 4.0.2 on 2022-03-20 01:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('help_pages', '0010_alter_categorias_slugcategoria'),
    ]

    operations = [
        migrations.AddField(
            model_name='chamadoblog',
            name='ViewConfirmation',
            field=models.ManyToManyField(blank=True, related_name='userview', to=settings.AUTH_USER_MODEL),
        ),
    ]
