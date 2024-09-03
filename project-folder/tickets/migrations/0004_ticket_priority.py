# Generated by Django 5.1 on 2024-09-03 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0003_alter_ticket_close_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='priority',
            field=models.CharField(choices=[(0, 'None'), (1, 'Medium'), (2, 'High'), (3, 'Critic')], default=0, max_length=10),
        ),
    ]
