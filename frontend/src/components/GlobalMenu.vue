<template>
  <nav class="navbar is-primary" id="global-menu">
    <!-- アプリ概要モーダル -->
    <ModalWindow :showWindow="modalInfo" @removeWindow="removeModalWindow">
      <template v-slot:appOverview>
        <AppOverview
          @removeModalInAppOverview="removeModalWindow"
        ></AppOverview>
      </template>
    </ModalWindow>

    <div class="container">
      <div class="navbar-brand is-marginless">
        <!-- アプリのロゴ -->
        <router-link id="app-name" class="navbar-item" to="/">
          <img :src="logo" alt="keshikii" />
        </router-link>

        <!-- タブレット用ハンバーガーメニューボタン -->
        <span id="tablet-search" class="navbar-item"><slot></slot></span>
        <a
          id="burger-button"
          role="button"
          class="navbar-burger"
          aria-label="menu"
          aria-expanded="false"
          @click="toggleBurger"
        >
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>

      <!-- モバイル用検索フォーム -->
      <span id="mobile-search" class="navbar-item"><slot></slot></span>

      <!-- ハンバーガメニュー -->
      <div v-show="isOpen" id="burger-menu">
        <a class="navbar-item" @click="showAppOverview">KESHKIIとは</a>
        <router-link to="/create/post" class="navbar-item">
          投稿する
        </router-link>
        <template v-if="!isLoggedIn">
          <router-link to="/login" class="navbar-item"> ログイン </router-link>
          <router-link to="/signup" class="navbar-item"> 新規登録 </router-link>
        </template>
        <template v-else>
          <router-link to="/mypage" class="navbar-item">
            マイページ
          </router-link>
          <a @click="logout" class="navbar-item"> ログアウト </a>
        </template>
      </div>

      <!-- デスクトップ用メニュー -->
      <div class="navbar-menu is-marginless">
        <div class="navbar-end">
          <span class="navbar-item"><slot></slot></span>
          <a class="navbar-item" @click="showAppOverview">KESHKIIとは</a>
          <router-link to="/create/post" class="navbar-item"
            >投稿する</router-link
          >
          <!-- ログインしているとき -->
          <template v-if="isLoggedIn">
            <div
              id="dropdown-container"
              class="dropdown navbar-item is-paddingless pc-button-width"
            >
              <!-- アカウントボタン -->
              <div id="dropdown-trigger" class="dropdown-trigger full">
                <button
                  @click="toggleDropdown"
                  aria-haspopup="true"
                  class="button is-primary"
                >
                  アカウント
                </button>
              </div>
              <!-- アカウントボタンのドロップダウンメニュー -->
              <div id="dropdown-menu" role="menu" v-show="isDown">
                <div
                  class="dropdown-content"
                  @mouseover="addIsActiveClass"
                  @mouseout="deleteIsActiveClass"
                >
                  <router-link to="/mypage" class="dropdown-item"
                    >マイページ</router-link
                  >
                  <hr class="dropdown-divider" />
                  <a @click="logout" class="dropdown-item"> ログアウト </a>
                </div>
              </div>
            </div>
          </template>

          <!-- ログインしていないとき -->
          <template v-else>
            <router-link to="/signup" class="navbar-item">新規登録</router-link>
            <router-link to="/login" class="navbar-item">ログイン</router-link>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { mapGetters } from "vuex";
import AppOverview from "@/components/AppOverview";
import ModalWindow from "@/components/ModalWindow";

export default {
  components: {
    ModalWindow,
    AppOverview,
  },
  data() {
    return {
      logo: require("@/assets/keshikii_logo2.png"),
      modalInfo: {
        hideWindow: true,
        slotName: "",
      },
    };
  },
  computed: {
    ...mapGetters("auth", ["username", "isLoggedIn"]),
    ...mapGetters("dropdown", ["isDown", "isOpen"]),
  },
  methods: {
    logout() {
      // ログアウトを実行
      this.$store.dispatch("auth/logout");
      // 現在のページがHomePageではないとき
      if (this.$route.path !== "/") {
        this.$router.replace({ name: "home", params: { before: "logout" } });
      }
    },
    toggleDropdown() {
      if (this.isDown) {
        // isDownをfalseにしてドロップダウンメニューを非表示
        this.$store.dispatch("dropdown/changeIsDown", false);
      } else {
        // isDownをtrueにしてドロップダウンメニューを表示
        this.$store.dispatch("dropdown/changeIsDown", true);
      }
    },
    toggleBurger() {
      if (this.isOpen) {
        // isOpenをfalseにしてハンバーガーメニューを非表示
        this.$store.dispatch("dropdown/changeIsOpen", false);
      } else {
        // isOpenをtrueにしてハンバーガーメニューを表示
        this.$store.dispatch("dropdown/changeIsOpen", true);
      }
    },
    // ドロップダウンメニューにカーソルを乗せたときの処理
    addIsActiveClass(event) {
      event.target.classList.add("is-active");
    },
    // ドロップダウンメニューからカーソルをどけたときの処理
    deleteIsActiveClass(event) {
      event.target.classList.remove("is-active");
    },
    removeModalWindow() {
      this.modalInfo.slotName = "";
      this.modalInfo.hideWindow = true;
    },
    showAppOverview() {
      this.modalInfo.slotName = "appOverview";
      this.modalInfo.hideWindow = false;
    },
  },
  destroyed() {
    if (this.isOpen) {
      // vuexのisOpenを初期化
      this.$store.dispatch("dropdown/changeIsOpen", false);
    }
    if (this.isDown) {
      // vuexのisDownを初期化
      this.$store.dispatch("dropdown/changeIsDown", false);
    }
  },
};
</script>

<style scoped>
#burger-menu {
  display: none;
  /* デスクトップでnoneに設定しないと
  バーガーメニューが開きっぱなしのときに
  デスクトップでも表示されてしまう。 */
}
.bars-icon {
  color: white;
}
#burger-menu a {
  color: white;
}
.navbar {
  min-height: 100px;
}
#dropdown-container {
  position: relative;
}
#dropdown-menu {
  position: absolute;
  top: 100px;
}
#global-menu {
  position: fixed;
  width: 100%;
  top: 0;
}
.full {
  height: 100%;
  width: 100%;
}
.full button {
  display: block;
  height: 100%;
  width: 100%;
  border-radius: 0;
  border-width: 1px;
}
.pc-button-width {
  /* width: 86px; */
  height: 98px;
}
#tablet-search {
  display: none;
}
#mobile-search {
  display: none;
}
@media screen and (max-width: 1024px) {
  #burger-menu {
    display: block;
    /* blockにしてあるがv-showの条件が
    trueにならないと表示されない */
  }
  #tablet-search {
    width: 60%;
    display: flex;
  }
}
@media screen and (max-width: 768px) {
  #mobile-search {
    display: flex;
  }
  #tablet-search {
    display: none;
  }
}
</style>