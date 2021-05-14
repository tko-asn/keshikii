import api from '@/api';

const state = {
  username: '',
  isLoggedIn: false,
  favoritePostsIdList: [],
  favoriteUsersList: [] // [{ username: '', icon_url: ''}...]
};

const getters = {
  username: state => state.username,
  isLoggedIn: state => state.isLoggedIn,
  favoritePostsIdList: state => state.favoritePostsIdList,
  favoriteUsersList: state => state.favoriteUsersList
};

const mutations = {
  set(state, payload) {
    state.username = payload.user.username;
    state.isLoggedIn = true;
    state.favoritePostsIdList = payload.user.favorite_posts;
  },
  clear(state) {
    state.username = '';
    state.isLoggedIn = false;
    state.favoritePostsIdList = [];
    state.favoriteUsersList = [];
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
  logout({ commit }) {
    localStorage.removeItem('access'); // 保存していたトークンを削除
    commit('clear'); // stateの認証情報を初期化
  },
  reload({ commit }) {
    // フォローユーザーの情報を取得しstateに保存
    api.get('/following/').then(following => {
      commit('replaceFavoriteUsersList', { favoriteUsersList: following.data });
    });
    return api.get('/auth/users/me/').then(response => { ///
      const user = response.data;
      commit('set', { user: user }); // vuexにユーザー情報をセット
      return user;
    });
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