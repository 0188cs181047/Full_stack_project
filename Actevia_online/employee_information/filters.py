import django_filters
from .models import Employees
from django.db.models import Q

class EmployeeFilter(django_filters.FilterSet):
    class Meta:
        model = Employees
        fields = ['department_id']