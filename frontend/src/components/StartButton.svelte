<script lang="ts">
	import { AuthController, type AuthInfo } from '../lib/oauth/spotify';

	export let auth_info: AuthInfo | null = null;
	export let auth_controller: AuthController;

	export let on_start: () => void;
</script>

<button
	class="bg-spotify text-fwhite p-x-5 p-y-3 rounded-full shadow-md font-semibold hover:bg-spotifydark transition-colors duration-80"
	on:click={() => {
		if (auth_info?.signedIn()) {
			on_start();
		} else if (auth_info != null) {
			auth_controller.oauth2SignIn();
		} else {
			return;
		}
	}}
	>{auth_info?.signedIn() ? 'はじめる' : auth_info != null ? 'Spotifyで認証する' : '確認中...'}
</button>
