<script lang="ts">
	import StartButton from '../components/StartButton.svelte';
	import type { AuthInfo, AuthController } from '../lib/oauth/spotify';

	export let auth_info: AuthInfo | null;
	export let auth_controller: AuthController;

	export let scene: string;
</script>

<div class="flex flex-col items-center justify-center h-screen text-fwhite">
	<h1 class="text-4xl font-bold">FlushTune</h1>
	<p class="text-lg text-center">素敵な音楽で<br />嫌な思い出をフラッシュ</p>
	<div class="h-5"></div>
	<StartButton
		{auth_info}
		{auth_controller}
		on_start={() => {
			scene = 'choice';
		}}
	/>
</div>
