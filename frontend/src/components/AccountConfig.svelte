<script lang="ts">
	import { AuthProvider, type AuthInfo } from '../lib/oauth/spotify';

	export let auth_info: AuthInfo | null = null;
	export let auth_provider: AuthProvider;
</script>

<p class="text-right text-sm absolute top-0 right-0 p-2">
    <span class="text-fsecondary">
        {auth_info?.signedIn() ? 'Spotify ID: ' + auth_info.name : ''}
    </span>
    <button
        class="bg-transparent border-b-2 border-spotify text-fprimary"
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
        >{auth_info?.signedIn() ? 'サインアウト' : auth_info != null ? 'Spotifyで認証する' : '確認中...'}
    </button>
</p>

<style>
</style>
