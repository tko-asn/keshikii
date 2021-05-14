<template>
  <div>
    <GlobalMenu></GlobalMenu>
    <GlobalMessage></GlobalMessage>
    <div id="edit-profile-container" class="container mt-6">
      <div class="columns is-centered is-vcentered">
        <form
          id="profile-form"
          class="box column is-5-desktop is-6-tablet is-8-mobile"
          @submit.prevent="clickEditProfile"
        >
          <div class="form-container">
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
                <span class="file-cta" id="image-select">
                  <span class="file-icon">
                    <fa-icon icon="file-upload"></fa-icon>
                  </span>
                  <span class="file-label"> 画像を選択 </span>
                </span>
                <span class="file-name">{{ this.iconFileName }}</span>
              </label>
            </div>
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
            <button id="profile-button" class="button is-primary is-fullwidth">
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
import GlobalMessage from "@/components/GlobalMessage";

export default {
  components: {
    GlobalMenu,
    GlobalMessage,
  },
  data() {
    return {
      user: {},
      newIconSrc: "",
      newIcon: null,
      iconFileNameInData: "",
    };
  },
  mounted() {
    api.get("/auth/users/me/").then((response) => {
      this.user = response.data;
    });
  },
  computed: {
    iconSrc() {
      if (!this.newIconSrc) {
        return this.user.icon_url;
      } else {
        return this.newIconSrc;
      }
    },
    iconFileName() {
      if (!this.iconFileNameInData) {
        if (this.user.icon_filename === "default_user_icon.jpeg") {
          return "デフォルト";
        }
        return this.user.icon_filename;
      } else {
        return this.iconFileNameInData;
      }
    },
  },
  methods: {
    getFileData(file) {
      return new Promise((resolve, reject) => {
        this.newIcon = file;
        this.iconFileNameInData = file.name;
        const fileReader = new FileReader();
        fileReader.readAsDataURL(file);
        fileReader.onload = () => resolve(fileReader.result);
        fileReader.onerror = (error) => reject(error); // 開発環境
      });
    },
    onIconChange(event) {
      const images = event.target.files || event.dataTransfer.files;
      this.getFileData(images[0])
        .then((fileData) => {
          this.newIconSrc = fileData;
        })
        .catch(() => {
          const errorMessage = "画像のアップロードに失敗しました。";
          this.$store.dispatch("message/setErrorMessage", {
            message: errorMessage,
          });
        });
    },
    clickEditProfile() {
      const params = new FormData();
      const editFields = ["username", "self_introduction"]; // 入力項目追加するごとに個々にも追加。
      Object.entries(this.user).forEach(([key, value]) => {
        if (editFields.includes(key)) {
          params.append(key, value);
        }
      });
      if (this.newIcon) {
        params.append("icon", this.newIcon);
      }
      api.patch("/auth/users/me/", params).then(() => {
        this.$router.replace({ name: "mypage" });
      });
    },
  },
};
</script>

<style scoped>
#image-select {
  width: 30%;
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
</style>