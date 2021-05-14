const state = {
	next: '',
	previous: '',
	count: 0,
	totalPages: 0,
	currentPage: 0,
	pageSize: 0,
	searchKeyword: '',
	searchCategorys: [],
	searchPrefecture: ''
};

const getters = {
	next: state => state.next,
	previous: state => state.previous,
	count: state => state.count,
	totalPages: state => state.totalPages,
	currentPage: state => state.currentPage,
	previousPage: state => state.currentPage - 1,
	nextPage: state => state.currentPage + 1,
	pageSize: state => state.pageSize,
	hasNext: state => !!state.next,
	hasPrevious: state => !!state.previous,
	searchKeyword: state => state.searchKeyword,
	searchCategorys: state => state.searchCategorys,
	searchPrefecture: state => state.searchPrefecture
};

const mutations = {
	set(state, payload) {
		state.next = payload.next;
		state.previous = payload.previous;
		state.count = payload.count;
		state.totalPages = payload.total_pages;
		state.currentPage = payload.current_page;
		state.pageSize = payload.page_size;
	},
	setSearchKeyword(state, payload) { // こっちもクリアしないと値が残るかも
		state.searchKeyword = payload.searchKeyword;
	},
	setSearchCategorys(state, payload) {
		state.searchCategorys = payload.searchCategorys;
	},
	setSearchPrefecture(state, payload) {
		state.searchPrefecture = payload.searchPrefecture;
	},
	clearSearchKeyword(state) {
		state.searchKeyword = '';
	},
	clearSearchCategorys(state) {
		state.searchCategorys = [];
	},
	clearSearchPrefecture(state) {
		state.searchPrefecture = '';
	}
};

const actions = {
	setPagination({ commit }, payload) {
		commit('set', payload);
	},
	registerSearchKeyword({ commit }, payload) {
		commit('setSearchKeyword', { searchKeyword: payload });
	},
	registerSearchCategorys({ commit }, payload) {
		commit('setSearchCategorys', { searchCategorys: payload });
	},
	registerSearchPrefecture({ commit }, payload) {
		commit('setSearchPrefecture', { searchPrefecture: payload });
	},
	destroySearchKeyword({ commit }) {
		commit('clearSearchKeyword');
	},
	destroySearchCategorys({ commit }) {
		commit('clearSearchCategorys');
	},
	destroySearchPrefecture({ commit }) {
		commit('clearSearchPrefecture');
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