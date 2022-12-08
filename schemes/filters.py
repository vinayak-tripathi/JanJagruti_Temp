import django_filters
# from .filters import ListingFilter
from .models import Schemes
from taggit.managers import TaggableManager
from django_filters import CharFilter

class ListingFilter(django_filters.FilterSet):

    class Meta:
        model = Schemes
        fields = {'nodalMinistry': ['exact'], 'category': [
            'exact'], 'uploadDate': ['lt']}
        filter_overrides = {
            TaggableManager: {'filter_class': CharFilter},
        }