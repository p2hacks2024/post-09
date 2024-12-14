<script lang="ts">
	import AccountConfig from '../components/AccountConfig.svelte';
	import Logo from '../components/Logo.svelte';
	import PressButton from '../components/PressButton.svelte';
	import Window from '../components/Window.svelte';
	import type { AuthInfo, AuthController } from '../lib/oauth/spotify';

	export let authInfo: AuthInfo | null;
	export let authController: AuthController;

	export let scene: string;
</script>

<Window>
	<Logo {scene} playingScene={['title']} />
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
			? '記録する'
			: authInfo != null
				? 'Spotifyで認証する'
				: '確認中...'}</PressButton
	>
	{#if authInfo?.signedIn()}
		<div class="m-t-5">
			<PressButton
				type="sub"
				onClick={() => {
					scene = 'analysis';
				}}>{authInfo.getName()}さんの記録を見る</PressButton
			>
		</div>
	{/if}
</Window>

<AccountConfig {authInfo} {authController} />
