<script lang="ts">
	import AccountConfig from '../components/AccountConfig.svelte';
	import ChoiceButton from '../components/ChoiceButton.svelte';
	import PressButton from '../components/PressButton.svelte';
	import Typewriter from '../components/Typewriter.svelte';
	import Window from '../components/Window.svelte';
	import { emotionTable } from '../lib/emotionTable';
	import type { AuthInfo, AuthController } from '../lib/oauth/spotify';

	export let authInfo: AuthInfo | null;
	export let authController: AuthController;

	export let scene: string;

	export let prompt: string;
	export let chosenEmotion: string;

	export let alert: string;
</script>

<Window>
	<div class="w-full flex flex-col gap-5">
		<div class="text-lg">
			<Typewriter text="思い出した嫌な出来事について教えてください" />
		</div>
		<div>
			<div>現れた感情</div>

			<div class="flex justify-start w-full gap-4 flex-wrap">
				{#each emotionTable as emotion}
					<ChoiceButton
						category={emotion}
						selected={emotion === chosenEmotion}
						onClick={() => {
							if (chosenEmotion === emotion) {
								chosenEmotion = '';
								return;
							}
							chosenEmotion = emotion;
						}}
					/>
				{/each}
			</div>
		</div>

		<div>
			または、あなた自身の言葉で...
			<input
				type="text"
				class="w-full p-2 rounded-md border-2 border-entryBorder bg-entryBack"
				bind:value={prompt}
				on:input={() => {
					if (prompt) {
						chosenEmotion = '';
					}
				}}
			/>
		</div>

		<div class="text-md text-red-200 text-center">
			{alert}
		</div>

		<PressButton
			onClick={() => {
				console.log(chosenEmotion, prompt);
				if (!chosenEmotion && !prompt) {
					alert = '感情を選択するか、言葉で教えてください';
					return;
				}
				scene = 'playing';
			}}>音楽を開始</PressButton
		>
	</div>
</Window>

<AccountConfig {authInfo} {authController} />
