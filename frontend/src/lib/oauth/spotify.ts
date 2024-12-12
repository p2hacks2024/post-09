const AUTH_SCOPES = ['user-read-email'];

export class AuthInfo {
	private isSignedIn: boolean;
	private name: string = '';
	private userid: string = '';
	private accessToken: string = '';
	constructor(isSignedIn: boolean, name: string, userid: string, accessToken: string) {
		this.isSignedIn = isSignedIn;
		this.name = name;
		this.userid = userid;
		this.accessToken = accessToken;
	}
	signedIn(): boolean {
		return this.isSignedIn;
	}

	getName(): string {
		return this.name;
	}

	getUserId(): string {
		return this.userid;
	}

	getAccessToken(): string {
		return this.accessToken;
	}
}

function generateRandomString() {
	return Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
}

export class AuthController {
	item_oauth_params = 'spotify_oauth_params';

	constructor() {}

	signOut() {
		localStorage.removeItem(this.item_oauth_params);
	}

	oauth2SignIn() {
		const oauth2Endpoint = 'https://accounts.spotify.com/authorize';
		const redirect_uri = window.location.origin + '/api/auth/spotify/callback';

		const params = {
			client_id: import.meta.env.VITE_SPOTIFY_API_CLIENT_ID || '',
			redirect_uri: redirect_uri,
			response_type: 'token',
			scope: AUTH_SCOPES.join(' '),
			show_dialog: 'true',
			state: generateRandomString()
		} as Record<string, string>;

		const form = document.createElement('form');
		form.setAttribute('method', 'GET');
		form.setAttribute('action', oauth2Endpoint);

		for (const p in params) {
			const input = document.createElement('input');
			input.setAttribute('type', 'hidden');
			input.setAttribute('name', p);
			input.setAttribute('value', params[p]);
			form.appendChild(input);
		}
		document.body.appendChild(form);
		form.submit();
	}

	handleAuthCallback(scene: string) {
		const fragmentString = window.location.hash.substring(1);
		const params = new URLSearchParams(fragmentString);
		const accessToken = params.get('access_token');
		if (accessToken) {
			localStorage.setItem(this.item_oauth_params, JSON.stringify({ access_token: accessToken }));
			window.history.replaceState({}, document.title, window.location.origin + '?scene=' + scene);
		}
	}

	accessToken(): string {
		const params = JSON.parse(localStorage.getItem(this.item_oauth_params) || '{}');
		return params['access_token'] || '';
	}

	async checkAuthorized(): Promise<AuthInfo> {
		const accessToken = this.accessToken();
		if (accessToken) {
			return fetch('https://api.spotify.com/v1/me' + '?access_token=' + accessToken)
				.then((response) => response.json())
				.then((data) => {
					return new AuthInfo(true, data.display_name, data.id, accessToken);
				})
				.catch((_) => {
					return new AuthInfo(false, '', '', '');
				});
		}
		return new AuthInfo(false, '', '', '');
	}
}
