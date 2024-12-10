<script lang="ts">
	import { onMount } from 'svelte';
	import { AuthController, type AuthInfo } from './lib/oauth/spotify';
	import PWABadge from './lib/PWABadge.svelte';
	import Title from './scenes/Title.svelte';
	import Analysis from './scenes/Analysis.svelte';
	import Suggestion from './scenes/Suggestion.svelte';
	import Choice from './scenes/Choice.svelte';

	let auth_info: AuthInfo | null = null;
	let auth_controller: AuthController = new AuthController();

	const defaultScene = 'title';

	let scene = defaultScene;

	onMount(async () => {
		const query = new URLSearchParams(location.search);
		scene = query.get('scene') || defaultScene;

		auth_controller.handleAuthCallback(scene);
		auth_info = await auth_controller.checkAuthorized();
	});
</script>

<main class="main-bg p-6">
	{#if scene === 'analysis'}
		<Analysis {auth_info} {auth_controller} />
	{:else if scene === 'choice'}
		<Choice {auth_info} {auth_controller} />
	{:else if scene === 'suggestion'}
		<Suggestion {auth_info} {auth_controller} />
	{:else}
		<Title {auth_info} {auth_controller} bind:scene />
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
