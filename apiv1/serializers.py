from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import serializers

from posts.models import Post, Category
from users.models import Following


class CustomUserSerializer(serializers.ModelSerializer):
    favorite_posts = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Post.objects.all(),
        required=False,
    )
    registered_date = serializers.DateTimeField(
        format='%Y年%m月%d日 %H:%M:%S',
        read_only=True,
    )
    icon_url = serializers.SerializerMethodField()
    icon_filename = serializers.SerializerMethodField()

    def get_icon_url(self, obj):
        return obj.icon_url

    def get_icon_filename(self, obj):
        return obj.icon_filename

    class Meta:
        model = get_user_model()
        fields = [
            'id', 'username', 'self_introduction', 
            'favorite_posts', 'icon', 'icon_url', 'icon_filename', 
            'registered_date',
        ]
        extra_kwargs = {
            'icon': {
                'write_only': True,
            }
        }


class PostSerializer(serializers.ModelSerializer):
    picture_url = serializers.SerializerMethodField()
    picture_filename = serializers.SerializerMethodField()
    author = CustomUserSerializer(read_only=True)
    posted_date = serializers.DateTimeField(
        format='%Y年%m月%d日 %H:%M', 
        read_only=True,
    )
    category = serializers.SlugRelatedField(
        slug_field='name', 
        queryset=Category.objects.all(), 
        many=True,
        allow_null=True,
        required=False,
    )

    def get_picture_url(self, obj):
        return obj.picture_url
        
    def get_picture_filename(self, obj):
        return obj.picture_filename

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'text', 'posted_date', 
            'picture_url', 'picture_filename', 'picture', 
            'author', 'status', 'category', 'zip_code', 
            'prefecture', 'location'
        ]
        extra_kwargs = {
            'picture': {
                'write_only': True,
            }
        }


class FollowingSerializer(serializers.ModelSerializer):
    followed_by = CustomUserSerializer(read_only=True)
    followed_user = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(), 
        write_only=True,
    )
    user_extra_field = serializers.SerializerMethodField()

    def get_user_extra_field(self, obj):
        return {
            'username': obj.followed_user.username, 
            'icon_url': obj.followed_user.icon_url
        }

    class Meta:
        model = Following
        fields = [
            'id', 'followed_by', 'followed_user', 'user_extra_field'
        ]
        
