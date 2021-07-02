<template>
  <section class="hero welcome is-small">
    <div class="hero-body columns is-vcentered is-marginless">
      <!-- ユーザーアイコン -->
      <div class="column is-2-desktop is-2-tablet">
        <div class="icon-box">
          <img :src="user.icon_url" alt="icon" />
        </div>
      </div>

      <!-- ユーザー名 -->
      <div class="column is-6-desktop">
        <h1 class="title username-h1">
          {{ user.username }}
        </h1>
      </div>

      <!-- プロフィール編集・フォローボタン -->
      <div class="column" id="button-container">
        <!-- 現在のページがマイページの場合 -->
        <button
          class="button is-info is-medium"
          @click="goToEditProfilePage"
          v-if="isYourPage"
        >
          プロフィールを編集
        </button>

        <!-- 現在のページがログインユーザー以外のページの場合 -->
        <template v-else>
          <UserFollowButton
            :userId="user.id"
            :username="user.username"
          ></UserFollowButton>
        </template>
      </div>
    </div>
  </section>
</template>

<script>
import UserFollowButton from "@/components/UserFollowButton";

export default {
  // 本コンポーネントで表示するユーザー
  props: ["user"],
  components: {
    UserFollowButton,
  },
  computed: {
    // 表示中のページがマイページかどうか判定
    isYourPage() {
      // 現在のパスにmypageが含まれているかどうか
      return this.$route.path.match(/mypage/);
    },
  },
  methods: {
    // プロフィール編集画面へ
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
