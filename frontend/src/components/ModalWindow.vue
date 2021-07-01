<template>
  <div
    @click="removeModalWindow"
    :class="{ displayNone: showWindow.hideWindow }"
  >
    <!-- モーダルの黒い部分 -->
    <div id="modal-overlay" class="columns is-centered is-vcentered is-mobile">
      <!-- モーダルの内容部分 -->
      <div
        id="modal-content"
        class="
          column
          is-4-desktop is-6-tablet is-10-mobile is-paddingless
          no-func
        "
      >
        <!-- no-funcクラスがついている部分はクリックしてもモーダルが消えない -->

        <!-- フォローしているユーザーを表示する場合 -->
        <slot
          name="favoriteUsers"
          v-if="showWindow.slotName === 'favoriteUsers'"
          class="no-func"
        ></slot>
        <!-- フォロワーを表示する場合 -->
        <slot
          name="followers"
          v-if="showWindow.slotName === 'followers'"
          class="no-func"
        ></slot>
        <!-- アプリ概要を表示する場合 -->
        <slot
          name="appOverview"
          v-if="showWindow.slotName === 'appOverview'"
          class="no-func"
        ></slot>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ["showWindow"],
  methods: {
    removeModalWindow(e) {
      // .no-funcクラスが付いた場所以外の場所をクリックしたとき
      if (!e.target.closest(".no-func")) {
        // モーダルを非表示にする
        this.$emit("removeWindow");
      }
    },
  },
};
</script>

<style scoped>
.displayNone {
  display: none;
}
#modal-overlay {
  z-index: 50;
  background-color: rgba(0, 0, 0, 0.75);
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
}
#modal-content {
  background-color: white;
  position: fixed;
  z-index: 100;
  height: 80%;
  border-radius: 20px;
  overflow: hidden;
}
</style>