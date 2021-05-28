from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.conf import settings
from django.test.utils import override_settings
from django.utils import dateformat
from django.utils import timezone
import os

from posts.models import Post, Category
from users.models import Following
from apiv1.serializers import (
    CustomUserSerializer, PostSerializer, FollowingSerializer
)


# テストで使用する画像ファイルのパス
PICTURE_PATH = os.path.join(
    settings.BASE_DIR,
    'media',
    'tests',
    'test_picture.jpg',
)

# テストで使用するアイコンのファイルパス
ICON_PATH = os.path.join(
    settings.BASE_DIR,
    'media', 
    'tests',
    'test_icon.jpeg',
)


class TestCustomUserSerializer(TestCase):
    """CustomUserSerializerのテストクラス"""

    def test_input_valid(self):
        """入力データのバリデーション（OK）"""

        # お気に入りの投稿用の画像ファイル
        picture = SimpleUploadedFile(
            name='test.jpg',
            content=open(PICTURE_PATH, 'rb').read(),
            content_type='image/jpeg',
        )

        # お気に入りの投稿に登録する投稿を作成
        favorite_post = Post.objects.create(
            title='favorite_post',
            picture=picture,
        )

        # ユーザーアイコン用画像ファイル
        icon = SimpleUploadedFile(
            name='test_icon.jpg',
            content=open(PICTURE_PATH, 'rb').read(),
            content_type='image/jpeg',
        )

        # シリアライザに渡すデータ
        input_data = {
            'username': 'test',
            'self_introduction': 'test_introduction',
            'favorite_posts': [favorite_post.id],
            'icon': icon,
        }

        # シリアライザを作成
        serializer = CustomUserSerializer(data=input_data)

        # バリデーション結果をテスト
        self.assertTrue(serializer.is_valid())

    def test_input_invalid_if_username_is_blank(self):
        """
        入力データのバリデーション
        （NG：ユーザー名の値が空文字列の場合）
        """

        # シリアライザに渡すデータ
        input_data = {
            'username': '',
        }

        # シリアライザを作成
        serializer = CustomUserSerializer(data=input_data)

        # バリデーション結果をテスト
        self.assertFalse(serializer.is_valid())
        self.assertCountEqual(serializer.errors.keys(), ['username'])
        self.assertCountEqual(
            [x.code for x in serializer.errors['username']],
            ['blank'],
        )

    def test_input_invalid_if_username_is_null(self):
        """
        入力データのバリデーション
        （NG：ユーザー名の値がNoneの場合）
        """

        # シリアライザに渡すデータ
        input_data = {
            'username': None,
        }

        # シリアライザを作成
        serializer = CustomUserSerializer(data=input_data)

        # バリデーション結果をテスト
        self.assertFalse(serializer.is_valid())
        self.assertCountEqual(serializer.errors.keys(), ['username'])
        self.assertCountEqual(
            [x.code for x in serializer.errors['username']],
            ['null'],
        )

    @override_settings(DEBUG=True)
    def test_output_data(self):
        """出力データの内容検証"""

        # お気に入りの投稿用の画像ファイル
        picture = SimpleUploadedFile(
            name='test.jpg',
            content=open(PICTURE_PATH, 'rb').read(),
            content_type='image/jpeg',
        )

        # お気に入りの投稿に登録する投稿を作成
        favorite_post = Post.objects.create(
            title='favorite_post',
            picture=picture,
        )

        # テスト対象のデータを作成
        user = get_user_model().objects.create_user(
            username='output_user',
            password='output_password',
        )
        user.favorite_posts.add(favorite_post)
        get_user_model().objects.filter(id=user.id).update(
            self_introduction='output_introduction',
        )
        registered_date = dateformat.format(
            timezone.localtime(user.registered_date), 
            'Y年m月d日 H:i:s',
        )

        # シリアライザを作成
        serializer = CustomUserSerializer(instance=user)

        # シリアライザの出力内容を検証
        expected_data = {
            'id': str(user.id),
            'username': user.username,
            'self_introduction': user.self_introduction,
            'favorite_posts': [favorite_post.id],
            'icon_url': user.icon_url,
            'icon_filename': user.icon_filename,
            'registered_date': str(registered_date),
        }
        self.assertDictEqual(serializer.data, expected_data)


class TestPostSerializer(TestCase):
    """PostSerializerのテストクラス"""

    def setUp(self):
        """テスト用レコードを作成"""

        # 投稿用の画像ファイル
        self.picture = SimpleUploadedFile(
            name='test.jpg',
            content=open(PICTURE_PATH, 'rb').read(),
            content_type='image/jpeg',
        )

        # ユーザーを作成
        self.test_user = get_user_model().objects.create_user(
            username='test_user',
            password='test_password',
        )

        # カテゴリーを作成
        self.category = Category.objects.create(
            name='test_category',
        )
   
    def test_input_valid(self):
        """入力データのバリデーション（OK）"""

        # シリアライザに渡すデータ
        input_data = {
            'title': 'test_title',
            'text': 'test_text',
            'picture': self.picture,
            'author': self.test_user,
            'status': 'public',
            'category': [self.category.name],
            'zip_code': '1600022',
            'prefecture': '東京都',
            'location': '新宿区新宿3丁目38-1',
        }

        # シリアライザを作成
        serializer = PostSerializer(data=input_data)

        # バリデーション結果をテスト
        self.assertTrue(serializer.is_valid())

    @override_settings(DEBUG=True)
    def test_output_data(self):
        """出力データの内容検証"""

        # テスト対象のデータを作成
        post = Post.objects.create(
            title='output_title',
            text='output_text',
            picture=self.picture,
            author=self.test_user,
            status='public',
            zip_code='1600022',
            prefecture='東京都',
            location='新宿区新宿3丁目38-1',
        )
        post.category.add(self.category)
        posted_date = dateformat.format(
            timezone.localtime(post.posted_date), 
            'Y年m月d日 H:i',
        )
        author_serializer = CustomUserSerializer(post.author)

        # シリアライザを作成
        serializer = PostSerializer(instance=post)

        # シリアライザの出力内容を検証
        expected_data = {
            'id': str(post.id),
            'title': post.title,
            'text': post.text,
            'posted_date': str(posted_date),
            'picture_url': post.picture_url,
            'picture_filename': post.picture_filename,
            'author': author_serializer.data,
            'status': post.status,
            'category': [self.category.name],
            'zip_code': post.zip_code,
            'prefecture': post.prefecture,
            'location': post.location,
        }
        self.assertDictEqual(serializer.data, expected_data)


class TestFollowingSerializer(TestCase):
    """FollowingSerializerのテストクラス"""

    def test_input_valid(self):
        """入力データのバリデーション（OK）"""

        # ユーザーを作成
        test_user = get_user_model().objects.create_user(
            username='test_user',
            password='test_password',
        )

        # シリアライザに渡すデータ
        input_data = {
            'followed_user': test_user.id,
        }

        # シリアライザを作成
        serializer = FollowingSerializer(data=input_data)

        # バリデーション結果をテスト
        self.assertTrue(serializer.is_valid())

    def test_input_invalid_if_followed_user_is_null(self):
        """
        入力データのバリデーション
        （NG：followed_userが未入力の場合）
        """

        # シリアライザに渡すデータ
        input_data = {
            'followed_user': None,
        }

        # シリアライザを作成
        serializer = FollowingSerializer(data=input_data)

        # バリデーション結果をテスト
        self.assertFalse(serializer.is_valid())
        self.assertCountEqual(serializer.errors.keys(), ['followed_user'])
        self.assertCountEqual(
            [x.code for x in serializer.errors['followed_user']],
            ['null'],
        )

    @override_settings(DEBUG=True)
    def test_output_data(self):
        """出力データの内容検証"""

        # ユーザーを作成
        followed_user = get_user_model().objects.create_user(
            username='followed_user',
            password='followed_password',
        )
        following_user = get_user_model().objects.create_user(
            username='following_user',
            password='following_password',
        )

        # テスト対象のデータを作成
        following = Following.objects.create(
            followed_by=following_user,
            followed_user=followed_user,
        )
        followed_by_serializer = CustomUserSerializer(following_user)

        # シリアライザを作成
        serializer = FollowingSerializer(instance=following)

        # シリアライザの出力内容を検証
        expected_data = {
            'id': str(following.id),
            'followed_by': followed_by_serializer.data,
            'user_extra_field': {
                'username': followed_user.username,
                'icon_url': followed_user.icon_url,
            },
        }
        self.assertDictEqual(serializer.data, expected_data)
        

        