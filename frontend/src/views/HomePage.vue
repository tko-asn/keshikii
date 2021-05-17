<template>
  <div>
    <GlobalMenu>
      <div class="field has-addons search-container">
        <div id="search-input" class="control">
          <input
            class="input is-small is-fullwidth"
            type="text"
            placeholder="キーワードで検索"
            v-model="searchKeyword"
          />
        </div>
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
    <GlobalMessage></GlobalMessage>
    <div id="home-container" class="container mt-4">
      <div class="columns is-marginless">
        <div class="column content has-text-centered">
          <h1 class="app-title a6-font-color">KESHKII</h1>
          <p class="mt-2 a6-font-color">景色共有サイト</p>
        </div>
      </div>
      <div v-if="posts.length">
        <div class="pb-5">
          <div id="category-menu" class="pb-3">
            <a @click="switchFilter" v-show="!filtering"
              ><fa-icon icon="filter"></fa-icon> フィルタ</a
            >
            <a @click="switchFilter" v-show="filtering"
              ><fa-icon icon="times"></fa-icon> 閉じる</a
            >
          </div>
          <CategoryFilter
            id="tablet-category-filter"
            class="p-4"
            @searchForCategory="setPostsInHome($event)"
            v-show="filtering"
          ></CategoryFilter>
        </div>
        <div class="columns posts-container is-marginless">
          <div class="column">
            <PostsList :posts="posts"></PostsList>
            <Pagination
              @paginate="setPostsInHome($event)"
              class="mt-6"
            ></Pagination>
          </div>
          <CategoryFilter
            id="pc-category-filter"
            @searchForCategory="setPostsInHome($event)"
            class="column is-3 ml-5"
            v-show="filtering"
          ></CategoryFilter>
        </div>
      </div>
      <div class="mt-6 columns has-text-centered" v-else>
        <h3 class="column a6-font-color">{{ noPosts }}</h3>
      </div>
    </div>
  </div>
</template>

<script>
import { publicApi } from "@/api";
import GlobalMenu from "@/components/GlobalMenu";
import GlobalMessage from "@/components/GlobalMessage";
import Pagination from "@/components/Pagination";
import CategoryFilter from "@/components/CategoryFilter";
import PostsList from "@/components/PostsList";

export default {
  components: {
    GlobalMenu,
    GlobalMessage,
    Pagination,
    CategoryFilter,
    PostsList,
  },
  props: ["before"],
  data() {
    return {
      posts: [],
      searchKeyword: "",
      filtering: false,
      noPosts: "",
    };
  },
  mounted() {
    publicApi.get("/posts/").then((response) => {
      if (response.data.results.length) {
        this.posts = response.data.results;
        this.$store.dispatch("pagination/setPagination", response.data);
      } else {
        this.noPosts = "投稿はありません。";
      }
    });
  },
  methods: {
    viewPost(postId) {
      this.$router.push({ name: "viewPost", params: { id: postId } });
    },
    setPostsInHome(postsData) {
      // 保存済みのpostsを初期化。
      // vuexのページネーションの設定はCategoryFilterで行っている。
      this.posts = [];
      if (postsData.length) {
        this.posts = postsData;
      } else {
        this.noPosts = "投稿が見つかりませんでした。";
      }
    },
    clickForSearch() {
      publicApi
        .get("/posts/", { params: { keyword: this.searchKeyword } })
        .then((response) => {
          this.posts = response.data.results;
          if (this.posts.length) {
            this.$store.dispatch("pagination/setPagination", response.data);
            this.$store.dispatch(
              "pagination/registerSearchKeyword",
              this.searchKeyword
            );
          } else {
            this.noPosts = "投稿が見つかりませんでした。";
          }
        });
    },
    switchFilter() {
      this.filtering = !this.filtering;
    },
  },
  beforeRouteEnter(to, from, next) {
    // mountedでapiを叩くときにinterceptorsの処理でmessageが削除されるのでdataにmessageを一時退避させる。
    if (to.params.before === "create") {
      next((vm) => {
        vm.$store.dispatch("message/setAddition", {
          messageType: "info",
          process: "created",
        });
      });
    } else if (to.params.before === "logout") {
      next((vm) => {
        vm.$store.dispatch("message/setAddition", {
          messageType: "info",
          process: "afterLogout",
        });
      });
    } else if (to.params.before === "login") {
      next((vm) => {
        vm.$store.dispatch("message/setAddition", {
          messageType: "info",
          process: "login",
        });
      });
    } else {
      next();
    }
  },
  destroyed() {
    this.$store.dispatch("pagination/destroySearchKeyword");
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