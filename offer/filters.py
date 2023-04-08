from django_filters import rest_framework as filters
from .models import Offer


class OfferFilter(filters.FilterSet):
    keyword = filters.CharFilter(field_name='title', lookup_expr='icontains')
    location = filters.CharFilter(field_name='address', lookup_expr='icontains')
    experience = filters.CharFilter(field_name='experience', lookup_expr='icontains')
    min_salary = filters.NumberFilter(field_name="month_salary" or 0, lookup_expr='gte')
    max_salary = filters.NumberFilter(field_name="month_salary" or 1000000, lookup_expr='lte')

    class Meta:
        model = Offer
        fields = ('keyword', 'location', 'job_type', 'experience', 'min_salary', 'max_salary')
