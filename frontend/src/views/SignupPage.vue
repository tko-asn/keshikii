<template>
  <div>
    <GlobalMenu></GlobalMenu>
    <GlobalMessage></GlobalMessage>
    <div id="signup-container" class="container mt-6">
      <div class="columns is-centered">
        <form
          id="signup-form"
          @submit.prevent="registerUser"
          class="box column is-4-desktop is-6-tablet is-8-mobile"
        >
          <div id="form-container">
            <div class="content mt-6 pb-1">
              <h1 class="has-text-centered">SignUp</h1>
            </div>
            <div class="field pt-4">
              <div class="control">
                <input
                  class="input"
                  type="text"
                  placeholder="ユーザー名"
                  v-model="newUser.username"
                />
              </div>
            </div>
            <div class="field">
              <div class="control">
                <input
                  class="input"
                  type="password"
                  placeholder="パスワード"
                  v-model="newUser.password"
                />
              </div>
            </div>
            <div class="field">
              <div class="control">
                <input
                  class="input"
                  type="password"
                  placeholder="確認用パスワード"
                  v-model="newUser.confirmationPassword"
                />
              </div>
            </div>
            <ValidationMessage :messages="messages"></ValidationMessage>
            <button
              class="button is-primary is-fullwidth"
              id="tablet-button"
              :disabled="disabled"
            >
              新規登録
            </button>
            <button
              class="button is-primary"
              id="pc-button"
              :disabled="disabled"
            >
              新規登録
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import GlobalMenu from "@/components/GlobalMenu";
import GlobalMessage from "@/components/GlobalMessage";
import ValidationMessage from "@/components/ValidationMessage";

export default {
  components: {
    GlobalMenu,
    GlobalMessage,
    ValidationMessage,
  },
  data() {
    return {
      newUser: {
        username: "",
        password: "",
        confirmationPassword: "",
      },
      disabled: false,
      messages: [],
    };
  },
  methods: {
    registerUser() {
      this.messages = [];
      this.disabled = true;
      if (this.newUser.password !== this.newUser.confirmationPassword) {
        this.disabled = false;
        this.messages.push("確認用パスワードが違います。");
        return;
      }
      this.$store
        .dispatch("auth/register", {
          username: this.newUser.username,
          password: this.newUser.password,
          re_password: this.newUser.confirmationPassword,
        })
        .then(() => {
          this.$store
            .dispatch("auth/login", {
              username: this.newUser.username,
              password: this.newUser.password,
            })
            .then(() => {
              this.$store.dispatch("message/setInfoMessage", {
                message: "ユーザー登録が完了しました。",
              });
              this.$router.replace("/");
            });
        })
        .catch(() => {
          this.disabled = false;
        });
    },
  },
};
</script>

<style scoped>
#signup-container {
  padding-top: 60px;
}
#signup-form {
  margin: 80px auto 0;
  min-height: 420px;
  border-radius: 20px;
}
#form-container {
  width: 90%;
  margin: 0 auto;
  position: relative;
  height: 100%;
}
#tablet-button {
  display: none;
}
#pc-button {
  position: absolute;
  bottom: 60px;
  display: block;
  width: 100%;
  border-radius: 20px;
}
#form-container input {
  border-radius: 20px;
}
@media screen and (max-width: 768px) {
  #tablet-button {
    display: block;
    margin-top: 50px;
    margin-bottom: 20px;
    border-radius: 15px;
  }
  #pc-button {
    display: none;
  }
  #form-container h1 {
    margin-top: 20px;
    margin-bottom: 40px;
    font-size: 40px;
  }
  #form-container input {
    height: 50px;
  }
}
</style>