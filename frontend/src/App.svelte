<script lang="ts">
	import { onMount } from 'svelte';
	import { AuthProvider, type AuthInfo } from './lib/oauth/google';
	import PWABadge from './lib/PWABadge.svelte';

	let auth_info: AuthInfo | null = null;
	let auth_provider: AuthProvider = new AuthProvider();

	onMount(async () => {
		auth_provider.handleAuthCallback();
		auth_info = await auth_provider.checkAuthorized();
	});
</script>

<main>
	<p>
		{auth_info?.signedIn()
			? `Your User ID is: ${auth_info?.userid}`
			: auth_info != null
				? 'You are not signed in'
				: 'Checking...'}
	</p>
	<button
		on:click={() => {
			if (auth_info?.signedIn()) {
				auth_provider.signOut();
				location.reload();
			} else if (auth_info != null) {
				auth_provider.oauth2SignIn();
			} else {
				return;
			}
		}}
		>{auth_info?.signedIn() ? 'Sign Out' : auth_info != null ? 'Sign In' : 'Checking...'}
	</button>
</main>

<PWABadge />

<style>
</style>
