const AUTH_REDIRECT_URI =
	import.meta.env.VITE_AUTH_REDIRECT_URI === 'RELEASE'
		? 'https://post-09.pages.dev/api/auth/google-oauth/callback'
		: 'http://localhost:5173/api/auth/google-oauth/callback';

const AUTH_CLIENT_ID = import.meta.env.VITE_GOOGLE_API_CLIENT_ID || '';

const AUTH_SCOPE = 'https://www.googleapis.com/auth/drive.readonly';

export function oauth2SignIn() {
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

export class AuthInfo {
	as_user: boolean;

	constructor(as_user: boolean) {
		this.as_user = as_user;
	}

	asUser(): boolean {
		return this.as_user;
	}
}

export function checkAuthorized(): AuthInfo {
	var params = JSON.parse(localStorage.getItem('oauth2-params') || '{}');
	if (params && params['access_token']) {
		if (params['scope'].includes(AUTH_SCOPE)) {
			var xhr = new XMLHttpRequest();
			xhr.open(
				'GET',
				'https://www.googleapis.com/drive/v3/about?fields=user&' +
					'access_token=' +
					params['access_token']
			);
			xhr.onreadystatechange = function (e) {
				if (xhr.readyState === 4 && xhr.status === 200) {
					console.log(xhr.response);
				} else if (xhr.readyState === 4 && xhr.status === 401) {
					oauth2SignIn();
				}
			};
			xhr.send(null);
		} else {
			console.log('User did not authorize read-only Drive activity permission.');
		}

		if (params['scope'].includes(AUTH_SCOPE)) {
			return new AuthInfo(true);
		} else {
			return new AuthInfo(false);
		}
	}
	return new AuthInfo(false);
}
