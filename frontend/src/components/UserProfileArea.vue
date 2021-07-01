<template>
  <section class="hero welcome is-small">
    <div class="hero-body columns is-vcentered is-marginless">
      <div class="column is-2-desktop is-2-tablet">
        <div class="icon-box">
          <img :src="user.icon_url" alt="icon" />
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
// import api from "@/api";
import UserFollowButton from "@/components/UserFollowButton";

export default {
  // 本コンポーネントで表示するユーザー
  props: ["user"],
  components: {
    UserFollowButton,
  },
  computed: {
    // 表示中のユーザーがログインユーザー自身かどうか
    isYourPage() {
      const loginUsername = this.$store.getters["auth/username"];
      return loginUsername === this.user.username;
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
