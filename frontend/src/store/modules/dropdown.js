const state = {
  isDown: false,
  isOpen: false
};

const getters = {
  isDown: state => state.isDown,
  isOpen: state => state.isOpen
};

const mutations = {
  setIsDown(state, status) {
    state.isDown = status;
  },
  setIsOpen(state, status) {
    state.isOpen = status;
  }
};

const actions = {
  changeIsDown({ commit }, status) {
    commit('setIsDown', status);
  },
  changeIsOpen({ commit }, status) {
    commit('setIsOpen', status);
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