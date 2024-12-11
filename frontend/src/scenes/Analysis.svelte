<script lang="ts">
	import AccountConfig from '../components/AccountConfig.svelte';
	import type { AuthInfo, AuthController } from '../lib/oauth/spotify';

	export let authInfo: AuthInfo | null;
	export let authController: AuthController;

	let analysis: any;

	$: if (authInfo?.signedIn()) {
		analysis = new Promise(async (resolve) => {
			const asis = await fetch(
				`${import.meta.env.VITE_API_SERVER_ORIGIN}/analysis/${authInfo?.getUserId()}`,
				{
					method: 'GET',
					headers: {
						'Content-Type': 'application/json'
					}
				}
			).then((res) => res.json());
			resolve(asis);
		})
			.then((asis) => {
				console.log(analysis);
				return asis;
			})
			.catch((e) => {
				console.error(e);
			});
	}
</script>

<div class="h-full text-fwhite">
	<h1 class="text-4xl font-bold">記録</h1>
	<p class="text-lg">記録をフラッシュ</p>
	<div class="h-5"></div>
</div>

<AccountConfig {authInfo} {authController} />
