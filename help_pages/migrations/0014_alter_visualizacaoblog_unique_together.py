# Generated by Django 4.0.2 on 2022-03-20 01:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('help_pages', '0013_visualizacaoblog'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='visualizacaoblog',
            unique_together={('Post_id', 'User_id')},
        ),
    ]