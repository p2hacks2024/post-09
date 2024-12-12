<script lang="ts">
	import PressButton from '../components/PressButton.svelte';
	import Window from '../components/Window.svelte';
	import type { AuthInfo, AuthController } from '../lib/oauth/spotify';

	export let authInfo: AuthInfo | null;
	export let authController: AuthController;

	export let scene: string;
</script>

<div class="flex flex-col items-center justify-center h-full text-fwhite">
	<Window>
		<h1 class="text-4xl font-bold">FlushTune</h1>
		<p class="text-lg text-center">素敵な音楽で<br />嫌な思い出をフラッシュ</p>
		<div class="h-5"></div>
		<PressButton
			onClick={() => {
				if (authInfo?.signedIn()) {
					scene = 'choice';
				} else if (authInfo != null) {
					authController.oauth2SignIn();
				} else {
					return;
				}
			}}
			>{authInfo?.signedIn()
				? 'はじめる'
				: authInfo != null
					? 'Spotifyで認証する'
					: '確認中...'}</PressButton
		>
	</Window>
</div>
