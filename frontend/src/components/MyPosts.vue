<template>
  <div v-if="myPosts.length">
    <!-- 投稿一覧 -->
    <PostsList :posts="myPosts"></PostsList>

    <!-- ページネーション -->
    <Pagination @paginate="setMyPosts($event)" class="mt-5"></Pagination>
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
    // ログインユーザーの投稿を取得
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
    // ページ移動した際にPaginationコンポーネントから投稿の配列を取得
    setMyPosts(posts) {
      this.myPosts = posts;
    },
  },
};
</script>