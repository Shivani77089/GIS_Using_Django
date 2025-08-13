import django_filters
from django.db.models import Q
from .models import HardwareData


class FilterTableInfo(django_filters.FilterSet):
    @classmethod
    def get_unique_base_names(cls):
        names = HardwareData.objects.values_list('name', flat=True)
        base_names = set(name.split('-')[0].upper() for name in names)
        return [(name, name) for name in sorted(base_names)]

    type = django_filters.ChoiceFilter(
        field_name="name",
        choices=lambda: FilterTableInfo.get_unique_base_names(),
        method="filter_by_base_name",
        label="Filter by Type"
    )

    def filter_by_base_name(self, queryset, name, value):
        return queryset.filter(Q(name__istartswith=value))

    class Meta:
        model = HardwareData
        fields = []


