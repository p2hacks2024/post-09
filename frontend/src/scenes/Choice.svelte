<script lang="ts">
	import AccountConfig from '../components/AccountConfig.svelte';
	import ChoiceButton from '../components/ChoiceButton.svelte';
	import PressButton from '../components/PressButton.svelte';
	import Typewriter from '../components/Typewriter.svelte';
	import Window from '../components/Window.svelte';
	import type { AuthInfo, AuthController } from '../lib/oauth/spotify';

	export let authInfo: AuthInfo | null;
	export let authController: AuthController;

	export let scene: string;

	let message: string = '';

	let chosenEmotion = '';
	const emotions = ['怒り', '恐怖', '不安', '悲しみ', '寂しさ', '嫉妬心'];
</script>

<Window>
	<div class="w-full flex flex-col gap-5">
		<div class="text-lg">
			<Typewriter text="あなたが思い出した嫌な出来事について教えてください" />
		</div>
		<div>
			<div>現れた感情</div>

			<div class="flex justify-start w-full gap-4 flex-wrap">
				{#each emotions as emotion}
					<ChoiceButton
						category={emotion}
						selected={emotion === chosenEmotion}
						onClick={() => {
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
				bind:value={message}
			/>
		</div>

		<PressButton
			onClick={() => {
				scene = 'playing';
			}}>音楽を開始</PressButton
		>
	</div>
</Window>

<AccountConfig {authInfo} {authController} />
