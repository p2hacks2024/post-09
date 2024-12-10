<script lang="ts">
	import { onMount } from 'svelte';
	import { AuthProvider, type AuthInfo } from './lib/oauth/spotify';
	import PWABadge from './lib/PWABadge.svelte';
	import Title from './scenes/Title.svelte';

	let auth_info: AuthInfo | null = null;
	let auth_provider: AuthProvider = new AuthProvider();

	onMount(async () => {
		auth_provider.handleAuthCallback();
		auth_info = await auth_provider.checkAuthorized();
	});
</script>

<main class="main-bg">
	<Title {auth_info} {auth_provider} />
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
