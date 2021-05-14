from rest_framework.permissions import BasePermission


class UsersPostPermission(BasePermission):

    # 投稿とそれを取得しようとしているユーザーのidが同じかを検証
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or request.user.is_superuser
