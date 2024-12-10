<script lang="ts">
	import PressButton from '../components/PressButton.svelte';
	import type { AuthInfo, AuthController } from '../lib/oauth/spotify';

	export let auth_info: AuthInfo | null;
	export let auth_controller: AuthController;

	export let scene: string;
</script>

<div class="flex flex-col items-center justify-center h-full text-fwhite">
	<h1 class="text-4xl font-bold">FlushTune</h1>
	<p class="text-lg text-center">素敵な音楽で<br />嫌な思い出をフラッシュ</p>
	<div class="h-5"></div>
	<PressButton
		onClick={() => {
			if (auth_info?.signedIn()) {
				scene = 'choice';
			} else if (auth_info != null) {
				auth_controller.oauth2SignIn();
			} else {
				return;
			}
		}}
		>{auth_info?.signedIn()
			? 'はじめる'
			: auth_info != null
				? 'Spotifyで認証する'
				: '確認中...'}</PressButton
	>
</div>
