from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register('posts', views.PublicPostViewSet, 'posts')
router.register('users_post', views.UsersPostViewSet, 'users-post')
router.register('custom_users', views.CustomUserViewSet)
router.register(
    'favorite_posts', views.UsersFavoritePostsViewSet,
    'favorite-posts'
)
router.register('following', views.FollowingViewSet, 'following')

app_name = 'apiv1'

urlpatterns = [
    path('', include(router.urls)),
]
