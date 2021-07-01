<template>
  <div>
    <a
      :class="['button', 'is-info', 'is-outlined', 'is-medium', buttonSizeClass]"
      v-if="!isYourFavoriteUser"
      @click="addToFavoriteUsers"
      >ユーザーをフォロー</a
    >
    <a
      :class="['button', 'is-info', 'is-outlined', 'is-medium', buttonSizeClass]"
      v-else
      @click="removeFromFavoriteUsers"
      >フォロー解除</a
    >
  </div>
</template>

<script>
import api from "@/api";

export default {
  props: {
    userId: {
      type: String,
    },
    username: {
      type: String,
    },
    page: {
      type: String,
      default: '',
    }
  },
  computed: {
    // 表示しているユーザーがログインユーザーのお気に入りかどうか判定
    isYourFavoriteUser() {
      // vuexからお気に入りのユーザーのデータのリストを取得
      const favoriteUsersList = this.$store.getters["auth/favoriteUsersList"];
      // お気に入りのユーザーがいないとき
      if (!favoriteUsersList.length) {
        return false;
      }

      let result = false;
      // お気に入りのユーザがいるとき
      favoriteUsersList.forEach((userInfo) => {
        // 現在表示中のユーザーがお気に入りのリストにいるとき
        if (userInfo.user_extra_field.username === this.username) {
          result = true;
        }
      });
      // 表示中のユーザーがお気に入りリストにいなかったとき
      return result;
    },
    // テンプレートのボタンのサイズのクラスをページによって変更するcomputed
    buttonSizeClass() {
      // ViewPostPageでこのコンポーネントが表示されている場合
      if (this.page === 'viewPost') {
        return 'width-80';
      }
      return '';
    }
  },
  methods: {
    addToFavoriteUsers() {
      // ログインしていない場合
      if (!this.$store.getters["auth/isLoggedIn"]) {
        // ログインページへ
        this.$router.push({ name: "login", params: { before: "viewPost" } });
      } else {
        // 表示中のユーザーのデータをデータベースに追加
        api
          .post("/following/", { followed_user: this.userId })
          .then((response) => {
            // フォローしたユーザーの情報をvuexに格納
            // response.data：{'user_extra_field': {}, 'followed_by': {}, 'id': ''}
            this.$store.dispatch("auth/setFavoriteUser", response.data);
          });
      }
    },
    // お気に入りのユーザーから削除
    removeFromFavoriteUsers() {
      // vuexからログインユーザーのfavoriteUsersListを取得
      const favoriteUsersList = this.$store.getters["auth/favoriteUsersList"];
      // 削除するユーザーのデータを格納する変数deleteUserData
      let deleteUserData = {};
      favoriteUsersList.forEach((userInfo) => {
        // このコンポーネントで表示されているユーザーと同じユーザーのデータを
        // deleteUserDataに格納
        if (userInfo.user_extra_field.username === this.username) {
          deleteUserData = userInfo;
        }
      });
      // フォローしているユーザーのデータをデータベースから削除
      api.delete("/following/" + deleteUserData.id + "/").then(() => {
        // vuexのfavoriteUsersListからも削除
        this.$store.dispatch("auth/removeFavoriteUser", deleteUserData);
      });
    },
  },
};
</script>

<style>
.width-80 {
  width: 80%;
}
</style>