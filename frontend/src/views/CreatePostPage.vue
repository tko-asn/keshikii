<template>
  <div>
    <!-- ヘッダー -->
    <GlobalMenu></GlobalMenu>

    <!-- メッセージ -->
    <Message></Message>

    <!-- 投稿フォーム -->
    <div id="post-container" class="container mt-6 mb-6">
      <div class="columns is-centered">
        <form
          id="post-form"
          @submit.prevent="createPost"
          class="box column is-5-desktop is-6-tablet is-8-mobile"
        >
          <div id="form-container">
            <!-- フォームラベル -->
            <div class="content mt-6">
              <h1 class="has-text-centered">Post Form</h1>
            </div>

            <!-- 投稿画像フォーム -->
            <PostImageForm @changeImage="setImageFile"></PostImageForm>

            <!-- タイトルフォーム -->
            <div class="field mt-5">
              <div class="control pt-3">
                <input
                  class="input"
                  type="text"
                  placeholder="タイトルを入力"
                  v-model="newPost.title"
                />
              </div>
            </div>

            <!-- 説明文フォーム -->
            <div class="field mt-5">
              <div class="control pt-3">
                <textarea
                  class="textarea"
                  placeholder="説明文を入力"
                  v-model="newPost.text"
                ></textarea>
              </div>
            </div>

            <!-- カテゴリフォーム -->
            <PostCategoryForm
              @changeSelectedCategorys="setCategorys($event)"
            ></PostCategoryForm>

            <!-- 地名・住所フォーム -->
            <PostLocationForm
              @send-zip="saveZip($event)"
              @send-prefecture="savePrefecture($event)"
              @send-location="saveLocation($event)"
            ></PostLocationForm>

            <!-- 公開設定フォーム -->
            <PostStatusForm @changeRadio="setStatus($event)"></PostStatusForm>

            <!-- バリデーションメッセージ -->
            <ValidationMessage :messages="messages"></ValidationMessage>

            <!-- 投稿ボタン -->
            <div class="field is-grouped mt-5 mb-2">
              <button
                :disabled="disabled"
                class="button button-border is-primary is-fullwidth"
              >
                投稿する
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/api";
import GlobalMenu from "@/components/GlobalMenu";
import PostLocationForm from "@/components/PostLocationForm";
import PostStatusForm from "@/components/PostStatusForm";
import PostCategoryForm from "@/components/PostCategoryForm";
import PostImageForm from "@/components/PostImageForm";
import ValidationMessage from "@/components/ValidationMessage";
import Message from "@/components/Message";

export default {
  components: {
    GlobalMenu,
    PostLocationForm,
    PostStatusForm,
    PostCategoryForm,
    PostImageForm,
    ValidationMessage,
    Message,
  },
  data() {
    return {
      newPost: {
        picture: null,
        fileName: "",
        title: "",
        text: "",
        status: "public",
      },
      selectedCategory: [],
      zipCode: "",
      prefecture: "",
      location: "",
      disabled: false,
      messages: [],
    };
  },
  methods: {
    setImageFile(...newFileData) {
      // 画像ファイル(Blob)を保存
      this.newPost.picture = newFileData[0];
      // 画像ファイル名を保存
      this.newPost.fileName = newFileData[1];
    },
    setCategorys(categorysList) {
      this.selectedCategory = categorysList;
    },
    setStatus(newStatus) {
      this.newPost.status = newStatus;
    },
    createPost() {
      this.disabled = true;
      // メッセージの初期化
      this.messages = [];

      // 入力必須項目が空の場合のメッセージ
      if (!this.newPost.picture || !this.newPost.title) {
        if (!this.newPost.picture) {
          this.messages.push("画像は必須項目です。");
          this.disabled = false;
        }
        if (!this.newPost.title) {
          this.messages.push("タイトルは必須項目です。");
          this.disabled = false;
        }
        return;
      }

      // 送信データの作成
      const params = new FormData();
      Object.entries(this.newPost).forEach(([key, value]) => {
        if (key === "picture") {
          // this.newPost.pictureはBlob
          // 第三引数にファイル名を追加
          params.append(key, this.newPost.picture, this.newPost.fileName);
        } else {
          params.append(key, value);
        }
      });

      // カテゴリの設定
      this.selectedCategory.forEach((value) => {
        // manytomanyfieldなのでひとつずつ加える。
        params.append("category", value);
      });

      // 地名・住所を設定
      params.append("zip_code", this.zipCode);
      params.append("prefecture", this.prefecture);
      params.append("location", this.location);

      // 投稿を作成
      api
        .post("/users_post/", params)
        .then(() => {
          // ホームページへ遷移
          this.$router.push({ name: "home", params: { before: "create" } });
        })
        .catch(() => {
          this.disabled = false;
        });
    },
    saveZip(zip) {
      if (!zip.match(/[^0-9０-９]/g)) {
        // 郵便番号のデータの全角数字を半角に変換。
        const zip1 = zip.replace(/[０-９]/g, (str) => {
          return String.fromCharCode(str.charCodeAt(0) - 0xfee0);
        });
        this.zipCode = zip1;
      } else {
        // 半角・全角数字以外の文字が郵便番号のデータに含まれている場合は郵便番号のデータを初期化。
        this.zipCode = "";
      }
    },
    savePrefecture(prefectureData) {
      this.prefecture = prefectureData;
    },
    saveLocation(locationData) {
      this.location = locationData;
    },
  },
};
</script>

<style scoped>
#post-container {
  padding-top: 40px;
}
.button-border {
  border-radius: 20px;
}
#post-form {
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
#form-container input,
textarea {
  height: 45px;
  border-radius: 10px;
}
@media screen and (max-width: 768px) {
  #form-container h1 {
    margin-top: 20px;
    margin-bottom: 40px;
    font-size: 40px;
  }
}
</style>