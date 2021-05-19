<template>
  <div class="field mt-5 pt-2 pb-5">
    <label class="label pt-1">カテゴリー</label>
    <div class="select is-info mb-5">
      <select v-model="parentCategory">
        <option value="">指定なし</option>
        <option>建物・人工物</option>
        <option>自然</option>
      </select>
    </div>
    <div class="vertical-align">
      <p class="help mb-1" v-show="parentCategory">
        以下からカテゴリーを選択してください。
      </p>
      <div v-show="parentCategory === '建物・人工物'">
        <label class="checkbox mr-4">
          <input v-model="selectedCategory" value="道路" type="checkbox" />
          道路
        </label>
        <label class="checkbox mr-4">
          <input v-model="selectedCategory" value="商業施設" type="checkbox" />
          商業施設
        </label>
        <label class="checkbox mr-4">
          <input v-model="selectedCategory" value="ビル" type="checkbox" />
          ビル
        </label>
        <label class="checkbox">
          <input v-model="selectedCategory" value="寺・神社" type="checkbox" />
          寺・神社
        </label>
      </div>
      <div v-show="parentCategory === '自然'">
        <label class="checkbox mr-5">
          <input v-model="selectedCategory" value="山" type="checkbox" />
          山
        </label>
        <label class="checkbox mr-5">
          <input v-model="selectedCategory" value="海" type="checkbox" />
          海
        </label>
        <label class="checkbox mr-5">
          <input v-model="selectedCategory" value="空" type="checkbox" />
          空
        </label>
        <label class="checkbox mr-5">
          <input v-model="selectedCategory" value="湖" type="checkbox" />
          湖
        </label>
        <label class="checkbox mr-5">
          <input v-model="selectedCategory" value="星" type="checkbox" />
          星
        </label>
        <label class="checkbox">
          <input v-model="selectedCategory" value="森林" type="checkbox" />
          森林
        </label>
      </div>
    </div>
    <div class="mt-3">
      <p class="help">選択したカテゴリー</p>
      <input
        id="readonly-input"
        class="input"
        type="text"
        :value="selectedCategoryValue"
        readonly
      />
    </div>
  </div>
</template>

<script>
export default {
  props: {
    defaultCategorys: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      parentCategory: "",
      selectedCategory: [],
      artificial: ["道路", "商業施設", "ビル", "寺・神社"],
      nature: ["山", "海", "空", "湖", "星", "森林"], // カテゴリを追加したらここを編集
    };
  },
  computed: {
    // 選択中のカテゴリを表す文字列を作成。
    selectedCategoryValue() {
      if (!this.parentCategory) {
        return "";
      } else {
        let categoryValue = "";
        // selectedCategoryの末尾の要素を取得。
        const lastCategoryValue = this.selectedCategory.slice(-1)[0];
        for (const category of this.selectedCategory) {
          if (category === lastCategoryValue) {
            categoryValue += category;
          } else {
            categoryValue += category + ", ";
          }
        }
        return this.parentCategory + " >  " + categoryValue;
      }
    },
  },
  watch: {
    // 親カテゴリが変更されたときは子カテゴリを初期化。
    parentCategory() {
      // EditPostPage.vue（投稿編集画面）表示時にすでに投稿にカテゴリが設定してあるときは子カテゴリを初期化すると選択中のカテゴリを表示する要素にデフォルトの子カテゴリが表示されなくなるので子カテゴリの初期化をせずにpropsの値を初期化する。
      if (this.defaultCategorys.length) {
        this.$emit("clearDefaultCategorys");
      } else {
        this.selectedCategory = [];
      }
    },
    selectedCategory() {
      // selectedCategory（子カテゴリ）に変化があったら親コンポーネントへデータを渡す。
      this.$emit("changeSelectedCategorys", this.selectedCategory);
      // 子カテゴリが選択されている場合は選択中のカテゴリを表示する要素に色をつける。
      const readonlyInput = document.getElementById("readonly-input");
      if (this.selectedCategory.length) {
        readonlyInput.classList.add("is-info");
      } else {
        readonlyInput.classList.remove("is-info");
      }
    },
    defaultCategorys(val) {
      // デフォルトのカテゴリが自然（親カテゴリ）の子カテゴリであればdataの親カテゴリに代入。
      if (this.nature.includes(val[0])) {
        this.parentCategory = "自然";
        // 親コンポーネントから投稿に既に設定してあるカテゴリを受け取った際はdataの子カテゴリのリストに代入。
        this.selectedCategory = val;
        // デフォルトのカテゴリが建物・人工物（親カテゴリ）の子カテゴリであればdataの親カテゴリに代入。
      } else if (this.artificial.includes(val[0])) {
        this.parentCategory = "建物・人工物";
        this.selectedCategory = val;
      }
    },
  },
};
</script>

<style scoped>
.vertical-align input {
  vertical-align: middle;
}
select,
input {
  height: 45px;
  border-radius: 10px;
}
</style>