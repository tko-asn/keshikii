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
  props: ["followers", "username"],
  methods: {
    goToUsersPage(username) {
      const loginUsername = this.$store.getters["auth/username"];
      if (username === loginUsername) {
        if (this.$route.name === "mypage") {
          this.$emit("removeModalInViewFollowers");
        } else {
          this.$router.push("/mypage");
        }
      } else if (this.username !== username) {
        this.$router.push({ name: "viewUser", params: { username: username } });
      } else {
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