# Generated by Django 4.0.2 on 2022-03-08 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitation', '0010_alter_chamadobackup_obs_alter_chamadobackup_problema'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chamadobackup',
            name='data_atu',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='chamadobackup',
            name='data_res',
            field=models.DateField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='chamadobackup',
            name='data_sol',
            field=models.DateField(blank=True, null=True),
        ),
    ]
