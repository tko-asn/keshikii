<template>
  <div v-if="myPosts.length">
    <PostsList :posts="myPosts"></PostsList>
    <Pagination
      @paginate="setMyPosts($event)"
      :id="''"
      class="mt-5"
    ></Pagination>
  </div>
  <div v-else>
    {{ noPosts }}
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
  data() {
    return {
      myPosts: [],
      noPosts: "",
    };
  },
  mounted() {
    api.get("/users_post/").then((response) => {
      if (response.data.results.length) {
        this.myPosts = response.data.results;
        this.$store.dispatch("pagination/setPagination", response.data);
      } else {
        this.noPosts = "投稿はありません。";
      }
    });
  },
  methods: {
    setMyPosts(posts) {
      this.myPosts = posts;
    },
  },
};
</script>