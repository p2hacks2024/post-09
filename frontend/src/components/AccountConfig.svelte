<script lang="ts">
	import { AuthController, type AuthInfo } from '../lib/oauth/spotify';

	export let authInfo: AuthInfo | null = null;
	export let authController: AuthController;
</script>

<p class="text-right text-md absolute top-0 right-0 p-2">
	<span class="text-fwhite">
		{authInfo?.signedIn() ? 'Spotify ID: ' + authInfo?.getName() : ''}
	</span>
	<button
		class="bg-transparent border-b-2 border-spotify text-fwhite"
		on:click={() => {
			if (authInfo?.signedIn()) {
				authController.signOut();
				location.reload();
			} else if (authInfo != null) {
				authController.oauth2SignIn();
			} else {
				return;
			}
		}}
		>{authInfo?.signedIn() ? 'サインアウト' : authInfo != null ? 'Spotifyで認証する' : '確認中...'}
	</button>
</p>

<style>
</style>
