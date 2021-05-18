import Vue from 'vue';
import Router from 'vue-router';
import store from './store';

const HomePage = () => import(/* webpackChankName: 'HomePage' */ './views/HomePage');
const SignupPage = () => import(/* webpackChankName: 'SignupPage' */ './views/SignupPage');
const LoginPage = () => import(/* webpackChankName: 'LoginPage' */ './views/LoginPage');
const MyPage = () => import(/* webpackChankName: 'MyPage' */ './views/MyPage');
const MyPosts = () => import(/* webpackChankName: 'MyPosts' */ './components/MyPosts');
const MyFavorites = () => import(/* webpackChankName: 'MyFavorites' */ './components/MyFavorites');
const ViewPostPage = () => import(/* webpackChankName: 'ViewPostPage' */ './views/ViewPostPage');
const ViewUserPage = () => import(/* webpackChankName: 'ViewUserPage' */ './views/ViewUserPage');
const CreatePostPage = () => import(/* webpackChankName: 'CreatePostPage' */ './views/CreatePostPage');
const EditPostPage = () => import(/* webpackChankName: 'EditPostPage' */ './views/EditPostPage');
const EditProfilePage = () => import(/* webpackChankName: 'EditProfilePage' */ './views/EditProfilePage');


Vue.use(Router);

const router = new Router({
	mode: 'history',
	routes: [
		{ path: '/', component: HomePage, name: 'home', props: true },
		{ path: '/post/:id', component: ViewPostPage, props: true, name: 'viewPost' },
		{ path: '/create/post', component: CreatePostPage, meta: { requiredAuth: true } },
		{ path: '/edit/post/:id', component: EditPostPage, name: 'edit', props: true, meta: { requiredAuth: true } },
		{ path: '/signup', component: SignupPage },
		{ path: '/login', component: LoginPage, name: 'login', props: true },
		{ path: '/mypage', component: MyPage, name: 'mypage', meta: { requiredAuth: true }, children: [{ path: 'myposts', component: MyPosts, name: 'myPosts' }, { path: 'favorites', component: MyFavorites, name: 'favoritePosts' }] },
		{ path: '/user/:username', component: ViewUserPage, props: true, name: 'viewUser' },
		{ path: '/edit/profile', component: EditProfilePage, name: 'editProfile', meta: { requiredAuth: true } },
		{ path: '*', redirect: '/' }
	]
});

function goToLoginPage(to, from, next) { // ログインページへ移動させる
	next({
		path: '/login/',
		query: { next: to.fullPath }
	});
}

router.beforeEach((to, from, next) => {
	const isLoggedIn = store.getters['auth/isLoggedIn'];
	const token = localStorage.getItem('access');
	if (to.matched.some(record => record.meta.requiredAuth)) {
		if (isLoggedIn) { // ログインしていれば遷移可能
			next();
		} else {
			if (token) {
				store.dispatch('auth/reload').then(() => {
					next();
				})
					.catch(() => {
						goToLoginPage(to, from, next);
					});
			} else {
				goToLoginPage(to, from, next);
			}
		}
	} else {
		if (token) {
			store.dispatch('auth/reload');
		}
		next();
	}
});

export default router;