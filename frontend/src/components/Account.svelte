<script lang="ts">
	import { AuthProvider, type AuthInfo } from '../lib/oauth/spotify';

	export let auth_info: AuthInfo | null = null;
	export let auth_provider: AuthProvider;
</script>

<p>
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
</p>

<style>
    button {
        font-size: 1em;
    }
</style>
