import django_filters
from .models import PollSession


class PollSessionFilter(django_filters.FilterSet):

    class Meta:
        model = PollSession
        fields = {
            'user': ['exact', 'isnull'],
            'poll': ['exact'],
        }
