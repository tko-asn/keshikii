<template>
  <div>
    <!-- モーダルウィンドウ -->
    <ModalWindow
      :showWindow="modalInfo"
      @removeWindow="removeModalWindowInMyPage"
    >
      <!-- フォローしているユーザーを表示するモーダルの場合 -->
      <template v-slot:favoriteUsers>
        <ViewFavoriteUsers
          :username="userProfile.username"
          @removeModalInViewFavoriteUsers="removeModalWindowInMyPage"
        ></ViewFavoriteUsers>
      </template>

      <!-- フォロワーを表示するモーダルの場合 -->
      <template v-slot:followers>
        <ViewFollowers
          :followers="followers"
          :username="userProfile.username"
          @removeModalInViewFollowers="removeModalWindowInMyPage"
        ></ViewFollowers>
      </template>
    </ModalWindow>

    <!-- ヘッダー -->
    <GlobalMenu></GlobalMenu>

    <!-- メッセージ -->
    <Message :info="messages.informations"></Message>

    <!-- ユーザアイコン, ユーザー名, プロフィール編集ボタンを表示する部分 -->
    <div id="mypage-container" class="container">
      <UserProfileArea :user="userProfile"></UserProfileArea>
    </div>

    <!-- タブメニュー -->
    <TabMenu :routesList="routeName" :tabNameList="tabName"></TabMenu>

    <div class="container">
      <!-- プロフィールタブ -->
      <keep-alive>
        <MyProfile
          v-show="isMyPageRoute"
          :user="userProfile"
          @showFollowers="showFollowersInMyPage($event)"
          @showFavoriteUsers="showFavoriteUsersInMyPage"
          @moveTabInMyPage="goToAnotherTab($event)"
        ></MyProfile>
      </keep-alive>

      <!-- それ以外のタブ -->
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import GlobalMenu from "@/components/GlobalMenu";
import MyProfile from "@/components/MyProfile";
import ModalWindow from "@/components/ModalWindow";
import ViewFavoriteUsers from "@/components/ViewFavoriteUsers";
import ViewFollowers from "@/components/ViewFollowers";
import TabMenu from "@/components/TabMenu";
import UserProfileArea from "@/components/UserProfileArea";
import Message from "@/components/Message";

export default {
  data() {
    return {
      routeName: ["mypage", "myPosts", "favoritePosts"],
      tabName: ["プロフィール", "自分の投稿", "お気に入りの投稿"],
      favoriteUsers: [],
      followers: [],
      modalInfo: {
        hideWindow: true,
        slotName: "",
      },
      messages: {
        informations: [],
      },
    };
  },
  components: {
    GlobalMenu,
    MyProfile,
    ModalWindow,
    ViewFavoriteUsers,
    ViewFollowers,
    TabMenu,
    UserProfileArea,
    Message,
  },
  methods: {
    // フォロワーを表示するモーダルを表示
    showFollowersInMyPage(myFollowers) {
      // myFollowers: MyProfileから送られてきたフォロワーのデータ
      this.followers = myFollowers;
      this.modalInfo.slotName = "followers";
      this.modalInfo.hideWindow = false;
    },
    // フォローしているユーザーを表示するモーダルを表示
    showFavoriteUsersInMyPage() {
      // ログインユーザー自身のフォローしているユーザーはvuexから
      // 参照できるのでViewFavoriteUsersコンポーネントのpropsには
      // データを送らなくていい
      this.modalInfo.slotName = "favoriteUsers";
      this.modalInfo.hideWindow = false;
    },
    // モーダルを非表示にするための処理
    removeModalWindowInMyPage() {
      this.modalInfo.slotName = "";
      this.modalInfo.hideWindow = true;
    },
    // タブ移動の処理
    goToAnotherTab(tabIndex) {
      const nextRoute = this.routeName[tabIndex];
      this.$router.push({ name: nextRoute });
    },
  },
  mounted() {
    // 現在のURLのrouteNameでのインデックスを取得
    const searchRouteIndex = this.routeName.indexOf(this.$route.name);
    // URLに応じてisActiveの値を変える
    this.isActive = searchRouteIndex;
  },
  computed: {
    // 現在のタブがプロフィールかどうか
    // URLが/mypageのみのときはプロフィールタブを表示する
    // これでMyProfileコンポーネントの表示を切り替える
    isMyPageRoute() {
      return this.$route.name === "mypage";
    },
    // ログインユーザーの情報
    ...mapGetters("auth", ["userProfile"]),
  },
  // メッセージの表示が必要な場合は
  // dataのmessagesに値を保存して
  // Messageコンポーネントに渡す
  beforeRouteEnter(to, from, next) {
    if (to.params.before === "editProfile") {
      next((vm) => {
        vm.messages.informations.push("プロフィールを編集しました。");
      });
    } else {
      next();
    }
  },
};
</script>

<style scoped>
#mypage-container {
  padding-top: 100px;
}
</style>