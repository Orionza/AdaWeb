# Generated by Django 5.0.7 on 2024-08-15 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0009_alter_saglikbilgileri_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='daskbilgileri',
            options={'verbose_name_plural': 'Dask Poliçeleri'},
        ),
        migrations.AlterField(
            model_name='aracbilgileri',
            name='plaka_kodu',
            field=models.CharField(max_length=5),
        ),
    ]
