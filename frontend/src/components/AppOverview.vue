<template>
  <div id="app-overview">
    <div class="scroll-block">
      <div class="overview-container">
        <h1 class="app-title pt-5 pb-3">KESHKIIとは</h1>
        <span>
          <span>誰でも気軽に</span>
          <span>写真を投稿できる</span>
          <span>景色共有アプリです。</span>
        </span>
        <span>
          <span>あなたが</span>
          <span>日常で見つけた</span>
          <span>小さな発見を</span>
          <span>写真に収めて</span>
          <span>他の人に</span>
          <span>紹介しましょう。</span>
        </span>
        <span>
          <span>このアプリでは</span>
          <span>地名や住所を</span>
          <span>表記できるため</span>
          <span>写真の撮影場所を</span>
          <span>サイト閲覧者に</span>
          <span>教えることが</span>
          <span>できます。</span>
        </span>
        <span>
          <span>あなたの見つけた</span>
          <span>観光地を他の人に</span>
          <span>紹介してみませんか？</span>
        </span>
        <a
          class="button is-primary is-medium is-outlined mt-5 mb-5 border-radius"
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
      this.$emit("removeModalInAppOverview");
    },
  },
};
</script>

<style scoped>
.scroll-block {
  height: 100%;
  overflow-y: scroll;
}
#app-overview {
  width: 100%;
  height: 100%;
}
.overview-container {
  height: 100%;
  width: 80%;
  margin: 0 auto;
  text-align: center;
}
.app-title {
  color: #aaaaaa;
  margin: 0;
  font-size: 3vw;
}
span {
  color: gray;
  line-height: 3;
  display: inline-block;
}
.border-radius {
  border-radius: 20px;
}
@media screen and (max-width: 768px) {
  .app-title {
    font-size: 7vw;
  }
}
</style>