# Generated by Django 5.0.6 on 2024-07-01 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alter_aportador_rut_alter_aporte_aportador_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='aportador',
            name='is_colaborador',
            field=models.BooleanField(default=False),
        ),
    ]
