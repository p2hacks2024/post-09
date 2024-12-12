<script lang="ts">
	import { onMount } from 'svelte';
	import { AuthController, type AuthInfo } from './lib/oauth/spotify';
	import PWABadge from './components/PWABadge.svelte';
	import Title from './scenes/Title.svelte';
	import Analysis from './scenes/Analysis.svelte';
	import Playing from './scenes/Playing.svelte';
	import Choice from './scenes/Choice.svelte';
	import Screen from './components/Screen.svelte';
	import Satisfied from './scenes/Satisfied.svelte';

	let authInfo: AuthInfo | null = null;
	let authController: AuthController = new AuthController();

	const defaultScene = import.meta.env.VITE_DEFAULT_SCENE || '';

	let scene = defaultScene;

	onMount(async () => {
		const query = new URLSearchParams(location.search);
		scene = query.get('scene') || defaultScene;

		authController.handleAuthCallback(scene);
		authInfo = await authController.checkAuthorized();
	});
</script>

<Screen {scene}>
	{#if scene === 'analysis'}
		<Analysis {authInfo} {authController} bind:scene />
	{:else if scene === 'choice'}
		<Choice {authInfo} {authController} bind:scene />
	{:else if scene === 'playing'}
		<Playing {authInfo} {authController} bind:scene />
	{:else if scene === 'satisfied'}
		<Satisfied bind:scene />
	{:else}
		<Title {authInfo} {authController} bind:scene />
	{/if}
</Screen>

<PWABadge />

<style>
	:global(body) {
		@apply font-sans text-fprimary;
	}
</style>
