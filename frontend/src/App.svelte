<script lang="ts">
	import { onMount } from 'svelte';
	import { AuthController, type AuthInfo } from './lib/oauth/spotify';
	import PWABadge from './components/PWABadge.svelte';
	import Title from './scenes/Title.svelte';
	import Analysis from './scenes/Analysis.svelte';
	import Playing from './scenes/Playing.svelte';
	import Choice from './scenes/Choice.svelte';

	let authInfo: AuthInfo | null = null;
	let authController: AuthController = new AuthController();

	const defaultScene = 'playing';

	let scene = defaultScene;

	onMount(async () => {
		const query = new URLSearchParams(location.search);
		scene = query.get('scene') || defaultScene;

		authController.handleAuthCallback(scene);
		authInfo = await authController.checkAuthorized();
	});
</script>

<main class="main-bg p-6 h-screen overflow-hidden">
	{#if scene === 'analysis'}
		<Analysis {authInfo} {authController} />
	{:else if scene === 'choice'}
		<Choice {authInfo} {authController} bind:scene />
	{:else if scene === 'playing'}
		<Playing {authInfo} {authController} />
	{:else}
		<Title {authInfo} {authController} bind:scene />
	{/if}
</main>

<PWABadge />

<style>
	:global(body) {
		@apply font-sans text-fprimary;
	}

	.main-bg {
		background-image: linear-gradient(-15deg, #7f2c85 0%, #4f307a 40% 70%, #193c9c 100%);
	}
</style>
