<template>
  <div>
    <!-- モーダル -->
    <ModalWindow :showWindow="modalInfo" @removeWindow="removeModalWindow">
      <!-- フォローしているユーザー -->
      <template v-slot:favoriteUsers>
        <ViewFavoriteUsers
          :username="username"
          :favoriteUsers="favoriteUsers"
          @removeModalInViewFavoriteUsers="removeModalWindow"
        ></ViewFavoriteUsers>
      </template>

      <!-- フォロワー -->
      <template v-slot:followers>
        <ViewFollowers
          :followers="followers"
          :username="username"
          @removeModalInViewFollowers="removeModalWindow"
        ></ViewFollowers>
      </template>
    </ModalWindow>

    <!-- ヘッダー -->
    <GlobalMenu></GlobalMenu>

    <!-- メッセージ -->
    <Message></Message>

    <div id="view-user-container">
      <div class="container">
        <!-- ユーザーアイコン・ユーザー名・フォローボタン -->
        <UserProfileArea :user="user"></UserProfileArea>

        <section class="info-tiles mb-5">
          <div class="tile is-ancestor has-text-centered">
            <!-- 投稿数タイル -->
            <div class="tile is-parent">
              <article
                class="tile is-child box click-cursor"
                @click="switchTab(1)"
              >
                <p class="title">{{ count }}</p>
                <p class="subtitle">投稿数</p>
              </article>
            </div>

            <!-- フォロワータイル -->
            <div class="tile is-parent">
              <article
                class="tile is-child box click-cursor"
                @click="showFollowers"
              >
                <p class="title">{{ followCount }}</p>
                <p class="subtitle">フォロワ―</p>
              </article>
            </div>

            <!-- フォロータイル -->
            <div class="tile is-parent">
              <article
                class="tile is-child box click-cursor"
                @click="showFavoriteUsers"
              >
                <p class="title">{{ favoriteUsersCount }}</p>
                <p class="subtitle">フォロー</p>
              </article>
            </div>
          </div>
        </section>

        <!-- タブメニュー -->
        <TabMenu
          :tabNameList="tabNameInViewUserPage"
          :option="optionNumber"
          @returnTabIndex="switchElement($event)"
          @resetOption="resetOptionNumber"
        ></TabMenu>

        <!-- ユーザー概要 -->
        <UserOverview :user="user" v-show="elementNumber === 0"></UserOverview>

        <!-- 投稿一覧 -->
        <div v-show="elementNumber === 1">
          <!-- 投稿が存在する場合 -->
          <template v-if="posts.length">
            <PostsList :posts="posts"></PostsList>
            <Pagination
              :id="user.id"
              class="mt-5"
              @paginate="movePage"
            ></Pagination>
          </template>

          <!-- 投稿が存在しない場合 -->
          <template v-else>
            {{ noPosts }}
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { publicApi } from "@/api";
import GlobalMenu from "@/components/GlobalMenu";
import ModalWindow from "@/components/ModalWindow";
import ViewFavoriteUsers from "@/components/ViewFavoriteUsers";
import ViewFollowers from "@/components/ViewFollowers";
import TabMenu from "@/components/TabMenu";
import PostsList from "@/components/PostsList";
import Pagination from "@/components/Pagination";
import UserProfileArea from "@/components/UserProfileArea";
import UserOverview from "@/components/UserOverview";
import Message from "@/components/Message";
import store from "@/store";

export default {
  components: {
    GlobalMenu,
    ModalWindow,
    ViewFavoriteUsers,
    ViewFollowers,
    TabMenu,
    PostsList,
    Pagination,
    UserProfileArea,
    UserOverview,
    Message,
  },
  mounted() {
    // ユーザーの情報を取得
    publicApi
      .get("/custom_users/" + this.username + "/")
      .then((userResponse) => {
        this.user = userResponse.data;

        // ユーザーのフォローしているユーザーを取得
        publicApi
          .get("/following/", { params: { other: this.user.id } })
          .then((followingObjects) => {
            // userのフォローユーザーを取得
            followingObjects.data.forEach((followerInfo) => {
              this.favoriteUsers.push(followerInfo);
            });
            this.favoriteUsersCount = followingObjects.data.length;
          });

        // ユーザーのフォロワーを取得
        publicApi
          .get("/following/", {
            params: { followers: "True", user: this.user.id },
          })
          .then((followingObjects) => {
            // userのフォロワーを取得
            followingObjects.data.forEach((following) => {
              this.followers.push(following.followed_by);
            });
            this.followCount = followingObjects.data.length;
          });

        // ユーザーの投稿を取得
        publicApi
          .get("/posts/", {
            params: {
              user_id: this.user.id,
            },
          })
          .then((postResponse) => {
            // ページネーションの状態をセット
            this.$store.dispatch("pagination/setPagination", postResponse.data);
            this.posts = postResponse.data.results;
            this.count = postResponse.data.count;
            if (!postResponse.data.count) {
              this.noPosts = "投稿はありません。";
            }
          });
      });
  },
  props: ["username"], // urlから対象ユーザーのusernameを取得
  data() {
    return {
      user: {},
      posts: [],
      count: 0,
      followers: [],
      followCount: 0,
      favoriteUsers: [],
      favoriteUsersCount: 0,
      modalInfo: {
        hideWindow: true,
        slotName: "",
      },
      tabNameInViewUserPage: ["プロフィール", "投稿一覧"],
      elementNumber: 0,
      optionNumber: false,
      noPosts: "",
    };
  },
  methods: {
    showFollowers() {
      this.modalInfo.slotName = "followers";
      this.modalInfo.hideWindow = false;
    },
    showFavoriteUsers() {
      this.modalInfo.slotName = "favoriteUsers";
      this.modalInfo.hideWindow = false;
    },
    removeModalWindow() {
      this.modalInfo.slotName = "";
      this.modalInfo.hideWindow = true;
    },
    switchElement(elementIndex) {
      this.elementNumber = elementIndex;
    },
    switchTab(num) {
      if (this.elementNumber !== num) {
        this.optionNumber = num;
        this.elementNumber = num;
      }
    },
    resetOptionNumber() {
      this.optionNumber = false;
    },
    // ページネーション
    movePage(posts) {
      this.posts = posts;
    },
  },
  beforeRouteEnter(to, from, next) {
    const loginUsername = store.getters["auth/username"];
    // ViewUserPageの表示内容が自分の場合はmypageへ飛ばす
    if (to.params.username === loginUsername) {
      next("/mypage");
    } else {
      next();
    }
  },
  // フォロワー・フォローのモーダルから
  // ログインユーザー以外のユーザーが選択されたとき
  // URLのparamsの変更を検知
  beforeRouteUpdate(to, from, next) {
    // タブメニューを初期化
    this.elementNumber = 0;
    this.optionNumber = 0;

    // ユーザーの情報を取得
    publicApi
      .get("/custom_users/" + to.params.username + "/")
      .then((userResponse) => {
        this.user = userResponse.data;

        // ユーザーのフォローしているユーザーを取得
        publicApi
          .get("/following/", { params: { other: this.user.id } })
          .then((followingObjects) => {
            // フォローユーザーのリストを初期化
            this.favoriteUsers = [];
            // userのフォローユーザーを取得
            followingObjects.data.forEach((followerInfo) => {
              this.favoriteUsers.push(followerInfo);
            });
            this.favoriteUsersCount = followingObjects.data.length;
          });

        // ユーザーのフォロワーを取得
        publicApi
          .get("/following/", {
            params: { followers: "True", user: this.user.id },
          })
          .then((followingObjects) => {
            // フォロワーのリストを初期化
            this.followers = [];
            // userのフォロワーを取得
            followingObjects.data.forEach((following) => {
              this.followers.push(following.followed_by);
            });
            this.followCount = followingObjects.data.length;
          });

        // ユーザーの投稿を取得
        publicApi
          .get("/posts/", {
            params: {
              user_id: this.user.id,
            },
          })
          .then((postResponse) => {
            // ページネーションの状態をセット
            this.$store.dispatch("pagination/setPagination", postResponse.data);
            this.posts = postResponse.data.results;
            this.count = postResponse.data.count;
            if (!postResponse.data.count) {
              this.noPosts = "投稿はありません。";
            }
          });
      });
    next();
  },
};
</script>

<style scoped>
#view-user-container {
  padding-top: 100px;
}
.click-cursor {
  cursor: pointer;
}
.click-cursor:hover {
  filter: brightness(90%);
}
</style>
