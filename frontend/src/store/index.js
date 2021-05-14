import Vue from 'vue';
import Vuex from 'vuex';
import auth from './modules/auth';
import message from './modules/message';
import pagination from './modules/pagination';
import dropdown from './modules/dropdown';

Vue.use(Vuex);

export default new Vuex.Store({
	modules: {
		auth,
		message,
		pagination,
		dropdown
	}
});