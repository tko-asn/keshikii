<template>
  <section class="hero welcome is-small">
    <div class="hero-body columns is-vcentered is-marginless">
      <div class="column is-2-desktop is-2-tablet">
        <div class="icon-box">
          <img :src="user.icon_url" alt="icon">
        </div>
      </div>
      <div class="column is-6-desktop">
        <h1 class="title username-h1">
          {{ user.username }}
        </h1>
      </div>
      <div class="column" id="button-container">
        <button
          class="button is-info is-medium"
          @click="goToEditProfilePage"
          v-if="isYourPage"
        >
          プロフィールを編集
        </button>
        <template v-else>
          <a
            class="button is-info is-outlined is-medium"
            v-if="!isYourFavoriteUser"
            @click="addToFavoriteUsers"
            >ユーザーをフォロー</a
          >
          <a
            class="button is-info is-outlined is-medium"
            v-else
            @click="removeFromFavoriteUsers"
            >フォロー解除</a
          >
        </template>
      </div>
    </div>
  </section>
</template>

<script>
import api from "@/api";

export default {
  props: ["user"],
  computed: {
    isYourFavoriteUser() {
      const favoriteUsersList = this.$store.getters["auth/favoriteUsersList"];
      if (favoriteUsersList.length) {
        let isYourFavoriteUser = false;
        favoriteUsersList.forEach((userInfo) => {
          if (userInfo.user_extra_field.username === this.user.username) {
            isYourFavoriteUser = true;
          }
        });
        return isYourFavoriteUser;
      } else {
        return false;
      }
    },
    isYourPage() {
      const loginUsername = this.$store.getters["auth/username"];
      return loginUsername === this.user.username;
    },
  },
  methods: {
    addToFavoriteUsers() {
      if (!this.$store.getters["auth/isLoggedIn"]) {
        this.$router.push({ name: "login", params: { before: "viewPost" } });
      } else {
        api
          .post("/following/", { followed_user: this.user.id })
          .then((response) => {
            // response.data = {'user_extra_field': {}, 'followed_by': {}, 'id': ''}
            // フォローしたユーザーの情報をvuexに格納
            this.$store.dispatch("auth/setFavoriteUser", response.data); 
          });
      }
    },
    removeFromFavoriteUsers() {
      const favoriteUsersList = this.$store.getters["auth/favoriteUsersList"];
      let deleteUserData = {};
      favoriteUsersList.forEach((userInfo) => {
        if (userInfo.user_extra_field.username === this.user.username) {
          deleteUserData = userInfo;
        }
      });
      api.delete("/following/" + deleteUserData.id + "/").then(() => {
        this.$store.dispatch("auth/removeFavoriteUser", deleteUserData); // favoriteUsersListから削除
      });
    },
    goToEditProfilePage() {
      this.$router.push({ name: "editProfile" });
    },
  },
};
</script>

<style scoped>
#button-container {
  display: flex;
  justify-content: flex-end;
}
.icon-box {
  height: 100px;
  width: 100px;
  margin: 0 auto;
}
.icon-box img {
  height: 100px;
  width: 100px;
  object-fit: cover;
  border-radius: 50%;
}
@media screen and (max-width: 768px) {
  .username-h1 {
    text-align: center;
  }
  #button-container {
    display: block;
    text-align: center;
  }
}
</style>
