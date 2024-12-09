const AUTH_REDIRECT_URI =
	import.meta.env.VITE_AUTH_REDIRECT_URI === 'RELEASE'
		? 'https://post-09.pages.dev/api/auth/google-oauth/callback'
		: 'http://localhost:5173/api/auth/google-oauth/callback';

const AUTH_CLIENT_ID = import.meta.env.VITE_GOOGLE_API_CLIENT_ID || '';

const AUTH_SCOPE = 'https://www.googleapis.com/auth/drive.readonly';

export class AuthInfo {
	signed_in: boolean;
	userid: string = '';

	constructor(signed_in: boolean, userid: string) {
		this.signed_in = signed_in;
		this.userid = userid;
	}

	signedIn(): boolean {
		return this.signed_in;
	}
}

export class AuthProvider {
	item_oauth_params = 'google_oauth_params';

	constructor() {}

	signOut() {
		localStorage.removeItem(this.item_oauth_params);
	}

	oauth2SignIn() {
		var oauth2Endpoint = 'https://accounts.google.com/o/oauth2/v2/auth';
		var form = document.createElement('form');
		form.setAttribute('method', 'GET');
		form.setAttribute('action', oauth2Endpoint);

		var params = {
			client_id: AUTH_CLIENT_ID,
			redirect_uri: AUTH_REDIRECT_URI,
			response_type: 'token',
			scope: AUTH_SCOPE,
			include_granted_scopes: 'true',
			state: 'pass-through value'
		} as Record<string, string>;

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
		const scope = params.get('scope');

		if (accessToken) {
			localStorage.setItem(
				this.item_oauth_params,
				JSON.stringify({ access_token: accessToken, scope: scope })
			);
			window.history.replaceState({}, document.title, window.location.pathname);
		}
	}

	async checkAuthorized(): Promise<AuthInfo> {
		var params = JSON.parse(localStorage.getItem(this.item_oauth_params) || '{}');
		if (params && params['access_token']) {
			let response = new Promise((resolve, reject) => {
				if (params['scope'].includes(AUTH_SCOPE)) {
					var xhr = new XMLHttpRequest();
					xhr.open(
						'GET',
						'https://www.googleapis.com/drive/v3/about?fields=user&' +
							'access_token=' +
							params['access_token']
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
				} else {
					reject('User did not authorize read-only Drive activity permission.');
				}
			});

			return response
				.then((data) => {
					return new AuthInfo(true, (data as any).user.emailAddress);
				})
				.catch((_) => {
					return new AuthInfo(false, '');
				});
		}
		return new AuthInfo(false, '');
	}
}
