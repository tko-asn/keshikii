<template>
  <!-- お気に入りの投稿が存在する場合 -->
  <div v-if="favoritePostsList.length">
    <!-- お気に入りの投稿一覧 -->
    <PostsList :posts="favoritePostsList"></PostsList>
    <!-- ページネーション -->
    <Pagination @paginate="setMyFavorites($event)" class="mt-5"></Pagination>
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
      // お気に入りの投稿が存在する場合
      if (response.data.results.length) {
        // isMountedをtrueにする
        this.$store.commit("pagination/changeIsMounted", true);

        this.favoritePostsList = response.data.results;
        this.$store
          .dispatch("pagination/setPagination", response.data)
          .then(() => {
            // stateの変更が完了したらisMountedをfalseにする
            this.$store.dispatch("pagination/setIsMounted", false);
          })
          .catch(() => {
            // beforeRouteLeaveのwhileの処理が終わらないので
            // stateの変更に失敗してもisMountedをfalseにする
            this.$store.dispatch("pagination/setIsMounted", false);
          });

        // お気に入りの投稿がない場合
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
    // ページネーションで実行
    setMyFavorites(posts) {
      this.favoritePostsList = posts;
    },
  },
};
</script>