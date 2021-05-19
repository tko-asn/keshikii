<template>
  <div>
    <ModalWindow
      :showWindow="modalInfo"
      @removeWindow="removeModalWindowInMyPage"
    >
      <template v-slot:favoriteUsers>
        <ViewFavoriteUsers
          :username="user.username"
          @removeModalInViewFavoriteUsers="removeModalWindowInMyPage"
        ></ViewFavoriteUsers>
      </template>
      <template v-slot:followers>
        <ViewFollowers
          :followers="followers"
          :username="user.username"
          @removeModalInViewFollowers="removeModalWindowInMyPage"
        ></ViewFollowers>
      </template>
    </ModalWindow>
    <GlobalMenu></GlobalMenu>
    <Message :info="messages.informations"></Message>
    <div id="mypage-container" class="container">
      <UserProfileArea :user="user"></UserProfileArea>
    </div>
    <TabMenu :routesList="routeName" :tabNameList="tabName"></TabMenu>
    <div class="container">
      <keep-alive>
        <MyProfile
          v-show="isMyPageRoute"
          :user="user"
          @showFollowers="showFollowersInMyPage($event)"
          @showFavoriteUsers="showFavoriteUsersInMyPage"
          @moveTabInMyPage="goToAnotherTab($event)"
        ></MyProfile>
      </keep-alive>
      <keep-alive>
        <router-view></router-view>
      </keep-alive>
    </div>
  </div>
</template>

<script>
import api from "@/api";
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
      user: {},
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
    showFollowersInMyPage(myFollowers) {
      this.followers = myFollowers;
      this.modalInfo.slotName = "followers";
      this.modalInfo.hideWindow = false;
    },
    showFavoriteUsersInMyPage() {
      this.modalInfo.slotName = "favoriteUsers";
      this.modalInfo.hideWindow = false;
    },
    removeModalWindowInMyPage() {
      this.modalInfo.slotName = "";
      this.modalInfo.hideWindow = true;
    },
    goToAnotherTab(tabIndex) {
      const nextRoute = this.routeName[tabIndex];
      this.$router.push({ name: nextRoute });
    },
  },
  mounted() {
    const searchRouteIndex = this.routeName.indexOf(this.$route.name);
    this.isActive = searchRouteIndex;
    api.get("/auth/users/me/").then((response) => {
      this.user = response.data;
    });
  },
  computed: {
    isMyPageRoute() {
      return this.$route.name === "mypage";
    },
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