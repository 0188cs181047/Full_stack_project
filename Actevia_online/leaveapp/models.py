from django.db import models
from django.utils import timezone
from django.db.models import F
from datetime import date
from celery import shared_task




class Manager(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )

    manager_id = models.CharField(max_length=10, unique=True)
    manager_name = models.CharField(max_length=100)
    manager_email = models.EmailField(unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return self.manager_name


class Employee(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )

    employee_id = models.CharField(max_length=10, unique=True)
    employee_name = models.CharField(max_length=100)
    employee_email = models.EmailField(unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    manager_approved = models.BooleanField(default=False, verbose_name='Manager Approved')
    last_earned_leave_update_date = models.DateField(null=True, blank=True)
    joining_date = models.DateField(verbose_name='Joining Date' ,auto_now_add=True)
    work_from_home_balance = models.DecimalField(
        verbose_name='Work from Home Balance',
        max_digits=10,
        decimal_places=2,
        default=0.0
    )


    def __str__(self):
        return self.employee_name

    @property
    def manager_name(self):
        return self.manager.manager_name

    @property
    def manager_email(self):
        return self.manager.manager_email
    



class ApplyLeave(models.Model):
    LEAVE_CHOICES = (
        # ('CL', 'Casual Leave'),
        ('EL', 'Earned Leave'),
        # ('CS', 'Compensatory Leave'),
        # ('BL', 'Balance Leave')
    )

    leave_reason = models.CharField(max_length=100, verbose_name='Leave Reason')
    start_date = models.DateField(verbose_name='Start Date')
    end_date = models.DateField(verbose_name='End Date')
    leave_type = models.CharField(max_length=20, choices=LEAVE_CHOICES, verbose_name='Leave Type', blank=True, null=True)
    work_from_home = models.BooleanField(default=False, verbose_name='Work from Home')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    description = models.TextField(verbose_name='Description')
    approved = models.BooleanField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True, null=True, verbose_name='Rejection Reason')


    def __str__(self):
        leave_type_name = dict(self.LEAVE_CHOICES).get(self.leave_type)
        return f"{leave_type_name}+{self.employee.employee_name}"

    def save(self, *args, **kwargs):
        if self.pk is None:
            if self.employee.manager:
                self.employee.manager_approved = False
                self.employee.save()

        super().save(*args, **kwargs)

    def approve_leave(self):
        if not self.employee.manager:
            self.approved = True
        else:
            self.employee.manager_approved = True
            self.employee.save()

            all_leave_approved = self.employee.applyleave_set.exclude(pk=self.pk).filter(approved=False).count() == 0
            if all_leave_approved:
                self.approved = True

        if not self.work_from_home:  # Regular leave (not work from home)
            # Subtract leave from leave balance
            if self.leave_type:
                leave_balance = LeaveBalance.objects.filter(
                    leave_type=self.leave_type,
                    leave_data__employee=self.employee
                ).first()

                if leave_balance:
                    start_date = self.start_date
                    end_date = self.end_date

                    # Calculate the number of days between start date and end date
                    duration = (end_date - start_date).days + 1

                    # Subtract the number of days taken from the leave balance
                    leave_balance.balance = F('balance') - duration
                    leave_balance.last_updated = timezone.now()
                    leave_balance.save()

        else:  # If it's a work from home leave application
            if not self.employee.manager:
                self.work_from_home = False
            else:
                self.employee.work_from_home_balance -= 1
                self.employee.save()

                # Subtract work from home days from work_from_home_balance
                start_date = self.start_date
                end_date = self.end_date
                duration = (end_date - start_date).days + 1
                self.employee.work_from_home_balance -= duration
                self.employee.save()

        self.save()


    def status(self):
        if self.approved:
            return "Approved"
        elif self.approved is False:
            return "Rejected"
        else:
            return "Pending"
        
    def reject_leave(self, rejection_reason):
        self.approved = False
        self.rejection_reason = rejection_reason
        self.save()




class LeaveBalance(models.Model):
    LEAVE_CHOICES = (
        # ('CL', 'Casual Leave'),
        ('EL', 'Earned Leave'),
        # ('CS', 'Compensatory Leave'),
        # ('BL', 'Balance Leave')
    )
    leave_type = models.CharField(max_length=20, choices=LEAVE_CHOICES, verbose_name='Leave Type', blank=True, null=True)
    balance = models.PositiveIntegerField(verbose_name='Leave Balance')
    balance_increase = models.DecimalField(verbose_name='Balance Increase per Month',max_digits=10,decimal_places=2,blank=True,null=True)
    work_from_home_balance = models.DecimalField(verbose_name='Work from Home Balance', max_digits=10, decimal_places=2, default=0.0)
    leave_data = models.ForeignKey(ApplyLeave, on_delete=models.CASCADE, related_name='leave_balances', null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_balances')
    days_taken = models.PositiveIntegerField(verbose_name='Days Taken', default=0)
    last_updated = models.DateTimeField(verbose_name='Last Updated', auto_now=True)

    def __str__(self):
        return f"{self.leave_type} - {self.balance}"

    def get_leave_status(self):
        if self.leave_type:
            return self.leave_type.status()
        else:
            return "N/A"


    @shared_task
    def increase_earned_leave_balance(self, leave_balance_id=None):
        leave_balance = LeaveBalance.objects.get(id=leave_balance_id)
        if leave_balance.leave_type == 'EL':
            current_date = timezone.now().date()
            last_updated_date = leave_balance.last_updated.date()

            # Calculate the number of minutes passed since the last update
            minutes_passed = (current_date - last_updated_date).days * 24 * 60
            minutes_passed += (current_date - last_updated_date).seconds // 60

            if minutes_passed >= 1:
                balance_increase = leave_balance.balance_increase
                increase_count = minutes_passed // 1  # Calculate the number of times balance_increase needs to be added
                leave_balance.balance += increase_count * balance_increase
                leave_balance.last_updated = timezone.now()
                leave_balance.save()

        pass

    class Meta:
        verbose_name = "Leave Balance"
        verbose_name_plural = "Leave Balances"



class Holiday(models.Model):


    date = models.DateField()
    occasion = models.CharField(max_length=100 ,default="None" , null=True ,blank=True)
    day = models.CharField(max_length=100)

   


    def __str__(self):
        if self.occasion == "None":
            return "No Occasion"
        return self.occasion
