import axios from 'axios';
import store from './store';

const api = axios.create({
	baseURL: process.env.VUE_APP_API_BASE_URL,
	timeout: 15000,
	headers: {
		'Content-Type': 'application/json',
		'X-Requested-With': 'XMLHttpRequest'
	}
});


api.interceptors.request.use(
	config => {
		store.dispatch('message/clearMessages');
		// apiを叩くときは必ずtokenの検証を行っている。
		const token = localStorage.getItem('access');
		if (token) {
			config.headers.Authorization = 'JWT ' + token;
			return config;
			// トークンがない場合はそのまま（認証が必要なページはbeforeEnterでアクセス制限）
		} else {
			return config;
		}
	},
	error => Promise.reject(error)
);


api.interceptors.response.use(
	response => response,
	error => {
		// console.log('error.response = ', error.response);
		store.dispatch('message/setAddition', { messageType: 'error', process: 'api' });
		const statusCode = error.response ? error.response.status : 500;
		let message;
		if (statusCode === 400) { // バリデーションエラー
			store.dispatch('message/setAddition', { messageType: 'warning', process: 'api' });
			let messages = [].concat.apply([], Object.values(error.response.data));
			store.dispatch('message/setWarningMessages', { messages: messages });
		} else if (statusCode === 401) { // 認証エラー
			const token = localStorage.getItem('access');
			if (token != null) {
				message = 'ログインしてください。';
			} else {
				message = '入力項目のいずれかが間違っています。';
			}
			store.dispatch('auth/logout'); // 認証情報とトークンの削除
			store.dispatch('message/setErrorMessage', { message: message });
		} else if (statusCode === 403) { // パーミッションエラー
			message = '許可されていません。';
			store.dispatch('message/setErrorMessage');
		} else {
			message = '問題が発生しました。';
			store.dispatch('message/setErrorMessage', { message: message });
		}
		return Promise.reject(error);
	}
);


const publicApi = axios.create({ // リクエスト時にトークンの検証を行わない。
	baseURL: process.env.VUE_APP_API_BASE_URL,
	timeout: 10000,
	headers: {
		'Content-Type': 'application/json',
		'X-Requested-With': 'XMLHttpRequest'
	}
});


publicApi.interceptors.response.use(
	response => response,
	error => {
		// console.log('error.response = ', error.response);
		store.dispatch('message/setAddition', { messageType: 'error', process: 'api' });
		const statusCode = error.response ? error.response.status : 500;
		let message;
		if (statusCode === 400) { // バリデーションエラー
			store.dispatch('message/setAddition', { messageType: 'warning', process: 'api' })
			let messages = [].concat.apply([], Object.values(error.response.data));
			store.dispatch('message/setWarningMessages', { messages: messages });
		} else if (statusCode === 403) { // パーミッションエラー
			message = '許可されていません。';
			store.dispatch('message/setErrorMessage');
		} else {
			message = '問題が発生しました。';
			store.dispatch('message/setErrorMessage', { message: message });
		}
		return Promise.reject(error);
	}
);


export default api;

export { publicApi };
