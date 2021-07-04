<template>
  <!-- お気に入りの投稿が存在する場合 -->
  <div v-if="favoritePostsList.length">
    <!-- お気に入りの投稿一覧 -->
    <PostsList :posts="favoritePostsList"></PostsList>
    <!-- ページネーション -->
    <Pagination @paginate="setMyFavorites" class="mt-5"></Pagination>
  </div>

  <!-- お気に入りの投稿がない場合 -->
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
      // ページネーションのvuexの情報を更新
      this.$store.dispatch("pagination/setPagination", response.data);
      this.favoritePostsList = response.data.results;

      // お気に入りの投稿がない場合
      if (!response.data.count) {
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
    // ページネーションで実行
    setMyFavorites(posts) {
      this.favoritePostsList = posts;
    },
  },
};
</script>