# Generated by Django 4.2 on 2023-06-16 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cridential', '0003_teacheruser_studentuser'),
        ('teacher', '0002_coursepublication'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursepublication',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cridential.studentuser'),
        ),
    ]
