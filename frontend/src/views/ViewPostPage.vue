<template>
  <div>
    <!-- ヘッダー -->
    <GlobalMenu></GlobalMenu>

    <!-- メッセージ -->
    <Message :info="messages.informations"></Message>

    <div id="view-post-container" class="hero-body">
      <div class="container">
        <div class="columns is-vcentered has-text-centered is-marginless">
          <!-- 投稿画像 -->
          <div class="column">
            <img class="post-image" :src="post.picture_url" :alt="post.title" />
          </div>
          <div class="column">
            <!-- タイトル -->
            <p class="title">{{ post.title }}</p>

            <!-- ユーザー名 -->
            <p>posted by {{ returnAuthor.username }}</p>

            <!-- お気に入りボタン -->
            <div id="favorite-button-container">
              <div>
                <a
                  v-if="!isYourFavoritePost"
                  @click="addToFavorites"
                  class="button is-medium is-info is-outlined"
                  >お気に入りに追加</a
                >
                <a
                  v-else
                  @click="removeFromFavorites"
                  class="button is-medium is-info is-outlined"
                  >お気に入り解除</a
                >
              </div>

              <div class="mt-4">
                <!-- 投稿編集ボタン -->
                <template v-if="isYourPost">
                  <a
                    class="button is-primary is-medium"
                    @click="editPost"
                    v-if="isLoggedIn"
                    >投稿を編集</a
                  >
                </template>

                <!-- ユーザーフォローボタン -->
                <template v-else>
                  <UserFollowButton
                    :userId="returnAuthor.id"
                    :username="returnAuthor.username"
                    :page="'viewPost'"
                  ></UserFollowButton>
                </template>
              </div>
            </div>
          </div>
        </div>

        <!-- 投稿概要欄 -->
        <div
          class="
            columns
            min-height
            mb-5
            mt-6
            border-top border-bottom
            is-marginless
          "
        >
          <!-- 投稿者 -->
          <div class="column is-paddingless mt-2 min-height">
            <h6 class="mb-2 title-h6">投稿者</h6>
            <div class="display-flex">
              <!-- アイコン -->
              <div
                class="icon-box mr-3 click-cursor"
                @click="moveUserPage(returnAuthor.username)"
              >
                <img :src="returnAuthor.icon_url" />
              </div>

              <!-- ユーザー名 -->
              <div
                class="click-cursor"
                @click="moveUserPage(returnAuthor.username)"
              >
                <p>{{ returnAuthor.username }}</p>
              </div>
            </div>
          </div>

          <!-- 投稿日 -->
          <div class="column is-paddingless mt-2">
            <h6 class="mb-2 title-h6">投稿日</h6>
            <p>{{ post.posted_date }}</p>
          </div>
        </div>

        <!-- 説明文 -->
        <div class="min-height mb-4">
          <h6 class="mb-2 title-h6">説明</h6>
          <p>{{ post.text }}</p>
        </div>

        <!-- カテゴリー -->
        <div class="min-height mb-4">
          <h6 class="mb-2 title-h6">カテゴリー</h6>
          <span
            class="tag is-info is-medium mb-2 mr-2"
            v-for="category in post.category"
            :key="category"
          >
            {{ category }}
          </span>
        </div>

        <!-- 写真撮影場所 -->
        <div class="min-height mb-4">
          <h6 class="mb-2 title-h6">写真撮影場所</h6>
          <p>{{ post.zip_code }}</p>
          <p>{{ post.prefecture }}{{ post.location }}</p>
          <div ref="map" class="map"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { publicApi } from "@/api";
import api from "@/api";
import GlobalMenu from "@/components/GlobalMenu";
import Message from "@/components/Message";
import UserFollowButton from "@/components/UserFollowButton";

export default {
  computed: {
    // ログイン状態かどうか
    isLoggedIn() {
      return this.$store.getters["auth/isLoggedIn"];
    },
    // 自分の投稿かどうか
    isYourPost() {
      const username = this.$store.getters["auth/username"];
      return username === this.returnAuthor.username;
    },
    // 自分のお気に入りの投稿に入っているかどうか
    isYourFavoritePost() {
      const favoritePostsIdList =
        this.$store.getters["auth/favoritePostsIdList"];
      if (!favoritePostsIdList.length) {
        return false;
      }
      return favoritePostsIdList.includes(this.id);
    },
    // post.authorをそのまま利用するとエラーが発生するので
    // computedを介してauthorのデータを参照できるようにした
    returnAuthor() {
      if (this.post.author) {
        return this.post.author;
      } else {
        return {};
      }
    },
  },
  components: {
    GlobalMenu,
    Message,
    UserFollowButton,
  },
  // URLから投稿のIDを取得
  props: ["id"],
  data() {
    return {
      post: {},
      messages: {
        informations: [],
      },
    };
  },
  async mounted() {
    // propsのIDから投稿の詳細なデータを取得
    const { data } = await publicApi.get("/posts/" + this.id + "/", {
      params: {
        retrieve: "True",
      },
    });
    this.post = data;
    const address = this.post.prefecture + this.post.location;
    let timer = setInterval(() => {
      if (window.google) {
        clearInterval(timer);
        const geocoder = new window.google.maps.Geocoder();
        geocoder.geocode({ address }, (results, status) => {
          if (status === window.google.maps.GeocoderStatus.OK) {
            const map = new window.google.maps.Map(this.$refs.map, {
              center: results[0].geometry.location,
              zoom: 17,
            });
            new window.google.maps.Marker({
              position: results[0].geometry.location,
              map,
            });
          }
        });
      }
    }, 500);
  },
  methods: {
    // 投稿者のページへ移動
    moveUserPage(username) {
      this.$router.push({ name: "viewUser", params: { username: username } });
    },
    // 投稿を編集
    editPost() {
      this.$router.push({ name: "edit", params: { id: this.id } });
    },
    // お気に入りの投稿に追加
    addToFavorites() {
      // ログインしていない場合はログインページへ
      if (!this.$store.getters["auth/isLoggedIn"]) {
        this.$router.push({ name: "login", params: { before: "viewPost" } });
      } else {
        const favoritePostsIdList =
          this.$store.getters["auth/favoritePostsIdList"].slice(); // リストをコピー
        favoritePostsIdList.push(this.id); // コピーしたリストに表示中の投稿のIDを追加

        // データベースの情報を更新
        api
          .patch("/auth/users/me/", { favorite_posts: favoritePostsIdList })
          .then(() => {
            // vuexの状態を更新
            this.$store.dispatch(
              "auth/setFavoritePostsIdList",
              favoritePostsIdList
            );
          });
      }
    },
    // お気に入りの投稿から削除
    removeFromFavorites() {
      const oldFavoritePostsIdList =
        this.$store.getters["auth/favoritePostsIdList"];
      // 削除後のお気に入りの投稿のIDのリストを作成
      const newFavoritePostsIdList = oldFavoritePostsIdList.filter(
        (id) => id !== this.id
      );
      // データベースの情報を更新
      api
        .patch("/auth/users/me/", {
          favorite_posts: newFavoritePostsIdList,
        })
        .then(() => {
          // vuexnの状態を更新
          this.$store.dispatch("auth/removeFavoritePost", this.id); // vuexから削除
        });
    },
  },
  // メッセージの表示が必要な場合は
  // dataのmessagesに値を保存して
  // Messageコンポーネントに渡す
  beforeRouteEnter(to, from, next) {
    // 投稿編集ページからこのページに遷移してきたとき
    if (to.params.before === "editPost") {
      next((vm) => {
        // メッセージをセット
        vm.messages.informations.push("投稿を編集しました。");
      });
    } else {
      next();
    }
  },
};
</script>

<style scoped>
#view-post-container {
  padding-top: 180px;
}
#favorite-button-container {
  margin: 30px auto 20px;
  width: 90%;
}
#favorite-button-container a {
  width: 80%;
}
.post-image {
  max-width: 100%;
  height: auto;
}

.icon-box {
  height: 30px;
  width: 30px;
}
.icon-box img {
  height: 30px;
  width: 30px;
  object-fit: cover;
  border-radius: 50%;
}
.display-flex {
  display: flex;
  justify-content: flex-start;
  flex-wrap: wrap;
}
.display-flex p {
  font-weight: bold;
}
.min-height {
  min-height: 100px;
}
.click-cursor {
  cursor: pointer;
}
.click-cursor:hover {
  filter: brightness(90%);
}
.title-h6 {
  font-size: 1.2em;
}
.border-top {
  border-top: 2px solid #eeeeee;
}
.border-bottom {
  border-bottom: 2px solid #eeeeee;
}
.map {
  width: 400px;
  height: 300px;
  margin-top: 30px;
  border: 2px solid gray;
}

@media screen and (max-width: 599px) {
  .map {
    width: 100%;
    height: 250px;
  }
}
</style>