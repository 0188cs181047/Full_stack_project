from django.shortcuts import get_object_or_404, render ,HttpResponse ,redirect

from .forms import ManagerForm, EmployeeForm,ApplyLeaveForm,LeaveBalanceForm,HolidayForm ,LeaveBalanceUpdateForm
from .models import Manager, Employee ,ApplyLeave ,LeaveBalance,Holiday
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Q
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from cridential.views import app_access_required



# Create your views here.

@app_access_required('Approval Management')
@login_required
def home(request):
    return render(request ,"leave/home.html")


@app_access_required('Approval Management')
@login_required
def leave_manager_list(request):
    manager = Manager.objects.all()

    return render(request ,"leave/leave_manager_list.html",{"manager":manager})



@app_access_required('Approval Management')
@login_required
def manager_create(request):
    if request.method == 'POST':
        form = ManagerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("leave_manager_list")
    else:
        form = ManagerForm()

    return render(request, 'leave/manager_form.html', {'form': form})



@app_access_required('Approval Management')
@login_required
def delete_selected_managers(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_items')
        if selected_ids:
            try:
                Manager.objects.filter(id__in=selected_ids).delete()
                messages.success(request, 'Selected managers have been deleted.')
            except Exception as e:
                messages.error(request, f'An error occurred while deleting managers: {str(e)}')
        else:
            messages.warning(request, 'No managers were selected for deletion.')

    return redirect('leave_manager_list')


@app_access_required('Approval Management')
def update_manager(request, pk):
    manager = get_object_or_404(Manager, id=pk)

    if request.method == 'POST':
        form = ManagerForm(request.POST, instance=manager)
        if form.is_valid():
            form.save()
            return redirect('leave_manager_list')
    else:
        form = ManagerForm(instance=manager)

    return render(request, 'leave/update_manager.html', {'form': form, 'manager': manager})






@app_access_required('Approval Management')
@login_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'leave/employee_list.html', {'employees': employees})


@app_access_required('Approval Management')
@login_required
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('leave_employee_list') 
    else:
        form = EmployeeForm()
    
    return render(request, 'leave/create_employee.html', {'form': form})




@app_access_required('Approval Management')
@login_required
def delete_selected_employees(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_items')
        if selected_ids:
            try:
                Employee.objects.filter(id__in=selected_ids).delete()
                messages.success(request, 'Selected managers have been deleted.')
            except Exception as e:
                messages.error(request, f'An error occurred while deleting managers: {str(e)}')
        else:
            messages.warning(request, 'No managers were selected for deletion.')

    return redirect('leave_employee_list')



@app_access_required('Approval Management')
@login_required
def update_employee(request, pk):
    employee = get_object_or_404(Employee, id=pk)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('leave_employee_list')
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'leave/update_employee.html', {'form': form, 'manager': employee})



@app_access_required('Approval Management')
@login_required
def show_all_apply_leave(request):
    if request.user.is_superuser or request.user.is_staff:
        all_leave = ApplyLeave.objects.all().select_related('employee')
    else:
        user_email = request.user.email
        all_leave = ApplyLeave.objects.filter(employee__employee_email=user_email)
    username = request.user.username
    return render(request, 'leave/show_all_apply_leave.html', {"leave": all_leave, "username": username})




from django.core.mail import send_mail

from datetime import timedelta
from datetime import date
from datetime import timedelta


def count_weekdays(start_date, end_date):
    count = 0
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() < 5:  # Monday to Friday (0 to 4)
            count += 1
        current_date += timedelta(days=1)
    return count


@login_required
def apply_leave_form(request):
    form = ApplyLeaveForm()
    current_date = date.today()

    try:
        employee = Employee.objects.get(employee_email=request.user.email)
        manager_email = employee.manager.manager_email
    except Employee.DoesNotExist:
        manager_email = None

    if request.method == "POST":
        form = ApplyLeaveForm(request.POST)
        if form.is_valid():
            # employee_email = form.cleaned_data['employee_email']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            # if request.user.email == employee_email:
            if start_date and end_date and start_date <= end_date:
                    try:
                        # employee = Employee.objects.get(employee_email=employee_email)
                        apply_leave = form.save(commit=False)
                        apply_leave.employee = employee
                        apply_leave.employee_name = employee.employee_name

                        if apply_leave.work_from_home and not apply_leave.leave_type:
                            apply_leave.leave_type = None

                        apply_leave.save()

                        # Calculate the number of days taken
                        if start_date and end_date and start_date <= end_date:
                            duration = count_weekdays(start_date, end_date)
                            print(f"Number of weekdays taken: {duration}")
                        else:
                            form.add_error(None, 'Invalid start date or end date.')

                        # Calculate the number of days taken for each leave type
                        leave_type_days_taken = {}
                        leave_data = ApplyLeave.objects.filter(
                            employee=employee,
                            start_date__lte=end_date,
                            end_date__gte=start_date,
                        )
                        for leave in leave_data:
                            leave_type = leave.leave_type
                            days_taken = count_weekdays(leave.start_date, leave.end_date)

                            leave_type_days_taken[leave_type] = leave_type_days_taken.get(leave_type, 0) + days_taken

                        # Print the number of days taken for each leave type
                        for leave_type, days_taken in leave_type_days_taken.items():
                            print(f"Leave Type: {leave_type}, Days Taken: {days_taken}")


                        # Send email notification to the manager
                        manager = employee.manager
                        manager_email = manager.manager_email
                        subject = 'Leave Application Notification'
                        message = (
                            f"Hello {manager.manager_name},\n\n"
                            f"An employee has applied for leave. Here are the details:\n\n"
                            f"Employee Username: {employee.employee_name}\n"
                            f"Employee ID: {employee.employee_id}\n"
                            f"Start Date: {apply_leave.start_date}\n"
                            f"End Date: {apply_leave.end_date}\n"
                        )

                        if apply_leave.work_from_home:
                            message += "Work from Home: Work From Home\n"
                        else:
                            message += f"Leave Type: {apply_leave.get_leave_type_display()}\n"

                        message += (
                            "Please take appropriate action on this leave application.\n\n"
                            "Thank you."
                        )
                        send_mail(subject, message, 'noreply@example.com', [manager_email])

                        return redirect('leave_approval') 

                    except Employee.DoesNotExist:
                        form.add_error('employee_email', 'Employee with this email does not exist.')
            else:
                form.add_error(None, 'Invalid start date or end date.')
        # else:
        #     form.add_error('employee_email', 'You can only apply leave for your own email.')

    return render(request, 'leave/apply_leave_form.html', {"form": form ,"current_date": current_date})




from django.core.exceptions import ObjectDoesNotExist

@app_access_required('Approval Management')
@login_required
def leave_approval(request):
    user_email = request.user.email
    username = request.user.username

    manager = Manager.objects.filter(manager_email=user_email).first()
    specific_employee_email = user_email
    employee = Employee.objects.filter(employee_email=specific_employee_email).first()

    if not manager:
        if employee:
            employee_leave = ApplyLeave.objects.filter(employee=employee)
            manager_leave = ApplyLeave.objects.none()
        else:
            employee_leave = ApplyLeave.objects.none()
            manager_leave = ApplyLeave.objects.filter(Q(employee__manager=manager) | Q(approved=True))
    else:
        employee_leave = ApplyLeave.objects.none()
        manager_leave = ApplyLeave.objects.filter(Q(employee__manager=manager) | Q(approved=True))

    if request.method == "POST":
        leave_id = request.POST.get("leave_id")
        action = request.POST.get("action")
        leave = get_object_or_404(ApplyLeave, pk=leave_id)

        # ...

        if action == "approve":
            leave.approve_leave()
            leave.approved = True
            leave.save()

            # Calculate the number of weekdays taken
            start_date = leave.start_date
            end_date = leave.end_date
            duration = count_weekdays(start_date, end_date)

            subject = 'Leave Application Approval'
            message = (
                f"Hello {leave.employee.employee_name},\n\n"
                "Your request has been approved by your manager.\n\n"
                f"Number of weekdays taken: {duration}\n\n"
            )

            if leave.leave_type:
                message += f"Leave Type: {leave.get_leave_type_display()}\n"
            else:
                message += "Work from Home: Work From Home\n"

            message += "\nThank you."

            send_mail(subject, message, 'noreply@example.com', [leave.employee.employee_email])

            print("Leave application approved")  # Print the approval message
            print(f"Number of weekdays taken: {duration}")

            # Calculate the number of weekdays taken for each leave type
            leave_type_days_taken = {}
            leave_data = ApplyLeave.objects.filter(
                employee=leave.employee,
                start_date__lte=leave.end_date,
                end_date__gte=leave.start_date,
            )
            for leave in leave_data:
                leave_type = leave.leave_type
                days_taken = count_weekdays(leave.start_date, leave.end_date)

                leave_type_days_taken[leave_type] = leave_type_days_taken.get(leave_type, 0) + days_taken

            # Print the number of weekdays taken for each leave type
            for leave_type, days_taken in leave_type_days_taken.items():
                print(f"Leave Type: {leave_type}, Weekdays Taken: {days_taken}")

            if leave.work_from_home:
                leave.employee.work_from_home_balance -= duration
                leave.employee.save()

                
# ...


        elif action == "reject":
            return render(request, 'leave/reject_form.html', {'leave': leave})# Print the rejection message
        # Print the rejection message

        elif action == "cancel":
            # Get the leave details before deleting it
            leave_details = {
                "employee_name": leave.employee.employee_name,
                "employee_email": leave.employee.employee_email
            }
            
            # Delete the leave instance
            
            leave.delete()
            
            # Send the cancellation email
            subject = 'Leave Application Cancellation'
            message = (
                f"Hello {leave_details['employee_name']},\n\n"
                "Your request has been canceled.\n\n"
                "Thank you."
            )
            send_mail(subject, message, 'noreply@example.com', [leave_details['employee_email']])
            
            return redirect("leave_approval") 
        

    # Exclude specific leave data of the user if they are both an employee and a manager
    if manager and employee:
        employee_leave = ApplyLeave.objects.filter(employee=employee)
        manager_leave = manager_leave.exclude(employee=employee)

    context = {
        "employee_leaves": employee_leave,
        "manager_leaves": manager_leave,
        "username": username,
        "manager_email": user_email,
        "is_manager": True if manager else False  
    }
    print("="*50)
    # Print leave type, days taken, and leave balance for each leave after approval
    for leave in employee_leave:
        leave_type = leave.leave_type
        try:
            leave_balance = LeaveBalance.objects.filter(employee=employee, leave_type=leave_type).latest('last_updated')
        except ObjectDoesNotExist:
            leave_balance = None

        if leave_balance:
            start_date = leave.start_date
            end_date = leave.end_date

            # Calculate the number of weekdays taken
            days_taken = count_weekdays(start_date, end_date)

            # Exclude Saturdays and Sundays from the total count
            current_date = start_date
            while current_date <= end_date:
                if current_date.weekday() < 5:  # Monday to Friday
                    days_taken -= 1
                current_date += datetime.timedelta(days=1)

            print(f"Leave Type: {leave_type}")
            print(f"Days Taken (excluding weekends): {days_taken}")
            print("="*50)



    return render(request, 'leave/leave_approval.html', context)



# @app_access_required('Approval Management')
# @login_required
# def leave_approval(request):
#     user_email = request.user.email
#     username = request.user.username

#     manager = Manager.objects.filter(manager_email=user_email).first()
#     specific_employee_email = user_email
#     employee = Employee.objects.filter(employee_email=specific_employee_email).first()

#     if not manager:
#         if employee:
#             employee_leave = ApplyLeave.objects.filter(employee=employee)
#             manager_leave = ApplyLeave.objects.none()
#         else:
#             employee_leave = ApplyLeave.objects.none()
#             manager_leave = ApplyLeave.objects.filter(Q(employee__manager=manager) | Q(approved=True))
#     else:
#         employee_leave = ApplyLeave.objects.none()
#         manager_leave = ApplyLeave.objects.filter(Q(employee__manager=manager) | Q(approved=True))

#     if request.method == "POST":
#         leave_id = request.POST.get("leave_id")
#         action = request.POST.get("action")
#         leave = get_object_or_404(ApplyLeave, pk=leave_id)

#         # ...

#         if action == "approve":
#             leave.approve_leave()
#             leave.approved = True
#             leave.save()

#             # Calculate the number of weekdays taken
#             start_date = leave.start_date
#             end_date = leave.end_date
#             duration = count_weekdays(start_date, end_date)

#             subject = 'Leave Application Approval'
#             message = (
#                 f"Hello {leave.employee.employee_name},\n\n"
#                 "Your request has been approved by your manager.\n\n"
#                 f"Number of weekdays taken: {duration}\n\n"
#             )

#             if leave.leave_type:
#                 message += f"Leave Type: {leave.get_leave_type_display()}\n"
#             else:
#                 message += "Work from Home: Work From Home\n"

#             message += "\nThank you."

#             send_mail(subject, message, 'noreply@example.com', [leave.employee.employee_email])

#             print("Leave application approved")  # Print the approval message
#             print(f"Number of weekdays taken: {duration}")

#             # Calculate the number of weekdays taken for each leave type
#             leave_type_days_taken = {}
#             leave_data = ApplyLeave.objects.filter(
#                 employee=leave.employee,
#                 start_date__lte=leave.end_date,
#                 end_date__gte=leave.start_date,
#             )
#             for leave in leave_data:
#                 leave_type = leave.leave_type
#                 days_taken = count_weekdays(leave.start_date, leave.end_date)

#                 leave_type_days_taken[leave_type] = leave_type_days_taken.get(leave_type, 0) + days_taken

#             # Print the number of weekdays taken for each leave type
#             for leave_type, days_taken in leave_type_days_taken.items():
#                 print(f"Leave Type: {leave_type}, Weekdays Taken: {days_taken}")
                
# # ...


#         elif action == "reject":
#             return render(request, 'leave/reject_form.html', {'leave': leave})# Print the rejection message
#         # Print the rejection message

#         elif action == "cancel":
#             # Get the leave details before canceling it
#             leave_details = {
#                 "employee_name": leave.employee.employee_name,
#                 "employee_email": leave.employee.employee_email
#             }
            
#             # Update the leave status to canceled and save the leave
#             leave.approved = None
#             leave.save()
            
#             # Calculate the number of weekdays taken
#             start_date = leave.start_date
#             end_date = leave.end_date
#             duration = count_weekdays(start_date, end_date)
            
#             # Add the canceled days back to the leave balance
#             leave_type = leave.leave_type
#             leave_balance = LeaveBalance.objects.filter(
#                 employee=leave.employee,
#                 leave_type=leave_type
#             ).latest('last_updated')
#             leave_balance.balance += duration
#             leave_balance.save()
            
#             # Send the cancellation email
#             subject = 'Leave Application Cancellation'
#             message = (
#                 f"Hello {leave_details['employee_name']},\n\n"
#                 "Your request has been canceled.\n\n"
#                 f"Number of weekdays canceled: {duration}\n\n"
#                 "Thank you."
#             )
#             send_mail(subject, message, 'noreply@example.com', [leave_details['employee_email']])
#             return redirect("leave_approval") 
        

#     # Exclude specific leave data of the user if they are both an employee and a manager
#     if manager and employee:
#         employee_leave = ApplyLeave.objects.filter(employee=employee)
#         manager_leave = manager_leave.exclude(employee=employee)

#     context = {
#         "employee_leaves": employee_leave,
#         "manager_leaves": manager_leave,
#         "username": username,
#         "manager_email": user_email,
#         "is_manager": True if manager else False  
#     }
#     print("="*50)
#     # Print leave type, days taken, and leave balance for each leave after approval
#     for leave in employee_leave:
#         leave_type = leave.leave_type
#         try:
#             leave_balance = LeaveBalance.objects.filter(employee=employee, leave_type=leave_type).latest('last_updated')
#         except ObjectDoesNotExist:
#             leave_balance = None

#         if leave_balance:
#             start_date = leave.start_date
#             end_date = leave.end_date

#             # Calculate the number of weekdays taken
#             days_taken = count_weekdays(start_date, end_date)

#             # Exclude Saturdays and Sundays from the total count
#             current_date = start_date
#             while current_date <= end_date:
#                 if current_date.weekday() < 5:  # Monday to Friday
#                     days_taken -= 1
#                 current_date += datetime.timedelta(days=1)

#             print(f"Leave Type: {leave_type}")
#             print(f"Days Taken (excluding weekends): {days_taken}")
#             print("="*50)



#     return render(request, 'leave/leave_approval.html', context)



def reject_leave(request):
    if request.method == 'POST':
        leave_id = request.POST.get('leave_id')
        rejection_reason = request.POST.get('rejection_reason')
        leave = ApplyLeave.objects.get(pk=leave_id)
        leave.reject_leave(rejection_reason)

        subject = 'Leave Application Rejection'
        message = (
            f"Hello {leave.employee.employee_name},\n\n"
            "Your request has been rejected by your manager.\n\n"
            f"Rejection Reason: {rejection_reason}\n\n"
            "Thank you."
        )
        send_mail(subject, message, 'noreply@example.com', [leave.employee.employee_email])

        print("Leave application rejected")  # Print the rejection message

    return redirect("leave_approval")  # Redirect to the leave approval page or any desired URL




@app_access_required('Approval Management')
@login_required
def profile(request):
    custom_user = request.user
    employee = Employee.objects.filter(employee_email=custom_user.email).first()
    manager = Manager.objects.filter(manager_email=custom_user.email).first()
    employees_count = Employee.objects.filter(manager=manager).count
    
    return render(request, "leave/profile.html", {"employee": employee, "manager": manager,"username": request.user.username , "employees_count": employees_count,"usermaill": request.user.email})






from django.db.models import Sum
from django.db.models import Avg
from datetime import datetime, timedelta
from django.utils import timezone








from django.db.models import Q
from datetime import timedelta, date
from django.db.models import Sum

def count_current_total_leave_balance(employee, leave_balance):
    # Calculate the increase in leave balance per month for earned leave
    if leave_balance['leave_type'] == 'EL':
        balance_increase = leave_balance['balance_increase']
        current_date = date.today()
        months_passed = (current_date.year - employee.joining_date.year) * 12 + current_date.month - employee.joining_date.month
        return leave_balance['total_balance'] + balance_increase * months_passed
    else:
        return leave_balance['total_balance']
    
from datetime import timedelta

def count_pending_work_from_home(employee, leave_balance):
    leave_type_data = ApplyLeave.objects.filter(
        Q(employee=employee) | Q(employee__employee_email=employee.employee_email),
        leave_type=leave_balance['leave_type'],
        approved=None,
        work_from_home=True,
    ).count()
    leave_balance['pending_work_from_home'] = leave_type_data



# @app_access_required('Approval Management')
# @login_required
# def show_leave_balance(request):
#     email = request.user.email
#     employee = Employee.objects.filter(employee_email=email).first()
#     employee_name = employee.employee_name if employee else None
#     leave_balances_with_employee = LeaveBalance.objects.filter(employee=employee)

#     leave_type_days_taken = {}
#     leave_data = ApplyLeave.objects.filter(
#         employee__employee_email=email,
#         approved=True
#     )

#     for leave in leave_data:
#         leave_type = leave.leave_type
#         duration = (leave.end_date - leave.start_date).days + 1

#         # Calculate the number of weekdays taken
#         current_date = leave.start_date
#         weekdays_taken = 0
#         while current_date <= leave.end_date:
#             if current_date.weekday() < 5:  # Monday to Friday
#                 weekdays_taken += 1
#             current_date += timedelta(days=1)

#         days_taken = leave_type_days_taken.get(leave_type, 0) + weekdays_taken
#         leave_type_days_taken[leave_type] = days_taken

#     distinct_leave_balances = []

#     if not employee or employee.manager:
#         leave_balances = LeaveBalance.objects.filter(
#             Q(employee=employee),
#         ).values('leave_type').annotate(
#             total_balance=Sum('balance'),
#             balance_increase=Sum('balance_increase')  # Sum instead of Avg for balance_increase
#         ).order_by('leave_type')

#         for leave_balance in leave_balances:
#             leave_type = leave_balance['leave_type']
#             days_taken = leave_type_days_taken.get(leave_type, 0)
#             leave_balance['total_balance'] -= days_taken

#             distinct_leave_balances.append({
#                 'leave_type': leave_type,
#                 'total_balance': count_current_total_leave_balance(employee, leave_balance),
#                 'days_taken': days_taken,
#                 'balance_increase': leave_balance['balance_increase']
#             })

#     total_current_leave_balance = sum(leave_balance['total_balance'] for leave_balance in distinct_leave_balances)

#     total_taken_leave = 0
#     total_pending_leave_count = 0
#     pending_leave_count = 0

#     for leave_balance in distinct_leave_balances:
#         leave_type_name = dict(ApplyLeave.LEAVE_CHOICES).get(leave_balance['leave_type'])
#         current_leave_balance = leave_balance['total_balance']

#         if not employee or employee.manager or (employee.manager and employee.manager.manager):
#             leave_type_data = ApplyLeave.objects.filter(
#                 Q(employee=employee) |
#                 Q(employee__employee_email=email),
#                 leave_type=leave_balance['leave_type'],
#                 approved=True
#             )
#             pending_leave_count = ApplyLeave.objects.filter(
#                 Q(employee=employee) |
#                 Q(employee__employee_email=email),
#                 leave_type=leave_balance['leave_type'],
#                 approved=None
#             ).count()

#             total_days_taken = sum(
#                 count_weekdays(leave.start_date, leave.end_date)
#                 for leave in leave_type_data
#             )

#             total_taken_leave += total_days_taken
#             total_pending_leave_count += pending_leave_count

#             print(f"Leave Type: {leave_type_name}")
#             print(f"Current Leave Balance: {current_leave_balance}")
#             print(f"Total Days Taken (excluding weekends): {total_days_taken}")

#             leave_balance['pending_leave_count'] = pending_leave_count

#     return render(request, 'leave/show_leave_balance.html', {
#         'leave_balances': distinct_leave_balances,
#         'total_leave_balance': total_current_leave_balance,
#         'username': request.user.username,
#         'employee_name': employee_name,
#         'total_days_taken': total_taken_leave,
#         'pending_leave_count': pending_leave_count,
#         'total_pending_leave_count': total_pending_leave_count,
#         'employee': employee,
#     })

def show_leave_balance(request):
    email = request.user.email
    employee = Employee.objects.filter(employee_email=email).first()
    employee_name = employee.employee_name if employee else None
    leave_balances_with_employee = LeaveBalance.objects.filter(employee=employee)

    leave_type_days_taken = {}
    leave_data = ApplyLeave.objects.filter(
        employee__employee_email=email,
        approved=True
    )

    for leave in leave_data:
        leave_type = leave.leave_type
        duration = (leave.end_date - leave.start_date).days + 1

        # Calculate the number of weekdays taken
        current_date = leave.start_date
        weekdays_taken = 0
        while current_date <= leave.end_date:
            if current_date.weekday() < 5:  # Monday to Friday
                weekdays_taken += 1
            current_date += timedelta(days=1)

        days_taken = leave_type_days_taken.get(leave_type, 0) + weekdays_taken
        leave_type_days_taken[leave_type] = days_taken

    distinct_leave_balances = []

    if not employee or employee.manager:
        leave_balances = LeaveBalance.objects.filter(
            Q(employee=employee),
        ).values('leave_type').annotate(
            total_balance=Sum('balance'),
            balance_increase=Sum('balance_increase'),  # Sum instead of Avg for balance_increase
            work_from_home_balance=Sum('work_from_home_balance')  # Add work_from_home_balance
        ).order_by('leave_type')

        for leave_balance in leave_balances:
            leave_type = leave_balance['leave_type']
            days_taken = leave_type_days_taken.get(leave_type, 0)
            leave_balance['total_balance'] -= days_taken

            distinct_leave_balances.append({
                'leave_type': leave_type,
                'total_balance': count_current_total_leave_balance(employee, leave_balance),
                'days_taken': days_taken,
                'balance_increase': leave_balance['balance_increase'],
                'work_from_home_balance': leave_balance['work_from_home_balance']  # Include work_from_home_balance
            })

    total_current_leave_balance = sum(leave_balance['total_balance'] for leave_balance in distinct_leave_balances)

    total_taken_leave = 0
    total_pending_leave_count = 0
    pending_leave_count = 0
    

    for leave_balance in distinct_leave_balances:
        leave_type_name = dict(ApplyLeave.LEAVE_CHOICES).get(leave_balance['leave_type'])
        current_leave_balance = leave_balance['total_balance']

        if not employee or employee.manager or (employee.manager and employee.manager.manager):
            leave_type_data = ApplyLeave.objects.filter(
                Q(employee=employee) |
                Q(employee__employee_email=email),
                leave_type=leave_balance['leave_type'],
                approved=True
            )
            pending_leave_count = ApplyLeave.objects.filter(
                Q(employee=employee) |
                Q(employee__employee_email=email),
                leave_type=leave_balance['leave_type'],
                approved=None
            ).count()

            total_days_taken = sum(
                count_weekdays(leave.start_date, leave.end_date)
                for leave in leave_type_data
            )

            total_taken_leave += total_days_taken
            total_pending_leave_count += pending_leave_count

            print(f"Leave Type: {leave_type_name}")
            print(f"Current Leave Balance: {current_leave_balance}")
            print(f"Total Days Taken (excluding weekends): {total_days_taken}")

            leave_balance['pending_leave_count'] = pending_leave_count
            count_pending_work_from_home(employee, leave_balance)

            
            work_from_home_balance = leave_balance['work_from_home_balance']
            work_from_home_pending = max(0, leave_balance['pending_leave_count'] - work_from_home_balance)
            leave_balance['work_from_home_pending'] = work_from_home_pending


    total_work_from_home_balance = sum(
        leave_balance['work_from_home_balance'] for leave_balance in distinct_leave_balances
    )
    total_work_from_home_pending = sum(
        leave_balance['work_from_home_pending'] for leave_balance in distinct_leave_balances
    )

    return render(request, 'leave/show_leave_balance.html', {
        'leave_balances': distinct_leave_balances,
        'total_leave_balance': total_current_leave_balance,
        'total_work_from_home_balance': total_work_from_home_balance,
        'total_work_from_home_pending': total_work_from_home_pending,
        'username': request.user.username,
        'employee_name': employee_name,
        'total_days_taken': total_taken_leave,
        'pending_leave_count': pending_leave_count,
        'total_pending_leave_count': total_pending_leave_count,
        'employee': employee,
    })





@app_access_required('Approval Management')
@login_required
def leave_balance_create(request):
    if request.method == 'POST':
        form = LeaveBalanceForm(request.POST)
        if form.is_valid():
            leave_balance = form.save(commit=False)
            leave_balance.employee = form.cleaned_data['employee']
            leave_balance.save()
            return redirect('leave_balances')
    else:
        form = LeaveBalanceForm()

    # Filter the employee queryset based on the selected employee
    selected_employee = request.GET.get('employee')
    if selected_employee:
        form.fields['employee'].queryset = Employee.objects.filter(id=selected_employee)

    context = {'form': form}
    return render(request, 'leave/leave_balance_create.html', context)


import datetime



def leave_balance_view(request):
    leave_balances = LeaveBalance.objects.all().select_related('employee')

    context = {
        'leave_balances': leave_balances
    }
    return render(request, 'leave/leave_balance.html', context)



def leave_balance_update(request, pk):
    leave_balance = get_object_or_404(LeaveBalance, pk=pk)

    if request.method == 'POST':
        form = LeaveBalanceUpdateForm(request.POST, instance=leave_balance)
        if form.is_valid():
            form.save()
            return redirect('leave_balances')
    else:
        form = LeaveBalanceUpdateForm(instance=leave_balance)

    context = {
        'form': form
    }

    return render(request, 'leave/leave_balance_update.html', context)



def leave_balance_delete(request):
    if request.method == 'POST':
        leave_balance_ids = request.POST.getlist('leave_balance_ids')
        LeaveBalance.objects.filter(id__in=leave_balance_ids).delete()
    
    return redirect('leave_balances')



@app_access_required('Approval Management')
def my_holiday(request):
    holiday = Holiday.objects.all()

    return render(request, 'leave/holiday.html' ,{"holiday":holiday})

# def my_holiday(request):
#     form = DateRangeForm(request.POST or None)
#     selected_range = None
#     all_dates = []
#     selected_category = None

#     if request.method == 'POST' and form.is_valid():
#         start_date = form.cleaned_data['start_date']
#         end_date = form.cleaned_data['end_date']
#         category = form.cleaned_data['category']

#         holidays = Holiday.objects.filter(date__range=[start_date, end_date])
#         if category:
#             holidays = holidays.filter(category=category)

#         selected_range = f"Selected Range: {start_date} - {end_date}"  # Store the selected range
#         selected_category = category  # Store the selected category
        
#         # Generate a list of all dates between the selected range
#         all_dates = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
#     else:
#         # If no date range is selected, display data for the current month
#         today = timezone.now().date()
#         start_date = today.replace(day=1)
#         end_date = today
#         holidays = Holiday.objects.filter(date__range=[start_date, end_date])
#         selected_range = f"Current Month: {start_date} - {end_date}"  # Store the selected range
        
#         # Generate a list of all dates between the selected range
#         all_dates = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

#     context = {
#         'form': form,
#         'holidays': holidays,
#         'selected_range': selected_range,
#         'all_dates': all_dates,
#         'selected_category': selected_category,
#     }
#     return render(request, 'leave/holiday.html', context)



@app_access_required('Approval Management')
@login_required
def create_holiday(request):
    if request.method == 'POST':
        form = HolidayForm(request.POST)
        if form.is_valid():
            holiday = form.save(commit=False)  # Create the Holiday instance but don't save it yet
            holiday.date = form.cleaned_data['date']  # Get the selected date from the form
            holiday.day = holiday.date.strftime('%A')  # Get the day of the week for the selected date
            holiday.save()  # Save the Holiday instance with the updated day field
            return redirect("my_holiday")
    else:
        form = HolidayForm()
    return render(request, 'leave/create_holiday.html', {'form': form})


def apply_wfh_form(request):
    form = ApplyLeaveForm()
    current_date = date.today()

    try:
        employee = Employee.objects.get(employee_email=request.user.email)
        manager_email = employee.manager.manager_email
    except Employee.DoesNotExist:
        manager_email = None

    if request.method == "POST":
        form = ApplyLeaveForm(request.POST)
        if form.is_valid():
            apply_leave = form.save(commit=False)
            apply_leave.employee = employee
            apply_leave.employee_name = employee.employee_name
            apply_leave.leave_type = None  # Set leave_type as None for WFH application
            apply_leave.save()

            # Send email notification to the manager
            manager = employee.manager
            manager_email = manager.manager_email
            subject = 'Work from Home Application Notification'
            message = (
                f"Hello {manager.manager_name},\n\n"
                f"An employee has applied for Work from Home. Here are the details:\n\n"
                f"Employee Username: {employee.employee_name}\n"
                f"Employee ID: {employee.employee_id}\n"
                f"Start Date: {apply_leave.start_date}\n"
                f"End Date: {apply_leave.end_date}\n"
                "Work from Home: Work From Home\n"
                "Please take appropriate action on this WFH application.\n\n"
                "Thank you."
            )
            send_mail(subject, message, 'noreply@example.com', [manager_email])
            return redirect('leave_approval')

    return render(request, 'leave/apply_wfh_form.html', {"form": form, "current_date": current_date})
