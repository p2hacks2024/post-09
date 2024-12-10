<script lang="ts">
	import { AuthController, type AuthInfo } from '../lib/oauth/spotify';

	export let auth_info: AuthInfo | null = null;
	export let auth_controller: AuthController;
</script>

<p class="text-right text-sm absolute top-0 right-0 p-2">
	<span class="text-fwhite">
		{auth_info?.signedIn() ? 'Spotify ID: ' + auth_info.name : ''}
	</span>
	<button
		class="bg-transparent border-b-2 border-spotify text-fwhite"
		on:click={() => {
			if (auth_info?.signedIn()) {
				auth_controller.signOut();
				location.reload();
			} else if (auth_info != null) {
				auth_controller.oauth2SignIn();
			} else {
				return;
			}
		}}
		>{auth_info?.signedIn()
			? 'サインアウト'
			: auth_info != null
				? 'Spotifyで認証する'
				: '確認中...'}
	</button>
</p>

<style>
</style>
