import Vue from 'vue';
import Vuex from 'vuex';
import auth from './modules/auth';
import pagination from './modules/pagination';
import dropdown from './modules/dropdown';
import messages from './modules/messages';

Vue.use(Vuex);

export default new Vuex.Store({
	modules: {
		auth,
		pagination,
		dropdown,
		messages
	}
});