<script lang="ts">
	import AccountConfig from '../components/AccountConfig.svelte';
	import Player from '../components/Player.svelte';
	import type { AuthInfo, AuthController } from '../lib/oauth/spotify';

	export let authInfo: AuthInfo | null;
	export let authController: AuthController;

	const tracks = [
		'3AoEQRuFf8zVXWqSLo2UOi',
		'4gxEY3Mh5FZZDAJAKPNrCS',
		'74X2u8JMVooG2QbjRxXwR8',
		'21ZvC8aUTJIe5IBT34sLbG',
		'2O4Bb2WCkjlTPO827OnBMI'
	];
</script>

<div class="h-full text-fwhite">
	<h1 class="text-4xl font-bold">曲</h1>
	<p class="text-lg">曲をフラッシュ</p>
	<div class="h-5"></div>
	<Player track="3AoEQRuFf8zVXWqSLo2UOi" />
	<AccountConfig {authInfo} {authController} />
</div>
