from django_filters import rest_framework as filters
from .models import Product


class ShopFilterSet(filters.FilterSet):
	price = filters.RangeFilter()
	categories = filters.CharFilter(lookup_expr='contains')

	class Meta:
		model = Product
		fields = ['price', 'categories']
