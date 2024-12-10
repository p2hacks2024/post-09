<script lang="ts">
	import AccountConfig from '../components/AccountConfig.svelte';
	import type { AuthInfo, AuthController } from '../lib/oauth/spotify';

	export let auth_info: AuthInfo | null;
	export let auth_controller: AuthController;
</script>

<div class="h-screen text-fwhite">
	<h1 class="text-4xl font-bold">選択</h1>
	<p class="text-lg">選択をフラッシュ</p>
	<div class="h-5"></div>
	<AccountConfig {auth_info} {auth_controller} />
</div>
