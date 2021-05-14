<template>
  <div v-if="favoritePostsList.length">
    <PostsList :posts="favoritePostsList"></PostsList>
    <Pagination
      @paginate="setMyFavorites($event)"
      :id="''"
      class="mt-5"
    ></Pagination>
  </div>
  <div v-else>
    {{ noFavorites }}
  </div>
</template>

<script>
import api from "@/api";
import Pagination from "@/components/Pagination";
import PostsList from "@/components/PostsList";

export default {
  components: {
    Pagination,
    PostsList,
  },
  created() {
    api.get("/favorite_posts/").then((response) => {
      if (response.data.results.length) {
        this.favoritePostsList = response.data.results;
        this.$store.dispatch("pagination/setPagination", response.data);
      } else {
        this.noFavorites = "お気に入りの投稿はありません。";
      }
    });
  },
  data() {
    return {
      favoritePostsList: [],
      noFavorites: "",
    };
  },
  methods: {
    setMyFavorites(posts) {
      this.favoritePostsList = posts;
    },
  },
};
</script>