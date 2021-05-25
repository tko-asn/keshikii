from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.utils import timezone
from django.test.utils import override_settings
import json
import os

from posts.models import Post, Category
from users.models import Following
from apiv1.serializers import (
    PostSerializer, CustomUserSerializer, FollowingSerializer
)


# テストで使用する画像ファイルのパス
PICTURE_PATH = os.path.join(
    settings.BASE_DIR,
    'media',
    'tests',
    'test_picture.jpg',
)


class TestPublicPostViewSet(APITestCase):
    """PublicPostViewSetのテストクラス"""

    # PublicPostViewSetのURL
    TARGET_URL = '/api/v1/posts/'

    def setUp(self):
        """TestPublicPostViewSetのテストメソッド用レコードを作成"""

        # テスト用ユーザーの作成
        self.user = get_user_model().objects.create_user(
            username='test_user',
            password='test_password',
        )

        # テスト用カテゴリーの作成
        self.category = Category.objects.create(
            name='test_category',
        )

        # テストで使用する画像ファイル
        self.mock_picture = SimpleUploadedFile(
            name='test.jpg',
            content=open(PICTURE_PATH, 'rb').read(),
            content_type='image/jpeg',
        )

        # Postモデルのテスト用インスタンスを作成
        self.post = Post.objects.create(
            title='test_post',
            text='test',
            status='public',
            picture=self.mock_picture,
            author=self.user,
            zip_code='1600022',
            prefecture='東京都',
            location='新宿区新宿3丁目38-1',
        )

        # テスト用カテゴリーをpostのカテゴリーに設定
        self.post.category.add(self.category)

    @override_settings(DEBUG=True)
    def test_list_success(self):
        """Postモデルの一覧取得APIへのGETリクエスト（正常系）"""

        # APIへのリクエストを実行
        response = self.client.get(
            self.TARGET_URL,
            format='json',
        )

        # JSONデータの読み込み
        content = json.loads(response.content)

        # レスポンスのステータスコードをテスト
        self.assertEqual(response.status_code, 200)

        # データベースからテスト対象のデータを取得
        posts = Post.objects.all()
       
        # シリアライザのインスタンスを作成
        serializer = PostSerializer(posts, many=True)

        # データ内容をテスト
        self.assertEqual(content['results'], serializer.data)

    @override_settings(DEBUG=True)
    def test_list_success_user_id(self):
        """
        Postモデルの一覧取得APIへのGETリクエスト
        （正常系：ユーザーIDクエリパラメータ）
        """

        # ターゲットのユーザーを作成
        target_user = get_user_model().objects.create_user(
            username='target_user',
            password='target_password',
        )

        # アクセス先URLを作成
        URL_WITH_USER_ID = self.TARGET_URL + '?user_id=' + str(target_user.id)

        # 取得する投稿を作成
        Post.objects.create(
            title='target_post',
            status='public',
            picture=self.mock_picture,
            author=target_user,
        )

        # APIへのリクエストを実行
        response = self.client.get(
            URL_WITH_USER_ID,
            format='json',
        )

        # JSONデータの読み込み
        content = json.loads(response.content)

        # レスポンスのステータスコードをテスト
        self.assertEqual(response.status_code, 200)

        # データベースからテスト対象のデータを取得
        target_post = Post.objects.filter(title='target_post')

        # シリアライザのインスタンスを作成
        serializer = PostSerializer(target_post, many=True)

        # データ内容をテスト
        self.assertEqual(content['results'], serializer.data)

    @override_settings(DEBUG=True)
    def test_list_success_public(self):
        """
        Postモデルの一覧取得APIへのGETリクエスト
        （正常系：status='public'の投稿取得）
        """

        # status='private'の非公開の投稿を作成
        private_post = Post.objects.create(
            title='private_post',
            status='private',
            picture=self.mock_picture,
            author=self.user,
        )

        # APIへのリクエストを実行
        response = self.client.get(
            self.TARGET_URL,
            format='json',
        )

        # JSONデータの読み込み
        content = json.loads(response.content)

        # レスポンスのステータスコードをテスト
        self.assertEqual(response.status_code, 200)

        # データベースからテスト対象のデータを取得
        public_posts = Post.objects.filter(status='public')
       
        # シリアライザのインスタンスを作成
        serializer = PostSerializer(public_posts, many=True)

        # データ内容をテスト
        self.assertEqual(content['results'], serializer.data)

    @override_settings(DEBUG=True)
    def test_retrieve_success(self):
        """Postモデルの個別取得APIへのGETリクエスト（正常系）"""

        # Postモデルのデータ個別取得用URL
        RETRIEVE_URL = self.TARGET_URL + str(self.post.id) + '/'

        # APIへのリクエストを実行
        response = self.client.get(
            RETRIEVE_URL,
            format='json',
        )

        # JSONデータの読み込み
        content = json.loads(response.content)

        # レスポンスのステータスコードをテスト
        self.assertEqual(response.status_code, 200)

        # データベースからテスト対象のデータを取得
        expected_post = Post.objects.get(id=self.post.id)

        # シリアライザのインスタンスを作成
        serializer = PostSerializer(expected_post)

        # データ内容をテスト
        self.assertEqual(content, serializer.data)

    @override_settings(DEBUG=True)
    def test_retrieve_success_query_params(self):
        """
        Postモデルの個別取得APIへのGETリクエスト
        （正常系：retrieve=Trueクエリパラメータ付きリクエスト）
        """
        
        # 非公開の投稿を作成
        private_post = Post.objects.create(
            title='private_post',
            status='private',
            picture=self.mock_picture,
            author=self.user,
        )

        # 非公開の投稿取得URL
        PRIVATE_RETRIEVE_URL = self.TARGET_URL + str(private_post.id) + '/?retrieve=True'

        # APIへのリクエストを実行
        response = self.client.get(
            PRIVATE_RETRIEVE_URL,
            format='json',
        )

        # JSONデータの読み込み
        content = json.loads(response.content)

        # レスポンスのステータスコードをテスト
        self.assertEqual(response.status_code, 200)

        # データベースからテスト対象のデータを取得
        expected_post = Post.objects.get(id=private_post.id)

        # シリアライザのインスタンスを作成
        serializer = PostSerializer(expected_post)

        # データ内容をテスト
        self.assertEqual(content, serializer.data)

    @override_settings(DEBUG=True)
    def test_retrieve_not_found(self):
        """
        Postモデルの個別取得APIへのGETリクエスト
        （異常系：404エラー）
        """

        # 既存のデータを削除
        Post.objects.filter(title='test_post').delete()

        # アクセス先URLを作成
        NOT_FOUND_URL = self.TARGET_URL + str(self.post.id) + '/'

        # APIへのリクエストを実行
        response = self.client.get(
            NOT_FOUND_URL,
            format='json',
        )

        # レスポンスのステータスコードをテスト
        self.assertEqual(response.status_code, 404)


    @override_settings(DEBUG=True)
    def test_retrieve_not_found_private_post(self):
        """
        Postモデルの個別取得APIへのGETリクエスト
        （異常系：retrieve=Trueクエリパラメータ無しでの
        　リクエストによる非公開の投稿取得失敗404エラー）
        """
        
        # 非公開の投稿を作成
        private_post = Post.objects.create(
            title='private_post',
            status='private',
            picture=self.mock_picture,
            author=self.user,
        )

        # クエリパラメータ無しのURLを作成
        NOT_FOUND_URL = self.TARGET_URL + str(private_post.id) + '/'

        # APIへのリクエストを実行
        response = self.client.get(
            NOT_FOUND_URL,
            format='json',
        )

        # JSONデータの読み込み
        content = json.loads(response.content)

        # レスポンスのステータスコードをテスト
        self.assertEqual(response.status_code, 404)
        

class TestMyPostViewSet(APITestCase):
    """MyPostViewSetのテストクラス"""

    TARGET_URL = '/api/v1/users_post/'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # ログインユーザーを作成
        cls.user = get_user_model().objects.create_user(
            username='test_user',
            password='test_password',
        )

    def setUp(self):
        """TestMyPostViewSetのテストメソッド用レコードを作成"""

        # テストで使用する画像ファイル
        self.mock_picture = SimpleUploadedFile(
            name='test.jpg',
            content=open(PICTURE_PATH, 'rb').read(),
            content_type='image/jpeg',
        )

        # ログインユーザーがauthorの投稿を作成
        self.my_post = Post.objects.create(
            title='my_post',
            status='public',
            picture=self.mock_picture,
            author=self.user,
        )

        # JWT認証のトークン取得
        token = str(RefreshToken.for_user(self.user).access_token)

        # ログイン
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
    
    @override_settings(DEBUG=True)
    def test_list_success(self):
        """自分の投稿一覧取得APIへのGETリクエスト（正常系）"""

        # ログインユーザーがauthorの投稿を追加で作成
        Post.objects.create(
            title='extra_my_post',
            status='public',
            picture=self.mock_picture,
            author=self.user,
        )

        # APIへのリクエストを実行
        response = self.client.get(
            self.TARGET_URL,
            format='json',
        )

        # JSONデータの読み込み
        content = json.loads(response.content)

        # レスポンスのステータスコードをテスト
        self.assertEqual(response.status_code, 200)

        # データベースからテスト対象のデータを取得
        target_posts = Post.objects.filter(author=self.user).order_by('-posted_date')

        # シリアライザのインスタンスを作成
        serializer = PostSerializer(target_posts, many=True)        

        # データ内容をテスト
        self.assertEqual(content['results'], serializer.data)

    @override_settings(DEBUG=True)
    def test_retrieve_success(self):
        """自分の投稿個別取得APIへのGETリクエスト（正常系）"""

        # URLを作成
        RETRIEVE_URL = self.TARGET_URL + str(self.my_post.id) + '/'

        # APIへのリクエストを実行
        response = self.client.get(
            RETRIEVE_URL,
            format='json',
        )

        # JSONデータの読み込み
        content = json.loads(response.content)

        # レスポンスのステータスコードをテスト
        self.assertEqual(response.status_code, 200)

        # データベースからテスト対象のデータを取得
        target_post = Post.objects.get(id=self.my_post.id)

        # シリアライザのインスタンスを作成
        serializer = PostSerializer(target_post)        

        # データ内容をテスト
        self.assertEqual(content, serializer.data)

    @override_settings(DEBUG=True)
    def test_create_success(self):
        """投稿作成APIへのPOSTリクエスト（正常系）"""

        # 投稿用画像ファイル
        uploaded_file = SimpleUploadedFile(
            'uploaded_file.jpeg', 
            content=open(PICTURE_PATH, 'rb').read(),
            content_type='multipart/form-data',
        )

        # 投稿データの作成
        params = {
            'title': 'new_post',
            'picture': uploaded_file,
        }

        # APIへのリクエストを実行
        response = self.client.post(
            self.TARGET_URL,
            params,
            format='multipart',
        )      

        # JSONデータの読み込み
        content = json.loads(response.content) 

        # データベースの状態をテスト
        self.assertEqual(Post.objects.count(), 2)

        # ステータスコードをテスト
        self.assertEqual(response.status_code, 201)

        # 投稿したデータを取得
        new_post = Post.objects.get(title='new_post')

        # シリアライザのインスタンスを作成
        serializer = PostSerializer(new_post)

        # データ内容をテスト
        self.assertEqual(content, serializer.data)

    @override_settings(DEBUG=True)
    def test_update_success(self):
        """投稿更新APIへのPUTリクエスト（正常系）"""

        # UPDATE用URLを作成
        UPDATE_URL = self.TARGET_URL + str(self.my_post.id) + '/'

        # 変更用画像ファイル
        updated_file = SimpleUploadedFile(
            'updated_file.jpeg', 
            content=open(PICTURE_PATH, 'rb').read(),
            content_type='multipart/form-data',
        )

        # 投稿変更データの作成
        params = {
            'id': str(self.my_post.id),
            'title': 'updated_post',
            'picture': updated_file,
        }

        # APIへのリクエストを実行
        response = self.client.put(
            UPDATE_URL,
            params,
            format='multipart',
        )      

        # JSONデータの読み込み
        content = json.loads(response.content) 

        # ステータスコードをテスト
        self.assertEqual(response.status_code, 200)

        # 投稿したデータを取得
        updated_post = Post.objects.get(title='updated_post')

        # シリアライザのインスタンスを作成
        serializer = PostSerializer(updated_post)

        # データ内容をテスト
        self.assertEqual(content, serializer.data)

    @override_settings(DEBUG=True)
    def test_partial_update_success(self):
        """投稿一部更新APIへのPATCHリクエスト（正常系）"""

        # PARTIAL_UPDATE用URLを作成
        PARTIAL_UPDATE_URL = self.TARGET_URL + str(self.my_post.id) + '/'

        # 投稿一部変更データの作成
        params = {
            'title': 'patch_post',
        }

        # APIへのリクエストを実行
        response = self.client.patch(
            PARTIAL_UPDATE_URL,
            params,
            format='json',
        )      

        # JSONデータの読み込み
        content = json.loads(response.content) 

        # ステータスコードをテスト
        self.assertEqual(response.status_code, 200)

        # 投稿したデータを取得
        updated_post = Post.objects.get(title='patch_post')

        # シリアライザのインスタンスを作成
        serializer = PostSerializer(updated_post)

        # データ内容をテスト
        self.assertEqual(content, serializer.data)

    @override_settings(DEBUG=True)
    def test_destroy_success(self):
        """投稿削除APIへのDELETEリクエスト（正常系）"""

        # DESTROY用URLを作成
        DEATROY_URL = self.TARGET_URL + str(self.my_post.id) + '/'

        # APIへのリクエストを実行
        response = self.client.delete(
            DEATROY_URL,
            format='json',
        )

        # データベースの状態をテスト
        self.assertEqual(Post.objects.count(), 0)

        # ステータスコードをテスト
        self.assertEqual(response.status_code, 204)

    @override_settings(DEBUG=True)
    def test_create_bad_request(self):
        """
        投稿作成APIへのPOSTリクエスト
        （異常系：バリデーションNG）
        """

        # 投稿データの作成
        params = {
            'title': 111,
            'picture': '',
        }

        # APIへのリクエストを実行
        response = self.client.post(
            self.TARGET_URL,
            params,
            format='json',
        )

        # データベースの状態をテスト
        self.assertEqual(Post.objects.count(), 1)

        # ステータスコードをテスト
        self.assertEqual(response.status_code, 400)

    @override_settings(DEBUG=True)
    def test_retrieve_not_found(self):
        """投稿個別取得APIへのGETリクエスト（異常系：404エラー）"""

        # 用意した投稿を削除
        Post.objects.filter(title='my_post').delete()

        # RETRIEVE用URLを作成
        RETRIEVE_URL = self.TARGET_URL + str(self.my_post.id) + '/'

        # APIへのリクエストを実行
        response = self.client.get(
            RETRIEVE_URL,
            format='json',
        )

        # ステータスコードをテスト
        self.assertEqual(response.status_code, 404)

    @override_settings(DEBUG=True)
    def test_update_not_found(self):
        """投稿更新APIへのPUTリクエスト（異常系：404エラー）"""

        # 用意した投稿を削除
        Post.objects.filter(title='my_post').delete()

        # UPDATE用URLを作成
        UPDATE_URL = self.TARGET_URL + str(self.my_post.id) + '/'

        # 変更用画像ファイル
        updated_file = SimpleUploadedFile(
            'updated_file.jpeg', 
            content=open(PICTURE_PATH, 'rb').read(),
            content_type='multipart/form-data',
        )

        # 変更用データを作成
        params = {
            'id': str(self.my_post.id),
            'title': 'new_post',
            'picture': updated_file,
        }

        # APIへのリクエストを実行
        response = self.client.put(
            UPDATE_URL,
            params,
            format='multipart',
        )

        # ステータスコードをテスト
        self.assertEqual(response.status_code, 404)

    @override_settings(DEBUG=True)
    def test_partial_update_not_found(self):
        """投稿一部更新APIへのPATCHリクエスト（異常系：404エラー）"""

        # 用意した投稿を削除
        Post.objects.filter(title='my_post').delete()

        # PARTIAL_UPDATE用URLを作成
        PARTIAL_UPDATE_URL = self.TARGET_URL + str(self.my_post.id) + '/'

        # 変更用データを作成
        params = {
            'title': 'new_post',
        }

        # APIへのリクエストを実行
        response = self.client.patch(
            PARTIAL_UPDATE_URL,
            params,
            format='multipart',
        )

        # ステータスコードをテスト
        self.assertEqual(response.status_code, 404)

    @override_settings(DEBUG=True)
    def test_destroy_not_found(self):
        """投稿削除APIへのDELETEリクエスト（異常系：404エラー）"""

        # 用意した投稿を削除
        Post.objects.filter(title='my_post').delete()

        # DESTROY用URLを作成
        DESTROY_URL = self.TARGET_URL + str(self.my_post.id) + '/'

        # APIへのリクエストを実行
        response = self.client.delete(
            DESTROY_URL,
            format='json',
        )

        # ステータスコードをテスト
        self.assertEqual(response.status_code, 404)

    @override_settings(DEBUG=True)
    def test_unauthorized(self):
        """
        自分の投稿モデル用APIへのリクエスト
        （異常系：認証エラー）
        GET・POSTリクエスト
        """

        # ログインユーザーをログアウト状態にする
        self.client.logout()

        # GETリクエストを実行
        get_response = self.client.get(
            self.TARGET_URL,
            format='json',
        )

        # ステータスコードをテスト
        self.assertEqual(get_response.status_code, 401)

        # 投稿用画像ファイル
        uploaded_file = SimpleUploadedFile(
            'uploaded_file.jpeg', 
            content=open(PICTURE_PATH, 'rb').read(),
            content_type='multipart/form-data',
        )

        # 投稿データの作成
        params = {
            'title': 'new_post',
            'picture': uploaded_file,
        }

        # POSTリクエストを実行
        post_response = self.client.post(
            self.TARGET_URL,
            params,
            format='multipart',
        )

        # ステータスコードをテスト
        self.assertEqual(post_response.status_code, 401)


class TestCustomUserViewSet(APITestCase):
    """CustomUserViewSetのテストクラス"""

    TARGET_URL = '/api/v1/custom_users/{}/'

    def setUp(self):
        """テストレコードの作成"""

        # テスト用ユーザーの作成
        self.user1 = get_user_model().objects.create_user(
            username='user1',
            password='user1_password',
        )

    @override_settings(DEBUG=True)
    def test_retrieve_success(self):
        """
        ユーザーモデルの個別取得APIへのGETリクエスト（正常系）
        """

        # 個別取得用URLを作成
        RETRIEVE_URL = self.TARGET_URL.format(str(self.user1.username))

        # リクエストを実行
        response = self.client.get(
            RETRIEVE_URL,
            format='json',
        )

        # JSONデータの読み込み
        content = json.loads(response.content)

        # ステータスコードをテスト
        self.assertEqual(response.status_code, 200)

        # テスト対象のデータを取得
        target_user = get_user_model().objects.get(username=self.user1.username)

        # シリアライザのインスタンスを作成
        serializer = CustomUserSerializer(target_user)

        # データ内容をテスト
        self.assertEqual(content, serializer.data)


    @override_settings(DEBUG=True)
    def test_retrieve_not_found(self):
        """
        ユーザーモデルの個別取得APIへのGETリクエスト
        （異常系：404エラー）
        """

        # URLを作成
        NOT_FOUND_URL = self.TARGET_URL.format('user2')

        # リクエストを実行
        response = self.client.get(
            NOT_FOUND_URL,
            format='json',
        )

        # ステータスコードをテスト
        self.assertEqual(response.status_code, 404)


class TestFavoritePostsListView(APITestCase):
    """FavoritePostsListViewのテストクラス"""
    
    TARGET_URL = '/api/v1/favorite_posts/'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # ログインユーザーを作成
        cls.user = get_user_model().objects.create_user(
            username='test_user',
            password='test_password',
        )

    def setUp(self):
        """テスト用レコードを作成"""

        # テストで使用する画像ファイル
        self.mock_picture = SimpleUploadedFile(
            name='test.jpg',
            content=open(PICTURE_PATH, 'rb').read(),
            content_type='image/jpeg',
        )

        # 他のユーザーを作成
        another_user = get_user_model().objects.create_user(
            username='another_user',
            password='another_password',
        )

        # お気に入りに追加する投稿を作成
        self.favorite_post = Post.objects.create(
            title='favorite_post',
            status='public',
            picture=self.mock_picture,
            author=another_user,
        )

        # ログインユーザーのお気に入りの投稿に追加
        self.user.favorite_posts.add(self.favorite_post)

        # JWT認証のトークン取得
        token = str(RefreshToken.for_user(self.user).access_token)

        # ログイン
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)


    @override_settings(DEBUG=True)
    def test_list_success(self):
        """
        自分のお気に入りの投稿一覧取得APIへのGETリクエスト
        （正常系）
        """

        # リクエストを実行
        response = self.client.get(
            self.TARGET_URL,
            format='json',
        )

        # JSONデータを読み込み
        content = json.loads(response.content)

        # ステータスコードをテスト
        self.assertEqual(response.status_code, 200)

        # 予想されるお気に入りの投稿一覧データ
        expected_posts = Post.objects.all()

        # シリアライザのインスタンスを作成
        serializer = PostSerializer(expected_posts, many=True)

        # データの内容をテスト
        self.assertEqual(content['results'], serializer.data)

    @override_settings(DEBUG=True)
    def test_unauthorized(self):
        """
        自分のお気に入りの投稿一覧取得APIへのGETリクエスト
        （異常系：認証エラー）
        """

        # ログインユーザーをログアウト状態にする
        self.client.logout()

        # リクエストを実行
        response = self.client.get(
            self.TARGET_URL,
            format='json',
        )

        # ステータスコードをテスト
        self.assertEqual(response.status_code, 401)


class TestFollowingViewSet(APITestCase):
    """FollowingViewSetのテストクラス"""

    TARGET_URL = '/api/v1/following/'

    def setUp(self):
        """テストレコードの作成"""

        # ログインユーザーの作成
        self.user = get_user_model().objects.create_user(
            username='test_user',
            password='test_password',
        )

        # 他のユーザーの作成
        self.another_user = get_user_model().objects.create_user(
            username='another_user',
            password='another_password',
        )

        # ログインユーザーのFollowingオブジェクトを作成
        self.my_following = Following.objects.create(
            followed_by=self.user,
            followed_user=self.another_user,
        )

        # 他のユーザーのFollowingオブジェクトを作成
        self.another_users_following = Following.objects.create(
            followed_by=self.another_user,
            followed_user=self.user,
        )

    @override_settings(DEBUG=True)
    def test_list_success_my_following_users(self):
        """
        Followingモデルの一覧取得APIへのGETリクエスト
        （正常系：自分のフォローしているユーザー情報の一覧取得）
        """
        
        # JWT認証のトークン取得
        token = str(RefreshToken.for_user(self.user).access_token)

        # ログイン
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        # リクエストを実行
        response = self.client.get(
            self.TARGET_URL,
            format='json',
        )

        # JSONデータの読み込み
        content = json.loads(response.content)

        # ステータスコードをテスト
        self.assertEqual(response.status_code, 200)

        # 予想されるデータを取得
        my_following_objects = Following.objects.filter(
            followed_by=self.user,
        )

        # シリアライザのインスタンスを作成
        serializer = FollowingSerializer(
            my_following_objects, 
            many=True,
        )

        # データ内容をテスト
        self.assertEqual(content, serializer.data)

    @override_settings(DEBUG=True)
    def test_list_success_another_users_following_users(self):
        """
        Followingモデルの一覧取得APIへの
        クエリパラメータ付きGETリクエスト
        （正常系：
        他のユーザーのフォローしているユーザー情報の一覧取得）
        """

        # URLを作成
        URL_WITH_QUERY_PARAMS = (
            self.TARGET_URL + '?other=' 
            + str(self.another_user.id)
        )

        # リクエストを実行
        response = self.client.get(
            URL_WITH_QUERY_PARAMS,
            format='json',
        )

        # JSONデータの読み込み
        content = json.loads(response.content)

        # ステータスコードをテスト
        self.assertEqual(response.status_code, 200)

        # 予想されるデータを取得
        another_users_following_objects = Following.objects.filter(
            followed_by=self.another_user,
        )

        # シリアライザのインスタンスを作成
        serializer = FollowingSerializer(
            another_users_following_objects, 
            many=True,
        )

        # データ内容をテスト
        self.assertEqual(content, serializer.data)

    @override_settings(DEBUG=True)
    def test_list_success_my_followers(self):
        """
        Followingモデルの一覧取得APIへの
        クエリパラメータ付きGETリクエスト
        （正常系：自分のフォロワー情報一覧取得）
        """

        # JWT認証のトークン取得
        token = str(RefreshToken.for_user(self.user).access_token)

        # ログイン
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        # URLを作成
        URL_WITH_QUERY_PARAMS = self.TARGET_URL + '?followers=True'

        # リクエストを実行
        response = self.client.get(
            URL_WITH_QUERY_PARAMS,
            format='json',
        )

        # JSONデータの読み込み
        content = json.loads(response.content)

        # ステータスコードをテスト
        self.assertEqual(response.status_code, 200)

        # 予想されるデータを取得
        my_followers = Following.objects.filter(
            followed_user=self.user,
        )

        # シリアライザのインスタンスを作成
        serializer = FollowingSerializer(
            my_followers, 
            many=True,
        )

        # データ内容をテスト
        self.assertEqual(content, serializer.data)

    @override_settings(DEBUG=True)
    def test_list_success_another_users_followers(self):
        """
        Followingモデルの一覧取得APIへの
        クエリパラメータ付きGETリクエスト
        （正常系：他のユーザーのフォロワー情報一覧取得）
        """

        # URLを作成
        URL_WITH_QUERY_PARAMS = (
            self.TARGET_URL + '?followers=True&user=' 
            + str(self.another_user.id)
        )

        # リクエストを実行
        response = self.client.get(
            URL_WITH_QUERY_PARAMS,
            format='json',
        )

        # JSONデータの読み込み
        content = json.loads(response.content)

        # ステータスコードをテスト
        self.assertEqual(response.status_code, 200)

        # 予想されるデータを取得
        another_users_followers = Following.objects.filter(
            followed_user=self.another_user,
        )

        # シリアライザのインスタンスを作成
        serializer = FollowingSerializer(
            another_users_followers, 
            many=True,
        )

        # データ内容をテスト
        self.assertEqual(content, serializer.data)

    @override_settings(DEBUG=True)
    def test_create_success(self):
        """
        Followingモデルのオブジェクト作成APIへのPOSTリクエスト
        （正常系）
        """

        # JWT認証のトークン取得
        token = str(RefreshToken.for_user(self.user).access_token)

        # ログイン
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        # ログインユーザーのフォロー対象となるテストユーザーを作成
        test_user = get_user_model().objects.create_user(
            username='test_followed_user',
            password='test_followed_password',
        )

        # Followingオブジェクトのデータを作成
        params = {
            'followed_user': test_user.id,
        }
        
        # リクエストを実行
        response = self.client.post(
            self.TARGET_URL,
            params,
            format='json',
        )

        # JSONデータの読み込み
        content = json.loads(response.content)

        # データベースの状態テスト
        self.assertEqual(Following.objects.count(), 3)

        # ステータスコードをテスト
        self.assertEqual(response.status_code, 201)

        # 予想されるデータを取得
        new_following = Following.objects.get(
            followed_by=self.user,
            followed_user=test_user,
        )

        # シリアライザのインスタンスを作成
        serializer = FollowingSerializer(
            new_following, 
        )

        # データ内容をテスト
        self.assertEqual(content, serializer.data)

    @override_settings(DEBUG=True)
    def test_destroy_success(self):
        """
        Followingモデルのオブジェクト削除APIへのDELETEリクエスト
        （正常系）
        """

        # JWT認証のトークン取得
        token = str(RefreshToken.for_user(self.user).access_token)

        # ログイン
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        # URLを作成
        DESTROY_URL = self.TARGET_URL + str(self.my_following.id) + '/'

        # リクエストを実行
        response = self.client.delete(
            DESTROY_URL,
            format='json',
        )

        # データベースの状態確認
        self.assertEqual(Following.objects.count(), 1)

        # ステータスコードをテスト
        self.assertEqual(response.status_code, 204)

    @override_settings(DEBUG=True)
    def test_unauthorized(self):
        """
        Followingモデルのオブジェクトを扱うAPIへのリクエスト
        （異常系：認証エラー）
        POST・DELETEリクエスト
        """

        # ログインユーザーのフォロー対象となるテストユーザーを作成
        test_user = get_user_model().objects.create_user(
            username='test_followed_user',
            password='test_followed_password',
        )

        # Followingオブジェクトのデータを作成
        params = {
            'followed_user': test_user.id,
        }

        # POSTリクエストを実行
        post_response = self.client.post(
            self.TARGET_URL,
            params,
            format='json',
        )

        # ステータスコードをテスト
        self.assertEqual(post_response.status_code, 401)

        # DESTROY用URLを作成
        DESTROY_URL = self.TARGET_URL + str(self.my_following.id) + '/'

        # DELETEリクエストを実行
        delete_response = self.client.delete(
            DESTROY_URL,
            format='json',
        )

        # ステータスコードをテスト
        self.assertEqual(post_response.status_code, 401)

    @override_settings(DEBUG=True)
    def test_forbidden(self):
        """
        Followingモデルのオブジェクトを扱うAPIへのリクエスト
        （異常系：403エラー）
        自分以外のユーザーのFollowingオブジェクトへのDELETEリクエスト
        """

        # JWT認証のトークン取得
        token = str(RefreshToken.for_user(self.user).access_token)

        # ログイン
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
    
        # URLを作成
        # クエリパラメータotherをつけることで他のユーザーの
        # Followingオブジェクトがget_querysetで返されるようにする
        DESTROY_URL = (
            self.TARGET_URL + str(self.another_users_following.id) 
            + '/?other=' + str(self.another_user.id)
        )

        # DELETEリクエストを実行
        delete_response = self.client.delete(
            DESTROY_URL,
            format='json',
        )

        # ステータスコードをテスト
        self.assertEqual(delete_response.status_code, 403)
        
    @override_settings(DEBUG=True)
    def test_list_success_not_authenticated(self):
        """
        Followingモデルのオブジェクト一覧取得APIへのGETリクエスト
        （正常系：ログインしていない状態での
        自分のFollowingオブジェクト一覧取得）
        """

        # リクエストを実行
        response = self.client.get(
            self.TARGET_URL,
            format='json',
        )

        # JSONデータの読み込み
        content = json.loads(response.content)

        # ステータスコードをテスト
        self.assertEqual(response.status_code, 200)

        # データ内容をテスト
        self.assertEqual(content, [])

    @override_settings(DEBUG=True)
    def test_list_success_not_authenticated_with_query_params(self):
        """
        Followingモデルのオブジェクト一覧取得APIへの
        クエリパラメータ付きGETリクエスト
        （正常系：ログインしていない状態での
        自分のフォロワー一覧取得）
        """

        # クエリパラメータ付きURLを作成
        URL_WITH_QUERY_PARAMS = self.TARGET_URL + '?followers=True'

        # リクエストを実行
        response = self.client.get(
            URL_WITH_QUERY_PARAMS,
            format='json',
        )

        # JSONデータの読み込み
        content = json.loads(response.content)

        # ステータスコードをテスト
        self.assertEqual(response.status_code, 200)

        # データ内容をテスト
        self.assertEqual(content, [])
