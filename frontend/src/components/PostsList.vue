<template>
  <div class="row columns is-multiline is-marginless">
    <!-- 投稿カード部分 -->
    <div
      v-for="post in posts"
      :key="post.id"
      class="column is-4 click-cursor"
      @click="viewPost(post.id)"
    >
      <div class="card">
        <!-- 投稿写真部分 -->
        <div class="card-image">
          <div class="image-box">
            <img :src="post.picture_url" :alt="post.title" />
          </div>
        </div>

        <div class="card-content">
          <div class="post-box">
            <!-- 投稿者アイコン -->
            <div class="icon-box">
              <img :src="post.author.icon_url" alt="icon" />
            </div>
            <!-- 投稿タイトル・投稿者名 -->
            <div>
              <p class="title is-4 no-padding">{{ post.title }}</p>
              <p class="subtitle is-6">{{ post.author.username }}の投稿</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ["posts"],
  methods: {
    viewPost(postId) {
      this.$router.push({ name: "viewPost", params: { id: postId } });
    },
  },
};
</script>

<style scoped>
.image-box {
  /* アスペクト比の統一 */
  width: 100%;
  padding-top: 60%;
  position: relative;
}
.image-box img {
  /* 画像のトリミング */
  position: absolute;
  width: 100%;
  height: 100%;
  object-fit: cover;
  top: 0;
}
.card {
  height: 100%;
}
.icon-box {
  height: 50px;
  width: 50px;
  margin-right: 10%;
}
.icon-box img {
  height: 50px;
  width: 50px;
  object-fit: cover;
  border-radius: 50%;
}
.post-box {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
}
.click-cursor {
  cursor: pointer;
}
.click-cursor:hover {
  filter: brightness(90%);
}
@media screen and (max-width: 768px) {
  .icon-box {
    height: 40px;
    width: 40px;
  }
  .icon-box img {
    height: 40px;
    width: 40px;
  }
}
</style>