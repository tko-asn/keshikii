<template>
  <div>
    <section class="info-tiles mb-5">
      <div class="tile is-ancestor has-text-centered">
        <div class="tile is-parent">
          <article class="tile is-child box click-cursor" @click="moveTab(1)">
            <p class="title">{{ myPostsCount }}</p>
            <p class="subtitle">投稿数</p>
          </article>
        </div>
        <div class="tile is-parent">
          <article
            class="tile is-child box click-cursor"
            @click="showMyFollowers"
          >
            <p class="title">{{ numberOfFollowers }}</p>
            <p class="subtitle">フォロワ―</p>
          </article>
        </div>
        <div class="tile is-parent">
          <article class="tile is-child box click-cursor" @click="moveTab(2)">
            <p class="title">{{ numberOfFavoritePosts }}</p>
            <p class="subtitle">お気に入り</p>
          </article>
        </div>
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
      myPostsCount: 0,
      myFollowers: [],
    };
  },
  mounted() {
    api.get("/users_post/").then((response) => {
      this.myPostsCount = response.data.count;
    });
    api
      .get("/following/", { params: { followers: "True" } })
      .then((followingObjects) => {
        followingObjects.data.forEach((following) => {
          this.myFollowers.push(following.followed_by);
          this.numberOfFollowers = followingObjects.data.length;
        });
      });
  },
  computed: {
    ...mapGetters("auth", ["favoriteUsersList"]),
    numberOfFavoritePosts() {
      if (this.user.favorite_posts) {
        return this.user.favorite_posts.length;
      }
      return 0;
    },
  },
  methods: {
    showMyFollowers() {
      this.$emit("showFollowers", this.myFollowers);
    },
    showMyFavoriteUsers() {
      // mypageでのViewFavoriteUserはvuexから値を得るためここからデータを送らなくていい。
      this.$emit("showFavoriteUsers");
    },
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