import django_filters
from django_filters import CharFilter
from django_filters import DateFilter
from .models import *


class ExpenseFilter(django_filters.FilterSet):
    title = CharFilter(field_name="title", lookup_expr='icontains')

    start_date = DateFilter(field_name="date", lookup_expr="gte")
    end_date = DateFilter(field_name="date", lookup_expr="lte")

    class Meta:
        model = Expense
        fields = '__all__'
        exclude = ['user', 'date', 'description', 'amount']
