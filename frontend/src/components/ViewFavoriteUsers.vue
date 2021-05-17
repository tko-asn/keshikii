<template>
  <div class="panel">
    <p class="panel-heading">フォロー中</p>
    <div class="scroll-block">
      <a
        v-for="favoriteUser in favoriteUsersList"
        :key="favoriteUser.id"
        class="panel-block columns is-marginless"
        @click="goToUsersPage(favoriteUser.user_extra_field.username)"
      >
        <div class="column is-3-desktop is-4-tablet is-5-mobile">
          <div class="icon-box">
            <img :src="favoriteUser.user_extra_field.icon_url" alt="icon" />
          </div>
        </div>
        <div class="column username hidden">
          <h3>{{ favoriteUser.user_extra_field.username }}</h3>
        </div>
      </a>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    username: {
      type: String,
      default: "",
    },
    favoriteUsers: {
      type: Array,
      default: () => [],
    },
  },
  computed: {
    favoriteUsersList() {
      if (this.$route.name === "mypage") {
        return this.$store.getters["auth/favoriteUsersList"];
      } else {
        return this.favoriteUsers;
      }
    },
  },
  methods: {
    goToUsersPage(username) {
      const loginUsername = this.$store.getters["auth/username"];
      if (username === loginUsername) {
        if (this.$route.name === "mypage") {
          this.$emit("removeModalInViewFavoriteUsers");
        } else {
          this.$router.push("/mypage");
        }
      } else if (this.username !== username) {
        this.$router.push({ name: "viewUser", params: { username: username } });
      } else {
        this.$emit("removeModalInViewFavoriteUsers");
      }
    },
  },
};
</script>

<style scoped>
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
