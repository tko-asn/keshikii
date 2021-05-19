<template>
  <div>
    <div class="img-box">
      <!-- previewSrcはBase64で変換されたもの -->
      <img :src="previewSrc" />
    </div>
    <div class="file has-name is-fullwidth pt-3">
      <label class="file-label">
        <input
          class="file-input"
          type="file"
          name="resume"
          @change="onImageChange"
        />
        <span class="file-cta">
          <span class="file-icon">
            <fa-icon icon="file-upload"></fa-icon>
          </span>
          <span class="file-label"> 画像を選択 </span>
        </span>
        <span class="file-name">{{ this.fileName }}</span>
      </label>
    </div>
  </div>
</template>

<script>
import Compressor from "compressorjs";

export default {
  props: {
    defaultSrc: {
      type: String,
      default: "",
    },
    defaultFileName: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      previewSrc: "", // imgタグのsrc属性に与える
      picture: null, // 実際に送信するファイル（親コンポーネントに送信）
      fileName: "", // ファイル名
    };
  },
  methods: {
    getFileData(file) {
      return new Promise((resolve, reject) => {
        this.picture = file;
        this.fileName = file.name;
        const fileReader = new FileReader();
        fileReader.readAsDataURL(file);
        fileReader.onload = () => resolve(fileReader.result);
        fileReader.onerror = (error) => reject(error);
      });
    },
    onImageChange(event) {
      const images = event.target.files || event.dataTransfer.files;
      const data = images[0];
      const _this = this;
      // 投稿画像を圧縮
      new Compressor(data, {
        // 圧縮した画像の解像度
        quality: 0.5,
        // 圧縮成功時の処理
        success(result) {
          _this
            .getFileData(result)
            .then((fileData) => {
              _this.previewSrc = fileData;
              // 指定画像の変化があれば新しい画像のファイルを親コンポーネントへ渡す
              _this.$emit("changeImage", _this.picture, _this.fileName);
            });
        },
        maxWidth: 400,
        maxHeight: 400,
        mimeType: "image/jpeg",
        // 圧縮失敗時の処理
        // error() {
        // },
      });
    },
  },
  watch: {
    defaultSrc(val) {
      if (this.defaultSrc) {
        // 投稿編集画面ではデフォルトで設定されているファイルのsrcをpropsで受け取る。
        this.previewSrc = val;
      }
    },
    defaultFileName(val) {
      if (this.defaultFileName) {
        // デフォルトで設定されているファイルのファイル名をpropsで受け取る。
        this.fileName = val;
      }
    },
  },
};
</script>

<style scoped>
.img-box {
  text-align: center;
}
.img-box img {
  max-width: 100%;
  height: auto;
  margin: 0 auto;
}
</style>
