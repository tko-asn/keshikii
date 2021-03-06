<template>
  <div>
    <!-- ヘッダー -->
    <GlobalMenu></GlobalMenu>

    <!-- メッセージ -->
    <Message></Message>

    <!-- 投稿編集フォーム -->
    <div id="edit-container" class="container mt-6 mb-6">
      <div class="columns is-centered">
        <form
          id="edit-form"
          @submit.prevent
          @keydown.enter.prevent
          class="box column is-5-desktop is-6-tablet is-8-mobile"
        >
          <div id="form-container">
            <!-- フォームラベル -->
            <div class="content mt-6">
              <h1 class="has-text-centered">Edit Form</h1>
            </div>

            <!-- 投稿画像フォーム -->
            <PostImageForm
              @changeImage="setImageFile"
              :defaultSrc="post.picture_url"
              :defaultFileName="post.picture_filename"
            ></PostImageForm>

            <!-- タイトルフォーム -->
            <div class="field mt-5">
              <div class="control pt-3">
                <input
                  class="input"
                  type="text"
                  placeholder="タイトルを入力"
                  v-model="post.title"
                />
              </div>
            </div>

            <!-- 説明文フォーム -->
            <div class="field mt-5">
              <div class="control pt-3">
                <textarea
                  class="textarea"
                  placeholder="説明文を入力"
                  v-model="post.text"
                ></textarea>
              </div>
            </div>

            <!-- カテゴリフォーム -->
            <PostCategoryForm
              @changeSelectedCategorys="setCategorys($event)"
              @clearDefaultCategorys="clearDefaultCategorysList"
              :defaultCategorys="defaultCategorysList"
            ></PostCategoryForm>

            <!-- 地名・住所フォーム -->
            <PostLocationForm
              @send-zip="saveZipInEdit($event)"
              @send-prefecture="savePrefectureInEdit($event)"
              @send-location="saveLocationInEdit($event)"
              :postZipCode="post.zip_code"
              :postPrefecture="post.prefecture"
              :postLocation="post.location"
            ></PostLocationForm>

            <!-- 公開設定フォーム -->
            <PostStatusForm
              @changeRadio="setStatus($event)"
              :origin="post.status"
            ></PostStatusForm>

            <!-- バリデーションメッセージ -->
            <ValidationMessage :messages="messages"></ValidationMessage>

            <!-- 投稿編集ボタン -->
            <div class="field is-grouped mt-5 mb-2">
              <button
                class="button button-border is-primary is-fullwidth"
                @click="editPost"
                :disabled="disabled"
              >
                投稿を編集する
              </button>
            </div>
            <hr />

            <!-- 投稿削除フォーム -->
            <div class="field mt-5">
              <!-- フォームラベル -->
              <label class="label">投稿を削除</label>

              <!-- 削除確認 -->
              <div class="control">
                <p class="help">
                  投稿を削除する場合は「削除」と入力してください。
                </p>
                <input
                  class="input"
                  type="text"
                  placeholder="削除"
                  v-model="deleteText"
                />
              </div>
            </div>

            <!-- 投稿削除ボタン -->
            <div class="field is-grouped mt-5 mb-2">
              <button
                class="button is-danger is-fullwidth button-border"
                :disabled="!isInput || disabled"
                @click="deletePost"
              >
                削除
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
  data() {
    return {
      post: {},
      deleteText: "",
      defaultCategorysList: [],
      zipCodeInEditForm: "",
      prefectureDataInEditForm: "",
      locationDataInEditForm: "",
      newPicture: null,
      newFileName: "",
      disabled: false,
      messages: [],
    };
  },
  computed: {
    // 削除確認
    isInput() {
      return this.deleteText === "削除";
    },
  },
  components: {
    GlobalMenu,
    PostLocationForm,
    PostStatusForm,
    PostCategoryForm,
    PostImageForm,
    ValidationMessage,
    Message,
  },
  props: ["id"],
  mounted() {
    // 編集対象の投稿を取得
    api
      .get("/users_post/" + this.id + "/")
      .then((response) => {
        this.post = response.data;
        this.defaultCategorysList = response.data.category;
      })
      .catch((error) => {
        // 認証エラー発生時
        if (error.response.status === 401) {
          // ホームへ
          this.$router.push("/");
        }
      });
  },
  methods: {
    setImageFile(...newFileData) {
      // 画像ファイル(Blob)を保存
      this.newPicture = newFileData[0];
      // 画像ファイル名を保存
      this.newFileName = newFileData[1];
    },
    setCategorys(newCategorys) {
      this.post.category = newCategorys;
    },
    clearDefaultCategorysList() {
      this.defaultCategorysList = [];
    },
    setStatus(newStatus) {
      this.post.status = newStatus;
    },
    editPost() {
      this.disabled = true;
      // メッセージの初期化
      this.messages = [];

      // 入力必須項目が空の場合のメッセージ
      if (!this.post.title) {
        this.messages.push("タイトルは必須項目です。");
        this.disabled = false;
        return;
      }

      // 送信データ作成
      const params = new FormData();
      // 元の投稿データから画像関連の属性を削除
      delete this.post.picture_url;
      delete this.post.picture_filename;

      Object.entries(this.post).forEach(([key, value]) => {
        // categoryはManyToManyField
        if (key === "category") {
          value.forEach((value) => {
            params.append("category", value);
          });
        } else {
          params.append(key, value);
        }
      });

      // 画像に変更があった場合
      if (this.newPicture) {
        params.append("picture", this.newPicture, this.newFileName);
      }

      // 地名・住所を設定
      params.append("zip_code", this.zipCodeInEditForm);
      params.append("prefecture", this.prefectureDataInEditForm);
      params.append("location", this.locationDataInEditForm);

      // 投稿を編集
      api
        .patch("/users_post/" + this.id + "/", params)
        .then(() => {
          // 公開設定を非公開に編集した場合
          if (this.post.status === "private") {
            // homeへ遷移
            this.$router.replace({ name: "home" });
          } else {
            // 投稿詳細画面へ
            this.$router.replace({
              name: "viewPost",
              params: { id: this.id, before: "editPost" },
            });
          }
        })
        .catch(() => {
          this.disabled = false;
        });
    },
    deletePost() {
      this.disabled = true;
      // 投稿を削除
      api
        .delete("/users_post/" + this.id + "/")
        .then(() => {
          // ホームへ
          this.$router.replace({
            name: "home",
            params: { before: "deletePost" },
          });
        })
        .catch(() => {
          this.disabled = false;
        });
    },
    saveZipInEdit(zip) {
      // zipが記述済みで半角・全角数字以外の文字が含まれていない場合。
      if (zip && !zip.match(/[^0-9０-９]/g)) {
        // 郵便番号のデータの全角数字を半角に変換。
        const zip1 = zip.replace(/[０-９]/g, (str) => {
          return String.fromCharCode(str.charCodeAt(0) - 0xfee0);
        });
        this.zipCodeInEditForm = zip1;
      } else {
        // 半角・全角数字以外の文字が郵便番号のデータに含まれている場合は郵便番号のデータを初期化。
        this.zipCodeInEditForm = "";
      }
    },
    savePrefectureInEdit(prefectureData) {
      this.prefectureDataInEditForm = prefectureData;
    },
    saveLocationInEdit(locationData) {
      this.locationDataInEditForm = locationData;
    },
  },
};
</script>

<style scoped>
#edit-container {
  padding-top: 40px;
}
.button-border {
  border-radius: 20px;
}
#edit-form {
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