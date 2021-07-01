<template>
  <div>
    <!-- ヘッダー -->
    <GlobalMenu></GlobalMenu>

    <!-- メッセージ -->
    <Message></Message>

    <div id="login-container" class="container mt-6">
      <!-- ゲストユーザーの情報表示部分 -->
      <div id="guest-user">
        <h2>ゲストとしてログイン</h2>
        <div class="mb-3">
          <span class="help">以下のアカウントでゲストとして</span>
          <span class="help">ログインできます。</span>
        </div>
        <p>ユーザー名：test</p>
        <p>パスワード：test-pass</p>
      </div>

      <!-- ログインフォーム -->
      <div class="columns is-centered">
        <form
          id="login-form"
          @submit.prevent="login"
          class="box column is-4-desktop is-6-tablet is-8-mobile"
        >
          <div id="form-container">
            <!-- フォームの題名 -->
            <div class="content mt-6">
              <h1 class="has-text-centered">Login</h1>
            </div>

            <div class="mt-6">
              <!-- ユーザー名のフォーム -->
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
              <!-- パスワードのフォーム -->
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

            <!-- ログインボタン -->
            <!-- タブレットのログインボタン -->
            <button
              id="tablet-button"
              class="button is-primary is-fullwidth"
              :disabled="disabled"
            >
              ログイン
            </button>

            <!-- デスクトップのログインボタン -->
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
import Message from "@/components/Message";

export default {
  components: {
    GlobalMenu,
    Message,
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
      // ボタンからの多重送信を防止
      this.disabled = true;
      this.$store
        .dispatch("auth/login", {
          username: this.form.username,
          password: this.form.password,
        })
        .then(() => {
          let nextPage = "";
          // ログイン後の行き先が指定されている場合
          if (this.$route.query.next) {
            nextPage = this.$route.query.next;
          } else {
            nextPage = { name: "home", params: { before: "login" } };
          }
          this.$router.replace(nextPage);
        })
        // ログイン失敗時に再度ボタンを押せるようにする
        .catch(() => {
          this.disabled = false;
        });
    },
  },
};
</script>

<style scoped>
#guest-user {
  margin: 20px auto 0;
  padding: 15px;
  box-shadow: 5px 5px 5px rgba(0, 0, 0, 0.2);
  background-color: lightgreen;
  width: 40%;
  border-radius: 20px;
  text-align: center;
  border-radius: 15px;
}
span {
  display: inline-block;
}
#guest-user h2 {
  font-size: 1.3rem;
  font-weight: bold;
}
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
  #guest-user {
    width: 80%;
  }
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