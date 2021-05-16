<template>
  <div>
    <GlobalMenu></GlobalMenu>
    <GlobalMessage></GlobalMessage>
    <div id="login-container" class="container mt-6">
      <div class="columns is-centered">
        <form
          id="login-form"
          @submit.prevent="login"
          class="box column is-4-desktop is-6-tablet is-8-mobile"
        >
          <div id="form-container">
            <div class="content mt-6">
              <h1 class="has-text-centered">Login</h1>
            </div>
            <div class="mt-6">
              <div class="field pt-5 pb-1">
                <div class="control">
                  <input
                    class="input"
                    type="text"
                    v-model="form.username"
                    placeholder="ユーザー名"
                  />
                </div>
              </div>
              <div class="field">
                <div class="control">
                  <input
                    class="input"
                    type="password"
                    v-model="form.password"
                    placeholder="パスワード"
                  />
                </div>
              </div>
            </div>
            <button
              id="tablet-button"
              class="button is-primary is-fullwidth"
              :disabled="disabled"
            >
              ログイン
            </button>
            <button
              class="button is-primary"
              id="pc-button"
              :disabled="disabled"
            >
              ログイン
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

export default {
  components: {
    GlobalMenu,
    GlobalMessage,
  },
  data() {
    return {
      form: {
        username: "",
        password: "",
      },
      disabled: false,
    };
  },
  props: ["before"],
  methods: {
    login() {
      this.disabled = true;
      this.$store
        .dispatch("auth/login", {
          username: this.form.username,
          password: this.form.password,
        })
        .then(() => {
          let nextPage = "";
          if (this.$route.query.next) {
            nextPage = this.$route.query.next;
          } else {
            nextPage = { name: "home", params: { before: "login" } };
          }
          this.$router.replace(nextPage);
        })
        .catch(() => {
          this.disabled = false;
        });
    },
  },
  beforeRouteEnter(to, from, next) {
    if (to.params.before === "viewPost") {
      next((vm) => {
        vm.$store.dispatch("message/setAddition", {
          messageType: "error",
          process: "clickAddFavorites",
        });
      });
    } else {
      next();
    }
  },
};
</script>

<style scoped>
#login-form {
  margin: 80px auto 0;
  min-height: 400px;
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
  height: 45px;
  border-radius: 20px;
}
#login-container {
  padding-top: 60px;
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