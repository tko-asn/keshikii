<template>
  <div class="message-container">
    <!-- エラーメッセージ -->
    <div
      v-for="message in errorMessages"
      :key="message"
      class="
        columns
        notification
        is-error is-light is-marginless is-paddingless
        opacity
      "
      v-show="errorMessages.length"
    >
      <p class="column is-11 pl-5">{{ message }}</p>
      <button
        class="delete column"
        @click="deleteMessage('error', message)"
      ></button>
    </div>
    <div v-if="warningMessages.length" class="div-space"></div>

    <!-- 注意 -->
    <div
      v-for="message in warningMessages"
      :key="message"
      class="
        columns
        notification
        is-warning is-light is-marginless is-paddingless
        opacity
      "
      v-show="warningMessages.length"
    >
      <p class="column is-11 pl-5">{{ message }}</p>
      <button
        class="delete column"
        @click="deleteMessage('warning', message)"
      ></button>
    </div>
    <div v-if="infoMessages.length" class="div-space"></div>

    <!-- お知らせ -->
    <div
      v-for="message in infoMessages"
      :key="message"
      class="
        columns
        notification
        is-info is-light is-marginless is-paddingless
        opacity
      "
      v-show="infoMessages.length"
    >
      <p class="column is-11 pl-5">{{ message }}</p>
      <button
        class="delete column"
        @click="deleteMessage('info', message)"
      ></button>
    </div>
    <div v-if="apiMessages.length" class="div-space"></div>

    <!-- apiからのエラーメッセージ等 -->
    <div
      v-for="message in apiMessages"
      :key="message"
      class="
        columns
        notification
        is-warning is-light is-marginless is-paddingless
        opacity
        mb-1
      "
      v-show="apiMessages.length"
    >
      <p class="column is-11 pl-5">{{ message }}</p>
      <button
        class="delete column"
        @click="deleteStoreMessage(message)"
      ></button>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  props: {
    error: {
      type: Array,
      default: () => [],
    },
    warning: {
      type: Array,
      default: () => [],
    },
    info: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      // propsのデータをそのままテンプレートに使うのではなく
      // メッセージの要素を消せるようにdataに代入
      errorMessages: [],
      warningMessages: [],
      infoMessages: [],
    };
  },
  computed: {
    // apiのレスポンスメッセージ
    ...mapGetters("messages", ["messages"]),
    apiMessages() {
      // apiのリクエストを複数同時に実行したときに
      // メッセージが重複してセットされる恐れがあるため
      // vuexのmessagesから重複を削除
      return Array.from(new Set(this.messages));
    },
  },
  methods: {
    // 削除ボタンをおされたとき
    // そのメッセージを含まない新しいメッセージの配列を作成し
    // dataに代入
    deleteMessage(type, message) {
      if (type === "error") {
        this.errorMessages = this.errorMessages.filter((v) => v !== message);
      } else if (type === "warning") {
        this.warningMessages = this.warningMessages.filter(
          (v) => v !== message
        );
      } else {
        this.infoMessages = this.infoMessages.filter((v) => v !== message);
      }
    },
    // apiからのメッセージはvuexのmessagesモジュールに保存
    // 削除ボタンを押したときにvuexのメッセージを削除
    deleteStoreMessage(message) {
      this.$store.dispatch("messages/remove", message);
    },
  },
  watch: {
    // 親コンポーネントからpropsに新しいメッセージが渡されたとき
    // そのメッセージをdataに反映
    // messageListは配列
    error(messageList) {
      for (const message of messageList) {
        this.errorMessages.push(message);
      }
    },
    warning(messageList) {
      for (const message of messageList) {
        this.warningMessages.push(message);
      }
    },
    info(messageList) {
      for (const message of messageList) {
        this.infoMessages.push(message);
      }
    },
  },
};
</script>

<style scoped>
.message-container {
  position: fixed;
  padding-top: 105px;
  z-index: 1;
  left: 2%;
  width: 96%;
  top: 0;
}
.message-container div {
  width: 100%;
  height: 50%;
}
.div-space {
  height: 5px;
}
.opacity {
  opacity: 0.8;
}
</style>