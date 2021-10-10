<template>
  <div class="app-overview">
    <div class="app-overview__scroll">
      <div class="container-overview">
        <!-- アプリ名 -->
        <h1 class="container-overview__title pt-5 pb-3">KESHKIIとは</h1>

        <!-- アプリ概要 -->
        <span class="container-overview__span">
          <span class="container-overview__span">誰でも気軽に</span>
          <span class="container-overview__span">写真を投稿できる</span>
          <span class="container-overview__span">景色共有アプリです。</span>
        </span>
        <span class="container-overview__span">
          <span class="container-overview__span">あなたが</span>
          <span class="container-overview__span">日常で見つけた</span>
          <span class="container-overview__span">小さな発見を</span>
          <span class="container-overview__span">写真に収めて</span>
          <span class="container-overview__span">他の人に</span>
          <span class="container-overview__span">紹介しましょう。</span>
        </span>
        <span class="container-overview__span">
          <span class="container-overview__span">このアプリでは</span>
          <span class="container-overview__span">地名や住所を</span>
          <span class="container-overview__span">表記できるため</span>
          <span class="container-overview__span">写真の撮影場所を</span>
          <span class="container-overview__span">サイト閲覧者に</span>
          <span class="container-overview__span">教えることが</span>
          <span class="container-overview__span">できます。</span>
        </span>
        <span class="container-overview__span">
          <span class="container-overview__span">あなたの見つけた</span>
          <span class="container-overview__span">観光地を他の人に</span>
          <span class="container-overview__span">紹介してみませんか？</span>
        </span>

        <!-- モーダル非表示ボタン -->
        <a
          class="
            container-overview__btn
            button
            is-primary is-medium is-outlined
            mt-5
            mb-5
          "
          @click="remove"
          >閉じる</a
        >
      </div>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    remove() {
      // モーダルを非表示
      this.$emit("removeModalInAppOverview");
    },
  },
};
</script>

<style scoped>
.app-overview__scroll {
  height: 100%;
  overflow-y: scroll;
}

.app-overview {
  width: 100%;
  height: 100%;
}

.container-overview {
  height: 100%;
  width: 80%;
  margin: 0 auto;
  text-align: center;
}

.container-overview__title {
  color: #aaaaaa;
  margin: 0;
  font-size: 3vw;
}

.container-overview__span {
  color: gray;
  line-height: 3;
  display: inline-block;
}

.container-overview__btn {
  border-radius: 20px;
}

@media screen and (max-width: 768px) {
  .container-overview__title {
    font-size: 7vw;
  }
}
</style>