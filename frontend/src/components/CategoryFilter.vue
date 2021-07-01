<template>
  <aside class="menu panel container" id="filter-container">
    <div class="container">
      <!-- ラベル -->
      <label id="filter-label" class="label pb-3">
        <fa-icon icon="filter"></fa-icon>
        フィルタ
      </label>

      <!-- デスクトップ用検索ボタン -->
      <div class="columns is-marginless" id="pc-search-button">
        <button
          @click="clickSearchButton"
          class="button is-primary column is-fullwidth"
        >
          検索
        </button>
      </div>

      <!-- 都道府県フィルタ -->
      <div class="mb-5 mt-4">
        <p class="menu-label">都道府県</p>
        <div class="select">
          <select v-model="selectedPrefecture">
            <option value="">指定なし</option>
            <option>北海道</option>
            <option>青森県</option>
            <option>岩手県</option>
            <option>宮城県</option>
            <option>秋田県</option>
            <option>山形県</option>
            <option>福島県</option>
            <option>茨城県</option>
            <option>栃木県</option>
            <option>群馬県</option>
            <option>埼玉県</option>
            <option>千葉県</option>
            <option>東京都</option>
            <option>神奈川県</option>
            <option>新潟県</option>
            <option>富山県</option>
            <option>石川県</option>
            <option>福井県</option>
            <option>山梨県</option>
            <option>長野県</option>
            <option>岐阜県</option>
            <option>静岡県</option>
            <option>愛知県</option>
            <option>三重県</option>
            <option>滋賀県</option>
            <option>京都府</option>
            <option>大阪府</option>
            <option>兵庫県</option>
            <option>奈良県</option>
            <option>和歌山県</option>
            <option>鳥取県</option>
            <option>島根県</option>
            <option>岡山県</option>
            <option>広島県</option>
            <option>山口県</option>
            <option>徳島県</option>
            <option>香川県</option>
            <option>愛媛県</option>
            <option>高知県</option>
            <option>福岡県</option>
            <option>佐賀県</option>
            <option>長崎県</option>
            <option>熊本県</option>
            <option>大分県</option>
            <option>宮崎県</option>
            <option>鹿児島県</option>
            <option>沖縄県</option>
          </select>
        </div>
      </div>

      <!-- カテゴリフィルタ -->
      <div>
        <p class="menu-label">カテゴリー</p>
        <div class="select is-info mb-2">
          <select v-model="currentParentCategory">
            <option value="">カテゴリを選択</option>
            <option>建物・人工物</option>
            <option>自然</option>
          </select>
        </div>
        <div>
          <p class="help mb-1" v-show="currentParentCategory">
            以下からカテゴリーを選択してください。
          </p>

          <!-- 親カテゴリ1 建物・人工物 -->
          <div
            class="category-checkbox"
            v-show="currentParentCategory === '建物・人工物'"
          >
            <label class="checkbox mr-2">
              <input
                v-model="selectedCategoryList"
                value="道路"
                type="checkbox"
              />
              道路
            </label>
            <label class="checkbox mr-2">
              <input
                v-model="selectedCategoryList"
                value="商業施設"
                type="checkbox"
              />
              商業施設
            </label>
            <label class="checkbox mr-2">
              <input
                v-model="selectedCategoryList"
                value="ビル"
                type="checkbox"
              />
              ビル
            </label>
            <label class="checkbox">
              <input
                v-model="selectedCategoryList"
                value="寺・神社"
                type="checkbox"
              />
              寺・神社
            </label>
          </div>

          <!-- 親カテゴリ2 自然 -->
          <div
            class="category-checkbox"
            v-show="currentParentCategory === '自然'"
          >
            <label class="checkbox mr-5">
              <input
                v-model="selectedCategoryList"
                value="山"
                type="checkbox"
              />
              山
            </label>
            <label class="checkbox mr-5">
              <input
                v-model="selectedCategoryList"
                value="海"
                type="checkbox"
              />
              海
            </label>
            <label class="checkbox mr-5">
              <input
                v-model="selectedCategoryList"
                value="空"
                type="checkbox"
              />
              空
            </label>
            <label class="checkbox mr-5">
              <input
                v-model="selectedCategoryList"
                value="湖"
                type="checkbox"
              />
              湖
            </label>
            <label class="checkbox mr-5">
              <input
                v-model="selectedCategoryList"
                value="星"
                type="checkbox"
              />
              星
            </label>
            <label class="checkbox">
              <input
                v-model="selectedCategoryList"
                value="森林"
                type="checkbox"
              />
              森林
            </label>
          </div>
        </div>
      </div>

      <!-- 選択中カテゴリ表示部分 -->
      <div class="mt-3 mb-4">
        <p class="help">選択したカテゴリー</p>
        <span
          class="tag is-primary mt-1 mx-1"
          v-for="category in selectedCategoryList"
          :key="category"
        >
          {{ category }}
        </span>
      </div>

      <!-- タブレット用検索ボタン -->
      <div class="columns is-marginless" id="tablet-search-button">
        <button
          @click="clickSearchButton"
          class="button is-primary column is-fullwidth"
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
        this.$emit("searchForCategory", response.data.results);
        this.$store.dispatch("pagination/setPagination", response.data);
        this.$store.dispatch(
          "pagination/registerSearchCategorys",
          this.selectedCategoryList
        );
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
#filter-container {
  position: relative;
}
#filter-label {
  color: gray;
}
.category-checkbox {
  margin: 0 auto;
  vertical-align: middle;
}
#category-list {
  height: 100px;
}
#category-list p {
  margin: 0 auto;
  width: 90%;
}
#category-list div {
  width: 90%;
  margin: 10px auto;
}
#tablet-search-button {
  display: none;
}
@media screen and (max-width: 768px) {
  #pc-search-button {
    display: none;
  }
  #tablet-search-button {
    display: block;
  }
}
</style>