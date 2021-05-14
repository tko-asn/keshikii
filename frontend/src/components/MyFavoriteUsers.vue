<template>
  <div>
    <div v-for="favoriteUser in favoriteUsersList" :key="favoriteUser.id">
      <router-link
        :to="{ name: 'viewUser', params: { username: favoriteUser.username } }"
      >
        {{ favoriteUser.username }}
      </router-link>
    </div>
  </div>
</template>

<script>
import api from "@/api";

export default {
  mounted() {
    api.get("/favorite_users/").then((response) => {
      this.favoriteUsersList = response.data;
    });
  },
  data() {
    return {
      favoriteUsersList: [],
    };
  },
};
</script>