<template>
  <div>
    <GlobalMenu></GlobalMenu>
    <GlobalMessage></GlobalMessage>
    <div id="post-container" class="container mt-6 mb-6">
      <div class="columns is-centered">
        <form
          id="post-form"
          @submit.prevent="createPost"
          class="box column is-5-desktop is-6-tablet is-8-mobile"
        >
          <div id="form-container">
            <div class="content mt-6">
              <h1 class="has-text-centered">Post Form</h1>
            </div>
            <PostImageForm
              @changeImage="setImageFile($event)"
              :defaultSrc="''"
              :defaultFileName="''"
            ></PostImageForm>
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
            <div class="field mt-5">
              <div class="control pt-3">
                <textarea
                  class="textarea"
                  placeholder="説明文を入力"
                  v-model="newPost.text"
                ></textarea>
              </div>
            </div>
            <PostCategoryForm
              @changeSelectedCategorys="setCategorys($event)"
              :defaultCategorys="[]"
            ></PostCategoryForm>
            <PostLocationForm
              @send-zip="saveZip($event)"
              @send-prefecture="savePrefecture($event)"
              @send-location="saveLocation($event)"
            ></PostLocationForm>
            <PostStatusForm @changeRadio="setStatus($event)" :origin="''"></PostStatusForm>
            <div class="field is-grouped mt-5 mb-2">
              <button class="button button-border is-primary is-fullwidth">
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
import GlobalMessage from "@/components/GlobalMessage";
import PostLocationForm from "@/components/PostLocationForm";
import PostStatusForm from "@/components/PostStatusForm";
import PostCategoryForm from "@/components/PostCategoryForm";
import PostImageForm from "@/components/PostImageForm";

export default {
  components: {
    GlobalMenu,
    GlobalMessage,
    PostLocationForm,
    PostStatusForm,
    PostCategoryForm,
    PostImageForm,
  },
  data() {
    return {
      newPost: {
        picture: null,
        title: "",
        text: "",
        status: "public",
      },
      selectedCategory: [],
      zipCode: "",
      prefecture: "",
      location: "",
    };
  },
  methods: {
    setImageFile(newFileData) {
      this.newPost.picture = newFileData;
    },
    setCategorys(categorysList) {
      this.selectedCategory = categorysList;
    },
    setStatus(newStatus) {
      this.newPost.status = newStatus;
    },
    createPost() {
      const params = new FormData();
      Object.entries(this.newPost).forEach(([key, value]) => {
        params.append(key, value);
      });
      this.selectedCategory.forEach((value) => {
        // manytomanyfieldなのでひとつずつ加える。
        params.append("category", value);
      });
      params.append("zip_code", this.zipCode);
      params.append("prefecture", this.prefecture);
      params.append("location", this.location);
      api.post("/users_post/", params).then(() => {
        this.$router.push({ name: "home", params: { before: "create" } });
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