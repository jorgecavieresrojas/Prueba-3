# Generated by Django 5.0.6 on 2024-07-01 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_residente_estado_salud_residente_fecha_ingreso_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Insumo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('cantidad', models.IntegerField()),
                ('fecha_recepcion', models.DateField()),
            ],
        ),
    ]
