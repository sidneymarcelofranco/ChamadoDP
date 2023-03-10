# Generated by Django 4.0.2 on 2022-03-13 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('help_pages', '0004_alter_categorias_tipoblog'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoBlog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TipoBlog', models.CharField(blank=True, max_length=50, null=True, verbose_name='Tipo de Blog')),
            ],
            options={
                'verbose_name': 'Tipo de Blog',
                'verbose_name_plural': 'Tipo de Blog',
                'ordering': ['id'],
            },
        ),
        migrations.AlterField(
            model_name='categorias',
            name='TipoBlog',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='help_pages.tipoblog', verbose_name='Tipo de Blog'),
        ),
    ]
