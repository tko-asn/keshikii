<template>
  <div v-if="myPosts.length">
    <!-- 投稿一覧 -->
    <PostsList :posts="myPosts"></PostsList>

    <!-- ページネーション -->
    <Pagination class="mt-5" @paginate="movePage"></Pagination>
  </div>
  <div v-else>{{ noPosts }}</div>
</template>

<script>
import api from "@/api";
import Pagination from "@/components/Pagination";
import PostsList from "@/components/PostsList";

export default {
  data() {
    return {
      myPosts: [],
      noPosts: "",
    };
  },
  mounted() {
    // ログインユーザーの投稿を取得
    api.get("/users_post/").then((response) => {
      this.myPosts = response.data.results;
      // ページネーションの情報をvuexに保存
      this.$store.dispatch("pagination/setPagination", response.data);

      // 投稿がないとき
      if (!response.data.count) {
        this.noPosts = "投稿がありません。";
      }
    });
  },
  components: {
    Pagination,
    PostsList,
  },
  methods: {
    // ページネーション
    movePage(posts) {
      this.myPosts = posts;
    },
  },
};
</script>