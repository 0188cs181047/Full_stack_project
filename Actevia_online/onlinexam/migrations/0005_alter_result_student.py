# Generated by Django 4.2 on 2023-06-19 03:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cridential', '0003_teacheruser_studentuser'),
        ('onlinexam', '0004_uploadedexcel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cridential.studentuser'),
        ),
    ]
