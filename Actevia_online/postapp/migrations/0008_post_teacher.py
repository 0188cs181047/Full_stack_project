# Generated by Django 4.1.6 on 2023-03-10 07:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0001_initial'),
        ('postapp', '0007_remove_replypostrating_comment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='teacher.teacher'),
        ),
    ]
