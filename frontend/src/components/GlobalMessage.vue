<template>
  <div id="message-container">
    <div id="messages" class="container">
      <div
        id="error"
        class="columns notification is-danger is-light is-marginless is-paddingless opacity"
        v-show="messages.errorMessage"
      >
        <p class="column is-11 pl-5">{{ messages.errorMessage }}</p>
        <button class="delete column" @click="deleteMessageData"></button>
      </div>
      <div v-if="messages.warningMessages.length" class="div-space"></div>
      <div
        id="warning"
        class="columns notification is-warning is-light is-marginless is-paddingless opacity"
        v-show="messages.warningMessages.length"
      >
        <div class="column is-11 pl-5">
          <p v-for="warning in messages.warningMessages" :key="warning">
            {{ warning }}
          </p>
        </div>
        <button class="delete column" @click="deleteMessageData"></button>
      </div>
      <div v-if="messages.infoMessage" class="div-space"></div>
      <div
        id="info"
        class="columns notification is-primary is-light is-marginless is-paddingless opacity"
        v-show="messages.infoMessage"
      >
        <p class="column is-11 pl-5">{{ messages.infoMessage }}</p>
        <button class="delete column" @click="deleteMessageData"></button>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  computed: {
    ...mapGetters("message", ["error", "warnings", "info"]),
    additionType() {
      return this.$store.getters["message/addition"].type;
    },
    additionProcess() {
      return this.$store.getters["message/addition"].process;
    },
  },
  data() {
    return {
      messages: {
        errorMessage: "",
        warningMessages: [],
        infoMessage: "",
      },
    };
  },
  methods: {
    deleteMessageData(event) {
      const messageType = event.target.parentElement.id;
      if (messageType === "error") {
        this.messages.errorMessage = "";
      } else if (messageType === "warning") {
        this.messages.warningMessages = [];
      } else {
        this.messages.infoMessage = "";
      }
    },
  },
  mounted() {
    // ページ遷移無しのapiを叩いたときなどにメッセージがセットされると、メッセージの表示ができない。
    this.messages.errorMessage = this.error;
    this.messages.warningMessages = this.warnings;
    this.messages.infoMessage = this.info;
    this.$store.dispatch("message/clearMessages");
  },
  // stateのtypeにapiを叩いた時のメッセージタイプが代入され、それをstoreから参照しwatchで監視。
  // メッセージを表示するときはこのwatchとadditionを使う。メッセージは遷移後のページでセットする。
  watch: {
    additionProcess(val) {
      if (val === "api") {
        if (this.additionType === "error") {
          this.messages.errorMessage = this.error;
        } else if (this.additionType === "warning") {
          this.messages.warningMessages = this.warnings;
        } else if (this.additionType === "info") {
          this.messages.infoMessage = this.info;
        }
      } else if (val === "afterLogoutInHome" && this.additionType === "info") {
        this.messages.infoMessage = "ログアウトしました。";
      } else if (val === "afterLogout" && this.additionType === "info") {
        this.messages.infoMessage = "ログアウトしました。";
      } else if (val === "created" && this.additionType === "info") {
        this.messages.infoMessage = "投稿しました。";
      } else if (val === "clickAddFavorites") {
        this.messages.errorMessage = "ログインしてください。";
      } else if (val === "login" && this.additionType === "info") {
        this.messages.infoMessage = "ログインしました。";
      }
      if (val !== "" || this.additionType !== "") {
        this.$store.dispatch("message/clearAddition");
      }
      this.$store.dispatch("message/clearMessages");
    },
  },
};
</script>

<style scoped>
#message-container {
  position: fixed;
  padding-top: 105px;
  z-index: 1;
  left: 2%;
  width: 96%;
  top: 0;
}
#messages div {
  width: 100%;
}
.div-space {
  height: 5px;
}
#error,
#warning,
#info {
  height: 50%;
}
.opacity {
  opacity: 0.8;
}
</style>