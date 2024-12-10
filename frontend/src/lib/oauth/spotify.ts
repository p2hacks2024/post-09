const AUTH_REDIRECT_URI =
	import.meta.env.VITE_MODE === 'RELEASE'
		? 'https://post-09.pages.dev/api/auth/spotify/callback'
		: 'http://localhost:5173/api/auth/spotify/callback';
const AUTH_CLIENT_ID = import.meta.env.VITE_SPOTIFY_API_CLIENT_ID || '';
const AUTH_SCOPES = ['user-read-email'];

export class AuthInfo {
	signed_in: boolean;
	name: string = '';
	userid: string = '';
	constructor(signed_in: boolean, name: string, userid: string) {
		this.signed_in = signed_in;
		this.name = name;
		this.userid = userid;
	}
	signedIn(): boolean {
		return this.signed_in;
	}
}

function generateRandomString() {
	return Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
}

export class AuthProvider {
	item_oauth_params = 'spotify_oauth_params';
	
	constructor() {}

	signOut() {
		localStorage.removeItem(this.item_oauth_params);
	}

	oauth2SignIn() {
		var oauth2Endpoint = 'https://accounts.spotify.com/authorize';
		var params = {
			client_id: AUTH_CLIENT_ID,
			redirect_uri: AUTH_REDIRECT_URI,
			response_type: 'token',
			scope: AUTH_SCOPES.join(' '),
			show_dialog: 'true',
			state: generateRandomString()
		} as Record<string, string>;

		var form = document.createElement('form');
		form.setAttribute('method', 'GET');
		form.setAttribute('action', oauth2Endpoint);

		for (var p in params) {
			var input = document.createElement('input');
			input.setAttribute('type', 'hidden');
			input.setAttribute('name', p);
			input.setAttribute('value', params[p]);
			form.appendChild(input);
		}
		document.body.appendChild(form);
		form.submit();
	}

	handleAuthCallback() {
		const fragmentString = window.location.hash.substring(1);
		const params = new URLSearchParams(fragmentString);
		const accessToken = params.get('access_token');
		if (accessToken) {
			localStorage.setItem(this.item_oauth_params, JSON.stringify({ access_token: accessToken }));
			window.history.replaceState({}, document.title, window.location.pathname);
		}
	}

	async checkAuthorized(): Promise<AuthInfo> {
		var params = JSON.parse(localStorage.getItem(this.item_oauth_params) || '{}');
		if (params && params['access_token']) {
			let response = new Promise((resolve, reject) => {
				var xhr = new XMLHttpRequest();
				xhr.open(
					'GET',
					'https://api.spotify.com/v1/me?' + 'access_token=' + params['access_token']
				);
				let signinFunc = this.oauth2SignIn;
				xhr.onreadystatechange = function (_) {
					if (xhr.readyState === 4 && xhr.status === 200) {
						resolve(JSON.parse(xhr.responseText));
					} else if (xhr.readyState === 4 && xhr.status === 401) {
						signinFunc();
					}
				};
				xhr.send(null);
			});
			return response
				.then((resp) => {
					const data = resp as any;
					return new AuthInfo(true, data.display_name, data.id);
				})
				.catch((_) => {
					return new AuthInfo(false, '', '');
				});
		}
		return new AuthInfo(false, '', '');
	}
}
