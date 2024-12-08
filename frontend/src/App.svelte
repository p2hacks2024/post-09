<script lang="ts">
	import { checkAuthorized, oauth2SignIn, type AuthInfo } from './lib/google/oauth';
	import PWABadge from './lib/PWABadge.svelte';

	let auth_info: AuthInfo | null = null;

	$: auth_info = checkAuthorized();
</script>

<main>
	<button
		on:click={() => {
			oauth2SignIn();
		}}
		disabled={auth_info !== null && auth_info.asUser()}>Authorize</button
	>
</main>

<PWABadge />

<style>
</style>
