<template>
  <div>
    <!-- ヘッダー -->
    <GlobalMenu>
      <!-- 投稿検索フォーム -->
      <div class="field has-addons search-container">
        <!-- 検索フォーム -->
        <div id="search-input" class="control">
          <input
            class="input is-small is-fullwidth"
            type="text"
            placeholder="キーワードで検索"
            v-model="searchKeyword"
          />
        </div>
        <!-- 検索ボタン -->
        <div id="search-button" class="control">
          <a
            class="button is-info is-small is-fullwidth"
            @click.prevent="clickForSearch"
          >
            検索
            <fa-icon icon="search" class="search-icon ml-2"></fa-icon>
          </a>
        </div>
      </div>
    </GlobalMenu>

    <!-- モーダル -->
    <Message :info="messages.informations"></Message>

    <div id="home-container" class="container mt-4">
      <div class="columns is-marginless">
        <!-- アプリ題名部分 -->
        <div class="column content has-text-centered">
          <h1 class="app-title a6-font-color">KESHKII</h1>
          <p class="mt-2 a6-font-color">景色共有サイト</p>
        </div>
      </div>

      <!-- フィルタ -->
      <div class="pb-5">
        <!-- フィルタ表示切り替えボタン -->
        <div id="category-menu" class="pb-3">
          <a @click="switchFilter" v-show="!filtering"
            ><fa-icon icon="filter"></fa-icon> フィルタ</a
          >
          <a @click="switchFilter" v-show="filtering"
            ><fa-icon icon="times"></fa-icon> 閉じる</a
          >
        </div>
        <!-- フィルタ部分（タブレット用） -->
        <CategoryFilter
          id="tablet-category-filter"
          class="p-4"
          v-show="filtering"
          @filterPosts="filter"
        ></CategoryFilter>
      </div>

      <div class="columns posts-container is-marginless">
        <!-- 投稿表示部分 -->
        <!-- 投稿が存在する場合 -->
        <div class="column" v-if="posts.length">
          <PostsList :posts="posts"></PostsList>
          <Pagination class="mt-6" @paginate="movePage"></Pagination>
        </div>

        <!-- 投稿が一件もない場合 -->
        <div class="column has-text-centered" v-else>
          <h3 class="a6-font-color">{{ noPosts }}</h3>
        </div>

        <!-- フィルタ部分（デスクトップ用） -->
        <CategoryFilter
          id="pc-category-filter"
          class="column is-3 ml-5"
          v-show="filtering"
          @filterPosts="filter"
        ></CategoryFilter>
      </div>
    </div>
  </div>
</template>

<script>
import { publicApi } from "@/api";
import { mapGetters } from "vuex";
import GlobalMenu from "@/components/GlobalMenu";
import Pagination from "@/components/Pagination";
import CategoryFilter from "@/components/CategoryFilter";
import PostsList from "@/components/PostsList";
import Message from "@/components/Message";

export default {
  components: {
    GlobalMenu,
    Pagination,
    CategoryFilter,
    PostsList,
    Message,
  },
  props: ["before"],
  data() {
    return {
      posts: [],
      searchKeyword: "",
      filtering: false,
      noPosts: "",
      messages: {
        informations: [],
      },
    };
  },
  computed: {
    // 投稿のリストと投稿数
    ...mapGetters("pagination", [
      "results",
      "count",
      "searchCategorys",
      "searchPrefecture",
    ]),
  },
  mounted() {
    publicApi.get("/posts/").then((response) => {
      this.posts = response.data.results;
      this.$store.dispatch("pagination/setPagination", response.data);
      // 投稿が空のとき
      if (!response.data.count) {
        this.noPosts = "投稿はありません。";
      }
    });
  },
  methods: {
    // 投稿詳細画面へ
    viewPost(postId) {
      this.$router.push({ name: "viewPost", params: { id: postId } });
    },
    // キーワード検索
    clickForSearch() {
      // 現在の検索キーワードをvuexに保存
      this.$store.dispatch(
        "pagination/registerSearchKeyword",
        this.searchKeyword
      );

      publicApi
        .get("/posts/", { params: { keyword: this.searchKeyword } })
        .then((response) => {
          // レスポンスからvuexのページネーションの情報を更新
          this.$store.dispatch("pagination/setPagination", response.data);
          this.posts = response.data.results;

          // 投稿が存在しない場合
          if (!response.data.count) {
            this.noPosts = "投稿が見つかりませんでした。";
          }
        });
    },
    switchFilter() {
      // filtering(bool)を切り替え
      // フィルタの表示・非表示を切り替え
      this.filtering = !this.filtering;
    },
    // フィルタリング後の投稿
    filter(filteringPosts) {
      this.posts = filteringPosts;
    },
    //ページネーション
    movePage(posts) {
      this.posts = posts;
    },
  },
  // メッセージの表示が必要な場合は
  // dataのmessagesに値を保存して
  // Messageコンポーネントに渡す
  beforeRouteEnter(to, from, next) {
    if (to.params.before === "create") {
      next((vm) => {
        vm.messages.informations.push("投稿しました。");
      });
    } else if (to.params.before === "logout") {
      next((vm) => {
        vm.messages.informations.push("ログアウトしました。");
      });
    } else if (to.params.before === "login") {
      next((vm) => {
        vm.messages.informations.push("ログインしました。");
      });
    } else if (to.params.before === "signup") {
      next((vm) => {
        vm.messages.informations.push("サインアップしました。");
      });
    } else if (to.params.before === "deletePost") {
      next((vm) => {
        vm.messages.informations.push("投稿を削除しました。");
      });
    } else {
      next();
    }
  },
  watch: {
    // フィルタから検索して該当する投稿がないとき
    // noPostsにメッセージを設定する
    posts(val) {
      const search =
        this.searchCategorys.length || this.searchPrefecture.length;
      // 投稿数が0かつsearchCategorysかsearchPrefectureのどちらかがtrueの場合
      // この条件でページ描画時に投稿が一件もなかったときに
      // noPostsに「投稿が見つかりませんでした。」のメッセージが代入されるのを防ぐ
      if (val.length === 0 && search) {
        this.noPosts = "投稿が見つかりませんでした。";
      }
    },
  },
  beforeRouteLeave(to, from, next) {
    // vuexの検索ワードの値を初期化
    this.$store.commit("pagination/clearSearchKeyword");
    next();
  },
};
</script>

<style scoped>
.a6-font-color {
  color: #aaaaaa;
}
.app-title {
  margin: 0;
  font-size: 4vw;
}
.search-container {
  width: 100%;
}
.posts-container {
  min-height: 400px;
}
.image-box {
  /* アスペクト比の統一 */
  width: 100%;
  padding-top: 60%;
  position: relative;
}
.image-box img {
  /* 画像のトリミング */
  position: absolute;
  width: 100%;
  height: 100%;
  object-fit: cover;
  top: 0;
}
.card {
  height: 100%;
}
#search-input {
  width: 300px;
}
#category-menu a {
  color: gray;
  margin-bottom: 0;
}
#category-menu {
  border-bottom: 3px solid #eeeeee;
  text-align: right;
}
#home-container {
  padding-top: 120px;
}
#tablet-category-filter {
  display: none;
}
.icon-box {
  height: 50px;
  width: 50px;
}
.icon-box img {
  height: 50px;
  width: 50px;
  object-fit: cover;
  border-radius: 50%;
}
@media screen and (max-width: 1024px) {
  #search-input {
    width: 80%;
  }
  #search-button {
    width: 20%;
  }
}
@media screen and (max-width: 768px) {
  .app-title {
    font-size: 5vw;
  }
  .search-icon {
    display: none;
  }
  #tablet-category-filter {
    display: block;
    margin-top: 10px;
    margin-bottom: 30px;
  }
  #pc-category-filter {
    display: none;
  }
  .icon-box {
    height: 40px;
    width: 40px;
  }
  .icon-box img {
    height: 40px;
    width: 40px;
  }
}
</style>