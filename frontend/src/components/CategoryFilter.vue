<template>
  <aside class="container-filter menu panel container">
    <div class="container-filter__container container">
      <!-- ラベル -->
      <label class="label-filter label pb-3">
        <fa-icon class="labal-filter__icon" icon="filter"></fa-icon>
        フィルタ
      </label>

      <!-- デスクトップ用検索ボタン -->
      <div class="search-button--pc columns is-marginless">
        <button
          @click="clickSearchButton"
          class="search-button__btn button is-primary column is-fullwidth"
        >
          検索
        </button>
      </div>

      <!-- 都道府県フィルタ -->
      <div class="filter-prefecture mb-5 mt-4">
        <p class="filter-prefecture__title menu-label">都道府県</p>
        <div class="filter-prefecture__select select">
          <select class="block-select" v-model="selectedPrefecture">
            <option class="block-select__item" value="">指定なし</option>
            <option
              class="block-select__item"
              v-for="prefecture in prefectureList"
              :key="prefecture"
            >
              {{ prefecture }}
            </option>
          </select>
        </div>
      </div>

      <!-- カテゴリフィルタ -->
      <div class="filter-category">
        <p class="filter-category__title menu-label">カテゴリー</p>
        <div class="filter-category__select select is-info mb-2">
          <select class="block-select" v-model="currentParentCategory">
            <option class="block-select__item" value="">カテゴリを選択</option>
            <option class="block-select__item">建物・人工物</option>
            <option class="block-select__item">自然</option>
          </select>
        </div>
        <div class="filter-category__block-child">
          <p
            class="filter-category__text-help help mb-1"
            v-show="currentParentCategory"
          >
            以下からカテゴリーを選択してください。
          </p>

          <!-- 親カテゴリ1 建物・人工物 -->
          <div
            class="checkbox-category"
            v-show="currentParentCategory === '建物・人工物'"
          >
            <label
              class="checkbox-category__label checkbox mr-2"
              v-for="category in artificial"
              :key="category"
            >
              <input
                class="checkbox-category__input"
                v-model="selectedCategoryList"
                :value="category"
                type="checkbox"
              />
              {{ category }}
            </label>
          </div>

          <!-- 親カテゴリ2 自然 -->
          <div
            class="checkbox-category"
            v-show="currentParentCategory === '自然'"
          >
            <label
              v-for="category in natural"
              :key="category"
              class="checkbox-category__label checkbox mr-5"
            >
              <input
                class="checkbox-category__input"
                v-model="selectedCategoryList"
                :value="category"
                type="checkbox"
              />
              {{ category }}
            </label>
          </div>
        </div>
      </div>

      <!-- 選択中カテゴリ表示部分 -->
      <div class="block-selected-category mt-3 mb-4">
        <p class="block-selected-category__title help">選択したカテゴリー</p>
        <span
          class="block-selected-category__tag tag is-primary mt-1 mx-1"
          v-for="category in selectedCategoryList"
          :key="category"
        >
          {{ category }}
        </span>
      </div>

      <!-- タブレット用検索ボタン -->
      <div class="search-button--tablet columns is-marginless">
        <button
          @click="clickSearchButton"
          class="search-button__btn button is-primary column is-fullwidth"
        >
          検索
        </button>
      </div>
    </div>
  </aside>
</template>

<script>
import { publicApi } from "@/api";

export default {
  data() {
    return {
      currentParentCategory: "",
      selectedCategoryList: [],
      selectedPrefecture: "",
      prefectureList: [
        "北海道",
        "青森県",
        "岩手県",
        "宮城県",
        "秋田県",
        "山形県",
        "福島県",
        "茨城県",
        "栃木県",
        "群馬県",
        "埼玉県",
        "千葉県",
        "東京都",
        "神奈川県",
        "新潟県",
        "富山県",
        "石川県",
        "福井県",
        "山梨県",
        "長野県",
        "岐阜県",
        "静岡県",
        "愛知県",
        "三重県",
        "滋賀県",
        "京都府",
        "大阪府",
        "兵庫県",
        "奈良県",
        "和歌山県",
        "鳥取県",
        "島根県",
        "岡山県",
        "広島県",
        "山口県",
        "徳島県",
        "香川県",
        "愛媛県",
        "高知県",
        "福岡県",
        "佐賀県",
        "長崎県",
        "熊本県",
        "大分県",
        "宮崎県",
        "鹿児島県",
        "沖縄県",
      ],
      artificial: ["道路", "商業施設", "ビル", "寺・神社"],
      natural: ["山", "海", "空", "湖", "星", "森林"],
    };
  },
  methods: {
    clickSearchButton() {
      // djangoのFilterクラスのカテゴリーの指定方法の都合上
      // フィルタのクエリパラメータは文字列で指定する
      // query: {}の形式では指定しない
      let query = "";

      // カテゴリが選択されている場合
      if (this.selectedCategoryList.length) {
        for (const category of this.selectedCategoryList) {
          // seletedCategoryListの最初の要素の場合
          if (category === this.selectedCategoryList[0]) {
            // ?をつける
            query += "?categorys=" + category;
          } else {
            query += "&categorys=" + category;
          }
        }
      }

      // 都道府県が選択されている場合
      if (this.selectedPrefecture) {
        // カテゴリが選択済みの場合
        if (query) {
          query += "&prefecture=" + this.selectedPrefecture;
          // カテゴリが選択されていない場合
        } else {
          query += "?prefecture=" + this.selectedPrefecture;
        }
      }

      // フィルタリング
      publicApi.get("/posts/" + query).then((response) => {
        // 絞った投稿を送信
        this.$emit("filterPosts", response.data.results);

        // ページネーションの状態を更新
        this.$store.dispatch("pagination/setPagination", response.data);

        // 検索カテゴリーの状態更新
        this.$store.dispatch(
          "pagination/registerSearchCategorys",
          this.selectedCategoryList
        );

        // 検索都道府県の状態更新
        this.$store.dispatch(
          "pagination/registerSearchPrefecture",
          this.selectedPrefecture
        );
      });
    },
  },
  destroyed() {
    // vuexの検索カテゴリと検索都道府県の値を初期化
    this.$store.dispatch("pagination/destroySearchCategorys");
    this.$store.dispatch("pagination/destroySearchPrefecture");
  },
  watch: {
    // 親カテゴリの値が変更されたら子カテゴリのリストを初期化
    // 子カテゴリは親カテゴリのどちらかのものしか選べないという仕様
    currentParentCategory() {
      this.selectedCategoryList = [];
    },
  },
};
</script>

<style scoped>
.container-filter {
  position: relative;
}

.label-filter {
  color: gray;
}

.checkbox-category {
  margin: 0 auto;
  vertical-align: middle;
}

.search-button--tablet {
  display: none;
}

@media screen and (max-width: 768px) {
  .search-button--pc {
    display: none;
  }
  .search-button--tablet {
    display: block;
  }
}
</style>