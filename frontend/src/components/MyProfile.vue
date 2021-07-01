<template>
  <div>
    <section class="info-tiles mb-5">
      <div class="tile is-ancestor has-text-centered">
        <!-- 投稿数 -->
        <div class="tile is-parent">
          <article class="tile is-child box click-cursor" @click="moveTab(1)">
            <p class="title">{{ count }}</p>
            <p class="subtitle">投稿数</p>
          </article>
        </div>

        <!-- フォロワー -->
        <div class="tile is-parent">
          <article
            class="tile is-child box click-cursor"
            @click="showMyFollowers"
          >
            <p class="title">{{ numberOfFollowers }}</p>
            <p class="subtitle">フォロワ―</p>
          </article>
        </div>

        <!-- お気に入りの投稿 -->
        <div class="tile is-parent">
          <article class="tile is-child box click-cursor" @click="moveTab(2)">
            <p class="title">{{ numberOfFavoritePosts }}</p>
            <p class="subtitle">お気に入り</p>
          </article>
        </div>

        <!-- フォローしているユーザー -->
        <div class="tile is-parent">
          <article
            class="tile is-child box click-cursor"
            @click="showMyFavoriteUsers"
          >
            <p class="title">{{ favoriteUsersList.length }}</p>
            <p class="subtitle">フォロー</p>
          </article>
        </div>
      </div>
    </section>

    <!-- ユーザーの概要部分 -->
    <UserOverview :user="user"></UserOverview>
  </div>
</template>

<script>
import api from "@/api";
import UserOverview from "@/components/UserOverview";
import { mapGetters } from "vuex";

export default {
  props: ["user"],
  components: {
    UserOverview,
  },
  data() {
    return {
      numberOfFollowers: 0,
      myFollowers: [],
    };
  },
  mounted() {
    // ログインユーザーのフォロワー取得
    api
      .get("/following/", { params: { followers: "True" } })
      .then((followingObjects) => {
        followingObjects.data.forEach((following) => {
          // フォロワーのデータをmyFollowersに格納していく
          this.myFollowers.push(following.followed_by);
          // フォロワー数
          this.numberOfFollowers = followingObjects.data.length;
        });
      });
  },
  computed: {
    // フォローしているユーザーのリスト
    ...mapGetters("auth", ["favoriteUsersList"]),
    ...mapGetters("pagination", ["count"]), // 投稿数
    numberOfFavoritePosts() {
      if (this.user.favorite_posts) {
        return this.user.favorite_posts.length;
      }
      return 0;
    },
  },
  methods: {
    // フォロワーボタンをクリックされたとき
    // 親コンポーネントのモーダルでフォロワーを表示
    showMyFollowers() {
      this.$emit("showFollowers", this.myFollowers);
    },
    // フォローボタンを押されたとき
    // 親コンポーネントのモーダルでフォローしているユーザーを表示
    showMyFavoriteUsers() {
      // mypageでのViewFavoriteUserはvuexから値を得るため
      // ここからデータを送らなくていい
      this.$emit("showFavoriteUsers");
    },
    // 投稿数orお気に入りボタンを押されたとき
    // 親コンポーネントでタブ移動
    moveTab(tabIndex) {
      this.$emit("moveTabInMyPage", tabIndex);
    },
  },
};
</script>

<style scoped>
.click-cursor {
  cursor: pointer;
}
.click-cursor:hover {
  filter: brightness(90%);
}
</style>