# Generated by Django 4.2 on 2023-06-19 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaveapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='applyleave',
            name='rejection_reason',
            field=models.TextField(blank=True, null=True, verbose_name='Rejection Reason'),
        ),
    ]
