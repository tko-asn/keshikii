from django_filters import rest_framework as filters
from django.db.models import Q

from posts.models import Category, Post


class PostFilter(filters.FilterSet):
    """Postモデル用フィルタクラス"""

    keyword = filters.CharFilter(
        method='title_or_text_or_author_or_prefecture_or_location_filter',
    )
    categorys = filters.ModelMultipleChoiceFilter(
        field_name='category__name',
        to_field_name='name',
        queryset=Category.objects.all(),
    )

    class Meta:
        model = Post
        fields = ['keyword', 'categorys', 'prefecture']

    def title_or_text_or_author_or_prefecture_or_location_filter(
        self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) | 
            Q(text__icontains=value) | 
            Q(author__username__icontains=value) | 
            Q(prefecture__icontains=value) | 
            Q(location__icontains=value)
        )
