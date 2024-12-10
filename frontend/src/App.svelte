<script lang="ts">
	import { onMount } from 'svelte';
	import { AuthProvider, type AuthInfo } from './lib/oauth/spotify';
	import PWABadge from './lib/PWABadge.svelte';
	import Account from './components/Account.svelte';

	let auth_info: AuthInfo | null = null;
	let auth_provider: AuthProvider = new AuthProvider();

	onMount(async () => {
		auth_provider.handleAuthCallback();
		auth_info = await auth_provider.checkAuthorized();
	});
</script>

<main>
	<Account {auth_info} {auth_provider} />
</main>

<PWABadge />

<style>
</style>
