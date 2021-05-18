const state = {
  messages: []
};

const getters = {
  messages: state => state.messages
};

const mutations = {
  addMessage(state, message) {
    state.messages.push(message);
  },
  clearMessage(state) {
    state.messages = [];
  },
  removeMessage(state, message) {
    state.messages = state.messages.filter(v => v !== message);
  }
};

const actions = {
  add({ commit }, message) {
    commit('addMessage', message);
  },
  clear({ commit }) {
    commit('clearMessage');
  },
  remove({ commit }, message) {
    commit('removeMessage', message);
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