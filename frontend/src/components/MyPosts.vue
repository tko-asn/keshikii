<template>
  <div v-if="count">
    <!-- 投稿一覧 -->
    <PostsList :posts="results"></PostsList>

    <!-- ページネーション -->
    <Pagination class="mt-5"></Pagination>
  </div>
  <div v-else>投稿がありません。</div>
</template>

<script>
import { mapGetters } from "vuex";
import Pagination from "@/components/Pagination";
import PostsList from "@/components/PostsList";

export default {
  components: {
    Pagination,
    PostsList,
  },
  computed: {
    // 投稿数と投稿リスト
    ...mapGetters("pagination", ["count", "results"]),
  },
};
</script>