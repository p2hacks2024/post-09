<script lang="ts">
	import AccountConfig from '../components/AccountConfig.svelte';
	import ChoiceButton from '../components/ChoiceButton.svelte';
	import type { AuthInfo, AuthController } from '../lib/oauth/spotify';
	import { ToggleSet } from '../lib/toggleSet';

	export let auth_info: AuthInfo | null;
	export let auth_controller: AuthController;

	let emotionSet: ToggleSet = new ToggleSet();
	const emotions = ['怒り', '恐怖', '不安', '悲しみ', '寂しさ'];

	let happeningSet: ToggleSet = new ToggleSet();
	const happenings = ['家族', '友人', '恋人', '仕事', '学校', 'その他'];

	$: console.log(emotionSet);
</script>

<div class="h-screen text-fwhite flex flex-col items-center justify-center">
	<div class="max-w-120 w-full">
		<div class="text-lg">あなたのフラッシュバックについて 教えてください</div>
		<div class="h-5"></div>
		<div>感情</div>

		<div class="flex justify-start w-full gap-4 flex-wrap">
			{#each emotions as emotion}
				<ChoiceButton
					category={emotion}
					selected={emotionSet.has(emotion)}
					onClick={() => {
						emotionSet.toggle(emotion);
						emotionSet = emotionSet;
					}}
				/>
			{/each}
		</div>
		<div class="h-5"></div>
		<div>出来事</div>
		<div class="flex justify-start w-full gap-4 flex-wrap">
			{#each happenings as happening}
				<ChoiceButton
					category={happening}
					selected={happeningSet.has(happening)}
					onClick={() => {
						happeningSet.toggle(happening);
						happeningSet = happeningSet;
					}}
				/>
			{/each}
		</div>
	</div>

	<AccountConfig {auth_info} {auth_controller} />
</div>
