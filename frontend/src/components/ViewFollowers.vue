<template>
  <div class="panel">
    <p class="panel-heading">フォロワー</p>
    <div class="scroll-block">
      <a
        v-for="follower in followers"
        :key="follower.id"
        class="panel-block columns is-marginless"
        @click="goToUsersPage(follower.username)"
      >
        <div class="column is-3-desktop is-4-tablet is-5-mobile">
          <div class="icon-box">
            <img :src="follower.icon_url" alt="icon" />
          </div>
        </div>
        <div class="column username hidden">
          <h3>{{ follower.username }}</h3>
        </div>
      </a>
    </div>
  </div>
</template>

<script>
export default {
  // propsのusernameは現在ViewUserPageまたはMyPageに表示されている
  // ユーザーのusername
  props: ["followers", "username"],
  methods: {
    goToUsersPage(username) {
      const loginUsername = this.$store.getters["auth/username"];
      // クリックされたユーザーがログインユーザー自身の場合
      if (username === loginUsername) {
        // 現在のページがマイページの場合
        if (this.$route.name === "mypage") {
          // モーダルを非表示
          this.$emit("removeModalInViewFollowers");
        } else {
          // マイページへ
          this.$router.push("/mypage");
        }
        // クリックされたユーザーが現在表示されているユーザーとは別のユーザーの場合
      } else if (this.username !== username) {
        this.$router.push({ name: "viewUser", params: { username: username } });
        // クリックされたユーザーと現在表示されているユーザーが同じ場合
      } else {
        // モーダルを非表示
        this.$emit("removeModalInViewFollowers");
      }
    },
  },
};
</script>

<style>
.panel {
  width: 100%;
  height: 100%;
}
.panel-heading {
  text-align: center;
}
.scroll-block {
  height: 499px;
  overflow-y: scroll;
}
.scroll-block a {
  border-bottom: 0.5px solid #eeeeee;
  border-radius: 0;
  width: 100%;
  max-height: 80px;
}
.hidden {
  overflow: hidden;
}
.icon-box {
  height: 50px;
  width: 50px;
}
.username {
  font-weight: bold;
  font-size: 30px;
}
.icon-box img {
  width: 50px;
  height: 50px;
  object-fit: cover;
  border-radius: 50%;
}
</style>