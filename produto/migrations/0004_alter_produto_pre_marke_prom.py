# Generated by Django 4.2.7 on 2023-11-29 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0003_alter_produto_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='pre_marke_prom',
            field=models.FloatField(),
        ),
    ]