import api from '@/api';

const state = {
  username: '',
  userProfile: {}, // ユーザー情報がすべて入ったオブジェクト
  isLoggedIn: false, // ログイン状態
  favoritePostsIdList: [],
  favoriteUsersList: [] // [{ username: '', icon_url: ''}...]
};

const getters = {
  username: state => state.username,
  userProfile: state => state.userProfile,
  isLoggedIn: state => state.isLoggedIn,
  favoritePostsIdList: state => state.favoritePostsIdList,
  favoriteUsersList: state => state.favoriteUsersList
};

const mutations = {
  set(state, payload) {
    // usernameを保存
    state.username = payload.user.username;

    // ユーザーのすべてのプロフィールを保存
    state.userProfile = payload.user;

    // お気に入りの投稿のIDのリストを作成
    state.favoritePostsIdList = payload.user.favorite_posts;

    // ログイン状態をtrueに変更
    state.isLoggedIn = true;
  },
  clear(state) {
    // ユーザー名を初期化
    state.username = '';

    // ユーザーのプロフィール情報を初期化
    state.userProfile = {};

    // ログイン状態をfalseに変更
    state.isLoggedIn = false;
  },
  // ユーザー情報の変更
  editProfile(state, newUserProfile) {
    state.username = newUserProfile.username;
    state.userProfile = newUserProfile;
  },
  replaceFavoritePostsIdList(state, payload) {
    state.favoritePostsIdList = payload.favoritePostsIdList;
  },
  deleteFavoritePost(state, payload) {
    const favoritesList = state.favoritePostsIdList;
    state.favoritePostsIdList = favoritesList.filter(id => id !== payload.postId);
  },
  replaceFavoriteUsersList(state, payload) {
    state.favoriteUsersList = payload.favoriteUsersList;
  },
  addFavoriteUser(state, payload) {
    state.favoriteUsersList.push(payload.data);
  },
  deleteFavoriteUser(state, payload) {
    const favoritesList = state.favoriteUsersList;
    state.favoriteUsersList = favoritesList.filter(data => data !== payload.data);
  }
};

const actions = {
  // サインアップ
  register(context, payload) {
    return api.post(
      '/auth/users/',
      {
        username: payload.username,
        password: payload.password,
        re_password: payload.rePassword
      }
    );
  },
  // ログイン
  login({ dispatch }, payload) {
    return api.post(
      '/auth/jwt/create/',
      {
        'username': payload.username,
        'password': payload.password
      }
    )
      .then(response => {
        localStorage.setItem('access', response.data.access);
        return dispatch('reload').then(user => user);
      });
  },
  // ログアウト
  logout({ commit }) {
    localStorage.removeItem('access'); // 保存していたトークンを削除
    commit('clear'); // stateの認証情報を初期化
  },
  // stateのユーザー情報を更新
  reload({ commit }) {
    // フォローユーザーの情報を取得しstateに保存
    api.get('/following/').then(following => {
      commit('replaceFavoriteUsersList', { favoriteUsersList: following.data });
    });
    // ユーザーのプロフィール情報をstateにセット
    return api.get('/auth/users/me/').then(response => {
      const user = response.data;
      commit('set', { user: user }); // stateにユーザー情報をセット
      return user;
    });
  },
  // ユーザー情報の変更
  // EditProfilePageにてユーザー情報を変更したときに実行
  editUserProfile({ commit }, newUserProfile) {
    commit('editProfile', newUserProfile)
  },
  setFavoritePostsIdList({ commit }, favoritePostsIdList) {
    commit('replaceFavoritePostsIdList', { favoritePostsIdList: favoritePostsIdList });
  },
  removeFavoritePost({ commit }, postId) {
    commit('deleteFavoritePost', { postId: postId });
  },
  setFavoriteUser({ commit }, favoriteUser) {
    commit('addFavoriteUser', { data: favoriteUser });
  },
  removeFavoriteUser({ commit }, favoriteUser) {
    commit('deleteFavoriteUser', { data: favoriteUser });
  }
};

export default {
  strict: process.env.NODE_ENV !== 'production',
  namespaced: true,
  state,
  getters,
  mutations,
  actions
};