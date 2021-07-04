from django.contrib.auth import get_user_model
from django.db.models import Q
from django_filters import rest_framework as filters
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, mixins
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
from .permissions import (
    UsersPostPermission, MyFavoritePostsPermission,
    MyFollowingDataPermission,
)


class PublicPostViewSet(mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    """
    公開されている投稿取得（一覧・個別）View

    自分の投稿は扱わない

    URL: /posts/

    以下アクセス元
    ViewPostPage.vue
    HomePage.vue
    ViewUserPage.vue
    CategoryFilter.vue
    Pagination.vue
    """

    serializer_class = PostSerializer
    pagination_class = CustomPagination
    filter_backends = [filters.DjangoFilterBackend]
    filter_class = PostFilter

    def get_queryset(self):
        # ?retrieve=Trueの場合
        if self.request.query_params.get('retrieve') == 'True':
            # 非公開の投稿をquerysetに含める
            queryset = Post.objects.all()
        else:
            queryset = Post.objects.filter(status='public')

        # user_idクエリパラメータで特定のユーザーの投稿を取得
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(author__id=user_id)
        return queryset.order_by('-posted_date')


class MyPostViewSet(viewsets.ModelViewSet):
    """
    自分の投稿を扱うViewSet

    URL: /users_post/

    以下アクセス元
    EditPostPage.vue
    MyPosts.vue
    MyProfile.vue
    Pagination.vue
    CreatePostPage.vue
    """

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, UsersPostPermission]
    pagination_class = CustomPagination

    def get_queryset(self):
        # ログインユーザーの投稿のみを取得
        return Post.objects.filter(
            author=self.request.user).order_by('-posted_date')

    def perform_create(self, serializer):
        # 投稿作成時にPostモデルのauthorフィールドにはログインユーザーを登録
        serializer.save(author=self.request.user)


class CustomUserViewSet(mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    """
    自分以外のユーザー情報取得（個別）View

    URL: /custom_users/

    以下アクセス元
    ViewUserPage.vue
    """

    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'username'


class FavoritePostsListView(generics.ListAPIView):
    """
    お気に入りの投稿一覧取得APIクラス

    URL: /favorite_posts/

    以下アクセス元
    MyFavorites.vue
    Pagination.vue
    """

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, MyFavoritePostsPermission]
    pagination_class = CustomPagination

    def get_queryset(self):
        favorite_posts_list = self.request.user.favorite_posts.all()
        # ログインユーザーのお気に入りの投稿が空の場合は空のリストを返す
        if not favorite_posts_list:
            return []
        return Post.objects.filter(
            reduce(operator.or_, (Q(id=x.id) for x in favorite_posts_list))
        )


class FollowingViewSet(mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    """
    自分のフォロワー・フォローユーザーの情報取得（一覧）・作成・削除ViewSet

    URL: /following/

    以下アクセス元
    ViewUserPage.vue
    MyProfile.vue
    ViewPostPage.vue
    UserProfileArea.vue
    """

    serializer_class = FollowingSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly, MyFollowingDataPermission
    ]

    def get_queryset(self):
        # 以下はユーザーのフォロワー取得のための処理

        # クエリパラメータに?follower=Trueがある場合
        if self.request.query_params.get('followers') == 'True':
            user_id = self.request.query_params.get('user')
            
            # クエリパラメータにuserがある場合
            # 他のユーザーのフォロワーのデータを取得したいときの処理
            if user_id:
                # user変数にidがuser_idのユーザーオブジェクトを代入
                user = get_user_model().objects.get(id=user_id)

            # ユーザーがログイン済みの場合
            # ログインユーザー自身のフォロワーのデータを取得したいときの処理
            elif self.request.user.is_authenticated:
                # user変数にログインユーザーを代入
                user = self.request.user
            else:
                return []
            
            following_list = Following.objects.filter(followed_user=user.id)
            # 指定のユーザーのフォロワーがいない場合
            if not following_list:
                return []
            return following_list

        # 以下はユーザーのフォローしているユーザー取得のための処理

        other_user_id = self.request.query_params.get('other')
        # クエリパラメータにotherがある場合
        # 他のユーザーのフォローしているユーザーのデータを取得する際の処理
        if other_user_id:
            # otherに指定されているidのユーザーオブジェクトを取得
            user = get_user_model().objects.get(id=other_user_id)

        # ログイン済みの場合
        # 自分のフォローしているユーザーのデータを取得するための処理
        elif self.request.user.is_authenticated:
            user = self.request.user
        else:
            return []
        
        following_list = user.followed_by.all()
        # 指定のユーザーのフォローしているユーザーがいない場合
        if not following_list:
            return []
        return following_list

    def perform_create(self, serializer):
        # followed_byフィールドはdataとして送らずviewset内で登録
        serializer.save(followed_by=self.request.user)
