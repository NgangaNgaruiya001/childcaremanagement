import django_filters
from django_filters import CharFilter

from .models import *

class StudentFilter(django_filters.FilterSet):
	programme = CharFilter(field_name='programme', lookup_expr='icontains')
	gender = CharFilter(field_name='gender', lookup_expr='icontains')
	email = CharFilter(field_name='email', lookup_expr='icontains')
	name = CharFilter(field_name='name', lookup_expr='icontains')
	class Meta:
		model  = Student
		fields = '__all__'