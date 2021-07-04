<template>
  <div>
    <nav class="pagination is-centered tablet-none" role="navigation">
      <ul class="pagination-list">
        <nav class="pagination" role="navigation" aria-label="pagination">
          <ul class="pagination-list">
            <!-- 前ページへの移動ボタン -->
            <li>
              <a
                class="pagination-previous"
                @click="movePage(currentPage - 1)"
                v-show="hasPrevious"
                >前のページ</a
              >
              <a
                class="pagination-previous"
                :disabled="!hasPrevious"
                v-show="!hasPrevious"
                >前のページ</a
              >
            </li>

            <!-- 全ページ数が10以下の場合 -->
            <template v-if="totalPages <= 10">
              <li v-for="pageNum in totalPages" :key="pageNum">
                <a
                  :id="pageNum"
                  class="pagination-link"
                  @click="movePage(pageNum)"
                  >{{ pageNum }}</a
                >
              </li>
            </template>

            <!-- 全ページ数が10以上ある場合 -->
            <template v-else>
              <!-- 現在のページ番号が10以下の場合 -->
              <template v-if="currentPage <= 10">
                <li v-for="pageNum in 10" :key="pageNum">
                  <a
                    :id="pageNum"
                    class="pagination-link"
                    @click="movePage(pageNum)"
                  >
                    {{ pageNum }}
                  </a>
                </li>
              </template>

              <!-- 現在のページ番号が10より上の場合 -->
              <template v-else>
                <!-- 現在のページの十の位が総ページ数の十の位と等しいとき -->
                <template v-if="tensOfCurrentPage === totalPagesDivideTen">
                  <!-- 上記の条件に加えて現在のページ番号の一の位が0の時（10、20など） -->
                  <!-- この条件分岐がないと一の位が0で上記の条件を満たしているとき下のv-elseの表記になってしまう -->
                  <template v-if="firstPlaceOfCurrentPage === 0">
                    <li v-for="pageNum in 10" :key="pageNum">
                      <a
                        :id="(tensOfCurrentPage - 1) * 10 + pageNum"
                        class="pagination-link"
                        @click="
                          movePage((tensOfCurrentPage - 1) * 10 + pageNum)
                        "
                      >
                        {{ (tensOfCurrentPage - 1) * 10 + pageNum }}
                      </a>
                    </li>
                  </template>

                  <!-- 上記の条件に加えて現在のページ番号の一の位が0出ないとき（11、21など） -->
                  <template v-else>
                    <li v-for="pageNum in divisionRemainder" :key="pageNum">
                      <a
                        :id="tensOfCurrentPage * 10 + pageNum"
                        class="pagination-link"
                        @click="movePage(tensOfCurrentPage * 10 + pageNum)"
                      >
                        {{ tensOfCurrentPage * 10 + pageNum }}
                      </a>
                    </li>
                  </template>
                </template>

                <!-- 現在のページの十の位が総ページ数の十の位と等しくないとき -->
                <template v-else>
                  <li v-for="pageNum in 10" :key="pageNum">
                    <a
                      :id="tensOfCurrentPage * 10 + pageNum"
                      class="pagination-link"
                      @click="movePage(tensOfCurrentPage * 10 + pageNum)"
                    >
                      {{ tensOfCurrentPage * 10 + pageNum }}
                    </a>
                  </li>
                </template>
              </template>
            </template>

            <!-- 次ページへの移動ボタン -->
            <li>
              <a
                class="pagination-next"
                @click="movePage(currentPage + 1)"
                v-show="hasNext"
                >次のページ</a
              >
              <a class="pagination-next" :disabled="!hasNext" v-show="!hasNext"
                >次のページ</a
              >
            </li>
          </ul>
        </nav>
      </ul>
    </nav>

    <!-- タブレット用ボタン -->
    <div class="text-align-center desktop-none">
      <div>
        <a class="pagination-link is-current">{{ currentPage }}</a>
      </div>
      <a
        class="pagination-previous"
        @click="movePage(currentPage - 1)"
        v-show="hasPrevious"
      >
        前のページ
      </a>
      <a
        class="pagination-previous"
        :disabled="!hasPrevious"
        v-show="!hasPrevious"
      >
        前のページ
      </a>
      <a
        class="pagination-next"
        @click="movePage(currentPage + 1)"
        v-show="hasNext"
      >
        次のページ
      </a>
      <a class="pagination-next" :disabled="!hasNext" v-show="!hasNext">
        次のページ
      </a>
    </div>
  </div>
</template>

<script>
import api from "@/api";
import { publicApi } from "@/api";
import { mapGetters } from "vuex";

export default {
  props: {
    id: {
      type: String,
      default: "",
    },
  },
  mounted() {
    // ページ数がDOMのid
    // デフォルトでは1ページ目にis-currentクラスを付与
    document.getElementById(1).classList.add("is-current");
  },
  computed: {
    ...mapGetters("pagination", [
      "count",
      "totalPages",
      "currentPage",
      "previousPage",
      "nextPage",
      "hasPrevious",
      "hasNext",
      "searchKeyword",
      "searchCategorys",
      "searchPrefecture",
    ]),
    totalPagesDivideTen() {
      // 前ページ数を10で割った値
      return Math.floor(this.totalPages / 10);
    },
    divisionRemainder() {
      // totalPagesを10で割った余りに1を足したもの
      return this.totalPages % 10;
    },
    tensOfCurrentPage() {
      // 現在のページ番号の十の位
      return Math.floor(this.currentPage / 10);
    },
    firstPlaceOfCurrentPage() {
      // 現在のページ番号の一の位
      return this.currentPage - this.tensOfCurrentPage * 10;
    },
  },
  methods: {
    movePage(pageNumber) {
      let url = "";

      // ページによって使用するaxiosのインスタンスが違う
      let axios = {};

      if (this.$route.name === "myPosts") {
        url = "/users_post/";
        // viewsetのパーミッション: IsAuthenticated
        axios = api;
      } else if (this.$route.name === "favoritePosts") {
        url = "/favorite_posts/";
        // viewsetのパーミッション: IsAuthenticated
        axios = api;
      } else {
        url = "/posts/";
        // viewsetのパーミッション: IsAuthenticatedOrReadOnly
        axios = publicApi;
      }

      // djangoのFilterクラスのカテゴリーの指定方法の都合上
      // クエリパラメータは文字列で指定する
      // query: {} 形式ではない
      let true_url = url;

      // 検索キーワードと検索カテゴリ・検索都道府県の両方を指定するのは
      // フィルタの仕様上不可
      // 検索キーワードがある場合
      if (this.searchKeyword) {
        const keywordQuery =
          "?keyword=" + this.searchKeyword + "&page=" + pageNumber;
        true_url += keywordQuery;
        // 検索カテゴリが設定されている場合
      } else if (this.searchCategorys.length) {
        const firstCategory = this.searchCategorys[0];
        for (const category of this.searchCategorys) {
          if (category === firstCategory) {
            true_url += "?categorys=" + category;
          } else {
            true_url += "&categorys=" + category;
          }
        }
        true_url += "&page=" + pageNumber;
        // 検索キーワードも検索カテゴリも設定されていない場合
      } else {
        true_url += "?page=" + pageNumber;
      }

      // 検索都道府県が設定されている場合
      if (this.searchPrefecture) {
        true_url += "&prefecture=" + this.searchPrefecture;
      }

      // 現在のページがViewUserPageの場合
      if (this.$route.name === "viewUser") {
        true_url += "&user_id=" + this.id;
      }

      // APIへリクエストを実行
      axios.get(true_url).then((response) => {
        this.$emit("paginate", response.data.results);
        // vuexのページネーションの状態を更新
        this.$store
          .dispatch("pagination/setPagination", response.data)
          .then(() => {
            // vuexのpaginationの情報が設定され終わったら（DOMへ反映されたら）is-currentを付与する
            document.getElementById(pageNumber).classList.add("is-current");
          });
      });
    },
  },
  watch: {
    currentPage(newPage, oldPage) {
      // 現在のページの値が更新されるとis-currentを新しいページの要素に付け替える
      // is-currentを要素から除去。
      if (oldPage) {
        document.getElementById(oldPage).classList.remove("is-current");
      }
    },
  },
};
</script>

<style scoped>
.text-align-center {
  text-align: center;
}
.desktop-none {
  display: none;
}
@media screen and (max-width: 1024px) {
  .desktop-none {
    display: block;
  }
  .tablet-none {
    display: none;
  }
}
</style>