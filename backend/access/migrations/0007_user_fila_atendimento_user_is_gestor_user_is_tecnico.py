# Generated by Django 4.2.10 on 2025-01-21 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0006_remove_user_cep_remove_user_cpf_remove_user_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='fila_atendimento',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='is_gestor',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_tecnico',
            field=models.BooleanField(default=False),
        ),
    ]
