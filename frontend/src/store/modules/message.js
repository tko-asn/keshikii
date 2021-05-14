const state = {
	error: '',
	warnings: [],
	info: '',
	addition: {
		type: '',
		process: ''
	}
};

const getters = {
	error: state => state.error,
	warnings: state => state.warnings,
	info: state => state.info,
	addition: state => state.addition
};

const mutations = {
	set(state, payload) {
		if (payload.error) {
			state.error = payload.error;
		}
		if (payload.warnings) {
			state.warnings = payload.warnings;
		}
		if (payload.info) {
			state.info = payload.info;
		}
	},
	clear(state) {
		state.error = '';
		state.warnings = [];
		state.info = '';
	},
	setAddition(state, payload) {
		state.addition.type = payload.messageType;
		state.addition.process = payload.process;
	},
	clearAddition(state) {
		state.addition.type = '';
		state.addition.process = '';
	}
};

const actions = {
	setErrorMessage({ commit }, payload) {
		commit('clear');
		commit('set', { error: payload.message })
	},
	setWarningMessages({ commit }, payload) {
		commit('clear');
		commit('set', { warnings: payload.messages })
	},
	setInfoMessage({ commit }, payload) {
		commit('clear');
		commit('set', { info: payload.message })
	},
	clearMessages({ commit }) {
		commit('clear');
	},
	setAddition({ commit }, payload) {
		commit('setAddition', { messageType: payload.messageType, process: payload.process });
	},
	clearAddition({ commit }) {
		commit('clearAddition');
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