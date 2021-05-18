<template>
  <div>
    <GlobalMenu></GlobalMenu>
    <Message :info="messages.informations"></Message>
    <div id="view-post-container" class="hero-body">
      <div class="container">
        <div class="columns is-vcentered has-text-centered is-marginless">
          <div class="column">
            <img class="post-image" :src="post.picture_url" :alt="post.title" />
          </div>
          <div class="column">
            <p class="title">{{ post.title }}</p>
            <p>posted by {{ returnAuthor.username }}</p>
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
                <template v-if="isAuthor">
                  <a
                    class="button is-primary is-medium"
                    @click="editPost"
                    v-if="isLoggedIn && isYourPost"
                    >投稿を編集</a
                  >
                </template>
                <template v-else>
                  <a
                    v-if="!isYourFavoriteUser"
                    @click="addToFavoriteUsers"
                    class="button is-medium is-info is-outlined"
                    >ユーザーをフォロー</a
                  >
                  <a
                    v-else
                    @click="removeFromFavoriteUsers"
                    class="button is-medium is-info is-outlined"
                    >フォロー解除</a
                  >
                </template>
              </div>
            </div>
          </div>
        </div>
        <div
          class="columns min-height mb-5 mt-6 border-top border-bottom is-marginless"
        >
          <div class="column is-paddingless mt-2 min-height">
            <h6 class="mb-2 title-h6">投稿者</h6>
            <div class="display-flex">
              <div
                class="icon-box mr-3 click-cursor"
                @click="moveUserPage(returnAuthor.username)"
              >
                <img :src="returnAuthor.icon_url" />
              </div>
              <div
                class="click-cursor"
                @click="moveUserPage(returnAuthor.username)"
              >
                <p>{{ returnAuthor.username }}</p>
              </div>
            </div>
          </div>
          <div class="column is-paddingless mt-2">
            <h6 class="mb-2 title-h6">投稿日</h6>
            <p>{{ post.posted_date }}</p>
          </div>
        </div>
        <div class="min-height mb-4">
          <h6 class="mb-2 title-h6">説明</h6>
          <p>{{ post.text }}</p>
        </div>
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
        <div class="min-height mb-4">
          <h6 class="mb-2 title-h6">写真撮影場所</h6>
          <p>{{ post.zip_code }}</p>
          <p>{{ post.prefecture }}{{ post.location }}</p>
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

export default {
  computed: {
    isLoggedIn() {
      return this.$store.getters["auth/isLoggedIn"];
    },
    isYourPost() {
      const username = this.$store.getters["auth/username"];
      return username === this.returnAuthor.username;
    },
    isYourFavoritePost() {
      const favoritePostsIdList = this.$store.getters[
        "auth/favoritePostsIdList"
      ];
      if (favoritePostsIdList.length) {
        return favoritePostsIdList.includes(this.id);
      } else {
        return false;
      }
    },
    isYourFavoriteUser() {
      const favoriteUsersList = this.$store.getters["auth/favoriteUsersList"];
      let isYourFavoriteUser = false;
      if (favoriteUsersList.length) {
        favoriteUsersList.forEach((userInfo) => {
          if (
            userInfo.user_extra_field.username === this.returnAuthor.username
          ) {
            isYourFavoriteUser = true;
          }
        });
        return isYourFavoriteUser;
      } else {
        return isYourFavoriteUser;
      }
    },
    returnAuthor() {
      if (this.post.author) {
        return this.post.author;
      } else {
        return {};
      }
    },
    isAuthor() {
      const loginUsername = this.$store.getters["auth/username"];
      return this.returnAuthor.username === loginUsername;
    },
  },
  components: {
    GlobalMenu,
    Message,
  },
  props: ["id"],
  data() {
    return {
      post: {},
      messages: {
        informations: [],
      },
    };
  },
  mounted() {
    publicApi
      .get("/posts/" + this.id + "/", {
        params: {
          retrieve: "True",
        },
      })
      .then((response) => {
        this.post = response.data;
      });
  },
  methods: {
    moveUserPage(username) {
      this.$router.push({ name: "viewUser", params: { username: username } });
    },
    editPost() {
      this.$router.push({ name: "edit", params: { id: this.id } });
    },
    addToFavorites() {
      if (!this.$store.getters["auth/isLoggedIn"]) {
        this.$router.push({ name: "login", params: { before: "viewPost" } });
      } else {
        const favoritePostsIdList = this.$store.getters[
          "auth/favoritePostsIdList"
        ].slice(); // リストをコピー
        favoritePostsIdList.push(this.id); // コピーしたリストに追加
        api
          .patch(
            "/custom_users/" + this.$store.getters["auth/username"] + "/",
            { favorite_posts: favoritePostsIdList }
          )
          .then(() => {
            this.$store.dispatch(
              "auth/setFavoritePostsIdList",
              favoritePostsIdList
            ); // vuexにて置き換え
          });
      }
    },
    removeFromFavorites() {
      const oldFavoritePostsIdList = this.$store.getters[
        "auth/favoritePostsIdList"
      ];
      const newFavoritePostsIdList = oldFavoritePostsIdList.filter(
        (id) => id !== this.id
      );
      api
        .patch("/custom_users/" + this.$store.getters["auth/username"] + "/", {
          favorite_posts: newFavoritePostsIdList,
        })
        .then(() => {
          this.$store.dispatch("auth/removeFavoritePost", this.id); // vuexから削除
        });
    },
    addToFavoriteUsers() {
      if (!this.$store.getters["auth/isLoggedIn"]) {
        this.$router.push({ name: "login" });
      } else {
        api
          .post("/following/", { followed_user: this.returnAuthor.id })
          .then((response) => {
            // response.data: {'user_extra_field': {}, 'followed_by': {}, 'id': ''}
            this.$store.dispatch("auth/setFavoriteUser", response.data);
          });
      }
    },
    removeFromFavoriteUsers() {
      const favoriteUsersList = this.$store.getters["auth/favoriteUsersList"];
      let deleteUserData = {};
      favoriteUsersList.forEach((userInfo) => {
        if (userInfo.user_extra_field.username === this.returnAuthor.username) {
          deleteUserData = userInfo;
        }
      });
      api.delete("/following/" + deleteUserData.id + "/").then(() => {
        // favoriteUsersListから削除
        this.$store.dispatch("auth/removeFavoriteUser", deleteUserData);
      });
    },
  },
  // メッセージの表示が必要な場合は
  // dataのmessagesに値を保存して
  // Messageコンポーネントに渡す
  beforeRouteEnter(to, from, next) {
    if (to.params.before === "editPost") {
      next((vm) => {
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
</style>