# Generated by Django 3.2 on 2022-12-18 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20221218_1325'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default='000000', max_length=6),
        ),
    ]
