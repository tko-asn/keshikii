import axios from 'axios';
import store from './store';

const api = axios.create({
	baseURL: process.env.VUE_APP_API_BASE_URL,
	timeout: 30000,
	headers: {
		'Content-Type': 'application/json',
		'X-Requested-With': 'XMLHttpRequest'
	}
});


api.interceptors.request.use(
	config => {
		// リクエスト時にメッセージを初期化
		store.dispatch('messages/clear');

		// apiへアクセスするときは必ずtokenの検証を行っている
		const token = localStorage.getItem('access');

		// トークンがある場合
		if (token) {
			// リクエストヘッダに認証トークンを設定
			config.headers.Authorization = 'JWT ' + token;
			return config;

			// トークンがない場合はそのまま
			// 認証が必要なページはbeforeEnterでアクセス制限
		} else {
			return config;
		}
	},
	error => Promise.reject(error)
);


api.interceptors.response.use(
	response => response,
	error => {
		const statusCode = error.response ? error.response.status : 500;
		let message;
		if (statusCode === 400) { // バリデーションエラー
			let messages = [].concat.apply([], Object.values(error.response.data));
			for (const message of messages) {
				store.dispatch('messages/add', message);
			}
		} else if (statusCode === 401) { // 認証エラー
			const token = localStorage.getItem('access');
			if (token != null) {
				message = 'トークンの有効期限によりログアウトしました。';
			} else {
				message = 'ユーザーの認証に失敗しました。';
			}
			store.dispatch('auth/logout'); // 認証情報とトークンの削除
			store.dispatch('messages/add', message);
		} else if (statusCode === 403) { // パーミッションエラー
			message = '許可されていません。';
			store.dispatch('messages/add', message);
		} else {
			message = '問題が発生しました。';
			store.dispatch('messages/add', message);
		}
		return Promise.reject(error);
	}
);


// リクエスト時にトークンの検証を行わない。
const publicApi = axios.create({
	baseURL: process.env.VUE_APP_API_BASE_URL,
	timeout: 30000,
	headers: {
		'Content-Type': 'application/json',
		'X-Requested-With': 'XMLHttpRequest'
	}
});


publicApi.interceptors.request.use(
	config => {
		// リクエスト時にメッセージを初期化
		store.dispatch('messages/clear');
		return config;
	},
	error => Promise.reject(error)
);


publicApi.interceptors.response.use(
	response => response,
	error => {
		const statusCode = error.response ? error.response.status : 500;
		let message;
		if (statusCode === 400) { // バリデーションエラー
			let messages = [].concat.apply([], Object.values(error.response.data));
			for (const message of messages) {
				store.dispatch('messages/add', message);
			}
		} else if (statusCode === 403) { // パーミッションエラー
			message = '許可されていません。';
			store.dispatch('messages/add', message);
		} else {
			message = '問題が発生しました。';
			store.dispatch('messages/add', message);
		}
		return Promise.reject(error);
	}
);


export default api;

export { publicApi };
