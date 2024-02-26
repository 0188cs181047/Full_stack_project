from django import forms
from .models import Manager, Employee,ApplyLeave ,LeaveBalance,Holiday

class ManagerForm(forms.ModelForm):
    class Meta:
        model = Manager
        fields = ['manager_id', 'manager_name', 'manager_email', 'gender']
        labels = {
            'manager_id': 'Manager ID',
            'manager_name': 'Manager Name',
            'manager_email': 'Manager Email',
            'gender': 'Gender',
            
        }
        widgets = {
            'manager_id': forms.TextInput(attrs={'placeholder': 'Enter Manager ID'}),
            'manager_name': forms.TextInput(attrs={'placeholder': 'Enter Manager Name'}),
            'manager_email': forms.EmailInput(attrs={'placeholder': 'Enter Manager Email'}),
            'gender': forms.Select(attrs={'placeholder': 'Select Gender'}),
            
        }

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['joining_date']
        fields = ['employee_id', 'employee_name', 'employee_email', 'gender',  'manager','joining_date']
        labels = {
            'employee_id': 'Employee ID',
            'employee_name': 'Employee Name',
            'employee_email': 'Employee Email',
            'gender': 'Gender',
            'manager' : 'Manager',
           'joining_date':'Joinig Date'

        }
        widgets = {
            'employee_id': forms.TextInput(attrs={'placeholder': 'Enter Employee ID'}),
            'employee_name': forms.TextInput(attrs={'placeholder': 'Enter Employee Name'}),
            'employee_email': forms.EmailInput(attrs={'placeholder': 'Enter Employee Email'}),
            'gender': forms.Select(attrs={'placeholder': 'Select Gender'}),
            'manager': forms.Select(attrs={'placeholder': 'Select Manager'}),
            'joining_date': forms.DateInput(attrs={'type': 'date','class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),

        }



class ApplyLeaveForm(forms.ModelForm):
    # employee_email = forms.EmailField(label='Employee Email')

    class Meta:
        model = ApplyLeave
        fields = ['leave_reason', 'start_date', 'end_date', 'leave_type', 'work_from_home', 'description']
        labels = {
            'leave_reason': 'Leave Reason',
            'start_date': 'Start Date',
            'end_date': 'End Date',
            'leave_type': 'Leave Type',
            'work_from_home': 'Work from Home',
            'description': 'Description',
        }
        widgets = {
            'leave_reason': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter reason'}),
            'start_date': forms.DateInput(attrs={'type': 'date','class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
            'end_date': forms.DateInput(attrs={'type': 'date','class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
            'leave_type': forms.Select(attrs={'class': 'form-control'}),
            'work_from_home': forms.CheckboxInput(attrs={'class': 'form-check-input','style': 'margin-top: 5px;'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description'}),
        }

    def clean_leave_type(self):
        leave_type = self.cleaned_data.get('leave_type')
        work_from_home = self.cleaned_data.get('work_from_home')

        if work_from_home and not leave_type:
            return None

        return leave_type
    


class LeaveBalanceForm(forms.ModelForm):
    employee = forms.ModelChoiceField(
        queryset=Employee.objects.all(),
        label='Employee Name',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = LeaveBalance
        fields = ['leave_type', 'balance', 'balance_increase', 'work_from_home_balance']  # Include the new field
        labels = {
            'leave_type': 'Leave Type',
            'balance': 'Leave Balance',
            'balance_increase': 'Balance Increase per Month',
            'work_from_home_balance': 'Work from Home Balance'  # Label for the new field
        }
        widgets = {
            'leave_type': forms.Select(attrs={'class': 'form-control'}),
            'balance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter leave balance'}),
            'balance_increase': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter balance increase'}),
            'work_from_home_balance': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter work from home balance'}),
        }








class HolidayForm(forms.ModelForm):
    occasion = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter occasion','class': 'form-control'}))

    class Meta:
        model = Holiday
        fields = ['date', 'occasion']
        labels = {
            'occasion': 'Occasion',
            'day': 'Day',
        
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date' ,'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
        
        }

class LeaveBalanceUpdateForm(forms.ModelForm):
    class Meta:
        model = LeaveBalance
        fields = ['balance', 'balance_increase','work_from_home_balance']
        labels = {

            'balance': 'Leave Balance',
            'balance_increase': 'Balance Increase per Month',
            'work_from_home_balance': 'Work from Home Balance'  # Label for the new field
        }

        widgets = {
            'balance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter leave balance'}),
            'balance_increase': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter balance increase'}),
            'work_from_home_balance': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter work from home balance'}),
        }

