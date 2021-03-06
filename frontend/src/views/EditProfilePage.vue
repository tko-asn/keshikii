<template>
  <div>
    <!-- ヘッダー -->
    <GlobalMenu></GlobalMenu>

    <!-- メッセージ -->
    <Message></Message>

    <!-- プロフィール編集フォーム -->
    <div id="edit-profile-container" class="container mt-6">
      <div class="columns is-centered is-vcentered">
        <form
          id="profile-form"
          class="box column is-5-desktop is-6-tablet is-8-mobile"
          @submit.prevent="clickEditProfile"
        >
          <div class="form-container">
            <!-- アイコン編集フォーム -->
            <div class="field mt-4">
              <div class="icon-box">
                <img :src="iconSrc" alt="icon" />
              </div>
            </div>
            <div class="file has-name is-fullwidth mt-5">
              <label class="file-label">
                <input
                  class="file-input"
                  type="file"
                  name="resume"
                  @change="onIconChange"
                />

                <!-- アイコンファイル選択ボタン -->
                <span class="file-cta" id="image-select">
                  <span class="file-icon">
                    <fa-icon icon="file-upload"></fa-icon>
                  </span>
                  <span id="select-icon" class="file-label"> 画像 </span>
                </span>

                <!-- ファイル名表示部分 -->
                <span class="file-name">{{ this.iconFileName }}</span>
              </label>
            </div>

            <!-- ユーザー名編集フォーム -->
            <div class="field mt-4">
              <label class="label">ユーザー名</label>
              <div class="control">
                <input
                  class="input"
                  type="text"
                  placeholder="ユーザー名を入力"
                  v-model="user.username"
                />
              </div>
            </div>

            <!-- 自己紹介編集フォーム -->
            <div class="field">
              <label class="label">自己紹介</label>
              <div class="control">
                <textarea
                  class="textarea"
                  placeholder="例）よろしくお願いします。"
                  v-model="user.self_introduction"
                ></textarea>
              </div>
            </div>

            <!-- バリデーションメッセージ -->
            <ValidationMessage
              :messages="messages"
              class="mb-2"
            ></ValidationMessage>

            <!-- プロフィール編集ボタン -->
            <button
              id="profile-button"
              class="button is-primary is-fullwidth"
              :disabled="disabled"
            >
              プロフィールを編集する
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/api";
import GlobalMenu from "@/components/GlobalMenu";
import ValidationMessage from "@/components/ValidationMessage";
import Message from "@/components/Message";
import Compressor from "compressorjs";

export default {
  components: {
    GlobalMenu,
    ValidationMessage,
    Message,
  },
  data() {
    return {
      user: {},
      newIconSrc: "",
      newIcon: null,
      iconFileNameInData: "",
      disabled: false,
      messages: [],
    };
  },
  mounted() {
    // ユーザーのデータをvuexから参照し保存
    this.user = this.$store.getters["auth/userProfile"];
  },
  computed: {
    iconSrc() {
      // アイコンに変更がない場合
      if (!this.newIconSrc) {
        return this.user.icon_url;
      }
      // アイコンが変更された場合
      return this.newIconSrc;
    },
    iconFileName() {
      // アイコンに変更がない場合
      if (!this.iconFileNameInData) {
        // デフォルトのアイコンの場合
        if (this.user.icon_filename === "default_user_icon.jpeg") {
          return "デフォルト";
        }
        // アイコンがデフォルトでない場合
        return this.user.icon_filename;
      }
      // アイコンが変更された場合
      return this.iconFileNameInData;
    },
  },
  methods: {
    // onIconChange内で使用する関数
    getFileData(file) {
      return new Promise((resolve, reject) => {
        this.newIcon = file;
        this.iconFileNameInData = file.name;
        const fileReader = new FileReader();
        fileReader.readAsDataURL(file);
        fileReader.onload = () => resolve(fileReader.result);
        fileReader.onerror = (error) => reject(error);
      });
    },
    // iconのフォームに変化があった場合の処理
    onIconChange(event) {
      const images = event.target.files || event.dataTransfer.files;
      // 画像ファイル
      const data = images[0];
      const _this = this;
      // 投稿画像を圧縮
      new Compressor(data, {
        // 圧縮した画像の解像度
        quality: 0.6,
        // 圧縮成功時の処理
        success(result) {
          _this.getFileData(result).then((fileData) => {
            _this.newIconSrc = fileData;
          });
        },
        maxWidth: 200,
        maxHeight: 200,
        mimeType: "image/jpeg",
        // 圧縮失敗時の処理
        // error() {
        // },
      });
    },
    clickEditProfile() {
      this.disabled = true;
      // ユーザー名が空の場合
      this.messages = [];
      // usernameフォームが空の場合
      if (!this.user.username) {
        this.messages.push("ユーザー名は必須項目です。");
        this.disabled = false;
        return;
      }

      const params = new FormData();
      // 入力項目追加するごとにeditFieldsにも追加
      const editFields = ["username", "self_introduction"];
      Object.entries(this.user).forEach(([key, value]) => {
        if (editFields.includes(key)) {
          params.append(key, value);
        }
      });

      // 新規アイコンが設定された場合
      if (this.newIcon) {
        params.append("icon", this.newIcon, this.iconFileNameInData);
      }

      // データベースに変更内容を反映
      api
        .patch("/auth/users/me/", params)
        // 成功したらマイページへ移動
        .then((response) => {
          // vuexのauth.jsのユーザー情報を書き換える
          // ここで変更しないと次にreloadが行われるまでstateの値が書き変わらない
          this.$store.dispatch("auth/editUserProfile", response.data);

          // MyPageへ
          this.$router.replace({
            name: "mypage",
            params: { before: "editProfile" },
          });
        })
        // 失敗したらボタンを再度押せるようにする
        .catch(() => {
          this.disabled = false;
        });
    },
  },
};
</script>

<style scoped>
#image-select {
  width: 25%;
}
.form-container {
  margin: 0 auto;
  width: 90%;
}
#edit-profile-container {
  padding-top: 100px;
}
#profile-form {
  margin: 0 auto;
  border-radius: 20px;
}
#profile-form input,
textarea,
button {
  border-radius: 20px;
}
.icon-box {
  width: 100px;
  height: 100px;
  margin: 0 auto;
}
.icon-box img {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 50%;
}
@media screen and (max-width: 768px) {
  #select-icon {
    display: none;
  }
  #image-select {
    width: 10%;
  }
  #image-select > span {
    width: 100%;
  }
}
</style>