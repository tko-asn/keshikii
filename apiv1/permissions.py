from rest_framework.permissions import BasePermission


class UsersPostPermission(BasePermission):
    """取得した投稿がログインユーザーのものかどうか判定するクラス"""

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or request.user.is_superuser


class MyFavoritePostsPermission(BasePermission):
    """取得した投稿がログインユーザーのお気に入りかどうか判定するクラス"""

    def has_object_permission(self, request, view, obj):
        favorite_posts_list = request.user.favorite_posts.all()
        return obj in favorite_posts_list or request.user.is_superuser