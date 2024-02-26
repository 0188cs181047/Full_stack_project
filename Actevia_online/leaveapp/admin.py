from django.contrib import admin
from .models import Manager ,Employee ,ApplyLeave,LeaveBalance,Holiday

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ['manager_id', 'manager_name', 'manager_email', 'gender']


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'employee_name', 'employee_email', 'gender', 'manager', 'manager_approved')
    list_filter = ('gender', 'manager', 'manager_approved')
    search_fields = ('employee_id', 'employee_name', 'employee_email')
    readonly_fields = ('manager_name', 'manager_email')

admin.site.register(Employee, EmployeeAdmin)
    



class ApplyLeaveAdmin(admin.ModelAdmin):
    list_display = ['leave_reason', 'start_date', 'end_date', 'leave_type', 'work_from_home', 'employee', 'description', 'status']
    list_filter = ['leave_type', 'work_from_home', 'employee']
    search_fields = ['leave_reason', 'employee__employee_name']
    actions = ['approve_selected_leaves']

    def status(self, obj):
        return obj.status() if hasattr(obj, 'approved') else "N/A"

    def approve_selected_leaves(self, request, queryset):
        for leave in queryset:
            leave.approve_leave()

        self.message_user(request, "Selected leaves have been approved.")

    approve_selected_leaves.short_description = "Approve selected leaves"

admin.site.register(ApplyLeave, ApplyLeaveAdmin)





admin.site.register(LeaveBalance)


admin.site.register(Holiday)
