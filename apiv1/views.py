from django.contrib.auth import get_user_model
from django.db.models import Q
from django_filters import rest_framework as filters
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated
)
from rest_framework.response import Response
from functools import reduce
import operator

from posts.models import Post
from users.models import Following
from .serializers import (
    PostSerializer, CustomUserSerializer,
    FollowingSerializer
)
from .paginations import CustomPagination
from .filters import PostFilter
from .permissions import UsersPostPermission


class PublicPostViewSet(viewsets.ModelViewSet):
    """status='public'の投稿用ViewSet"""

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination
    filter_backends = [filters.DjangoFilterBackend]
    filter_class = PostFilter

    def get_queryset(self):
        if self.request.query_params.get('retrieve') == 'True':
            queryset = Post.objects.all()
        else:
            queryset = Post.objects.filter(status='public')

        # user_idクエリパラメータで特定のユーザーの投稿を取得
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(author__id=user_id)
        return queryset.order_by('-posted_date')


class UsersPostViewSet(viewsets.ModelViewSet):
    """自分の投稿用ViewSet"""

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, UsersPostPermission]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Post.objects.filter(
            author=self.request.user).order_by('-posted_date')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CustomUserViewSet(viewsets.ModelViewSet):
    """ユーザー情報用ViewSet"""

    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'username'


class UsersFavoritePostsViewSet(viewsets.ModelViewSet):
    """お気に入りの投稿用ViewSet"""

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        favorite_posts_list = self.request.user.favorite_posts.all()
        if not favorite_posts_list:
            return []
        return Post.objects.filter(
            reduce(operator.or_, (Q(id=x.id) for x in favorite_posts_list))
        )


class FollowingViewSet(viewsets.ModelViewSet):
    """自分のフォロワー・フォローユーザーの情報用ViewSet"""

    serializer_class = FollowingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # ユーザーのフォロワー取得
        if self.request.query_params.get('followers') == 'True':
            user_id = self.request.query_params.get('user')
            user = self.request.user
            if user_id:
                user = get_user_model().objects.get(id=user_id)
            following_list = Following.objects.filter(followed_user=user.id)
            if not following_list:
                return []
            return following_list

        # ユーザーのフォローユーザー取得
        other_user_id = self.request.query_params.get('other')
        user = self.request.user
        # 指定のユーザーのフォローユーザー取得
        if other_user_id:
            user = get_user_model().objects.get(id=other_user_id)
        following_list = user.followed_by.all()
        if not following_list:
            return []
        return following_list

    def perform_create(self, serializer):
        # followed_byフィールドはdataとして送らずviewset内で登録
        serializer.save(followed_by=self.request.user)
