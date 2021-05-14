<template>
  <div class="field mt-5 mb-1">
    <label class="label">写真撮影住所</label>
    <div class="control mt-4">
      <label for="zip" class="label-font">郵便番号（半角, ハイフンなし）</label>
      <input id="zip" type="text" class="input mt-2" v-model="zip" />
    </div>
    <div class="control mt-4">
      <label for="pref" class="label-font">都道府県</label>
      <input id="pref" type="text" class="input mt-2" v-model="prefecture" />
    </div>
    <div class="control mt-4">
      <label for="address" class="label-font">市区町村・番地</label>
      <input id="address" class="input mt-2" type="text" v-model="address" />
    </div>
  </div>
</template>

<script>
let YubinBango = require("yubinbango-core2");

export default {
  props: ["postZipCode", "postPrefecture", "postLocation"],
  data() {
    return {
      zip: "",
      prefecture: "",
      address: "",
    };
  },
  watch: {
    zip(zip) {
      let _this = this;
      // 郵便番号が記入済みで半角又は全角数字以外の文字が含まれていないときは住所検索。
      if (zip && !zip.match(/[^0-9０-９]/g)) {
        new YubinBango.Core(zip, (addr) => {
          _this.prefecture = addr.region;
          _this.address = addr.locality + addr.street;
          // 親コンポーネントへ郵便番号データを渡す。
          this.$emit("send-zip", zip);
        });
        // 郵便番号欄が空、または半角・全角数字以外の文字が含まれているときは住所のデータを初期化。
      } else {
        _this.prefecture = "";
        _this.address = "";
        // 親コンポーネントへ郵便番号データを渡す。
        this.$emit("send-zip", zip);
      }
    },
    // 県データを変更したら親コンポーネントにそのデータを渡す。
    prefecture(prefecture) {
      this.$emit("send-prefecture", prefecture);
    },
    // 市区町村・番地データを変更したら親コンポーネントにそのデータを渡す。
    address(address) {
      this.$emit("send-location", address);
    },
    postZipCode(zipCode) {
      this.zip = zipCode;
    },
    postPrefecture(prefecture) {
      this.prefecture = prefecture;
    },
    postLocation(location) {
      this.address = location;
    },
  },
};
</script>

<style scoped>
#zip {
  display: block;
  width: 100px;
  height: 35px;
}
.label-font {
  font-size: 14px;
}
</style>