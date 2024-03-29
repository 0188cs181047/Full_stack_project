# Generated by Django 4.2 on 2023-06-15 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApplyLeave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leave_reason', models.CharField(max_length=100, verbose_name='Leave Reason')),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('end_date', models.DateField(verbose_name='End Date')),
                ('leave_type', models.CharField(blank=True, choices=[('CL', 'Casual Leave'), ('EL', 'Earned Leave'), ('CS', 'Compensatory Leave'), ('BL', 'Balance Leave')], max_length=20, null=True, verbose_name='Leave Type')),
                ('work_from_home', models.BooleanField(default=False, verbose_name='Work from Home')),
                ('description', models.TextField(verbose_name='Description')),
                ('approved', models.BooleanField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.CharField(max_length=10, unique=True)),
                ('employee_name', models.CharField(max_length=100)),
                ('employee_email', models.EmailField(max_length=254, unique=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('manager_approved', models.BooleanField(default=False, verbose_name='Manager Approved')),
                ('last_earned_leave_update_date', models.DateField(blank=True, null=True)),
                ('joining_date', models.DateField(auto_now_add=True, verbose_name='Joining Date')),
            ],
        ),
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('occasion', models.CharField(blank=True, default='None', max_length=100, null=True)),
                ('day', models.CharField(max_length=100)),
                ('category', models.CharField(choices=[('Internal', 'Internal'), ('External', 'External'), ('Other', 'Other')], default='External', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manager_id', models.CharField(max_length=10, unique=True)),
                ('manager_name', models.CharField(max_length=100)),
                ('manager_email', models.EmailField(max_length=254, unique=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='LeaveBalance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leave_type', models.CharField(blank=True, choices=[('CL', 'Casual Leave'), ('EL', 'Earned Leave'), ('CS', 'Compensatory Leave'), ('BL', 'Balance Leave')], max_length=20, null=True, verbose_name='Leave Type')),
                ('balance', models.PositiveIntegerField(verbose_name='Leave Balance')),
                ('balance_increase', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Balance Increase per Month')),
                ('days_taken', models.PositiveIntegerField(default=0, verbose_name='Days Taken')),
                ('last_updated', models.DateTimeField(auto_now=True, verbose_name='Last Updated')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leave_balances', to='leaveapp.employee')),
                ('leave_data', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='leave_balances', to='leaveapp.applyleave')),
            ],
            options={
                'verbose_name': 'Leave Balance',
                'verbose_name_plural': 'Leave Balances',
            },
        ),
        migrations.AddField(
            model_name='employee',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leaveapp.manager'),
        ),
        migrations.AddField(
            model_name='applyleave',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leaveapp.employee'),
        ),
    ]
