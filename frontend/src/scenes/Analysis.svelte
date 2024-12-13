<script lang="ts">
	import AccountConfig from '../components/AccountConfig.svelte';
	import type { AuthInfo, AuthController } from '../lib/oauth/spotify';
	import { emotionTable } from '../lib/emotionTable';
	import Window from '../components/Window.svelte';
	import PressButton from '../components/PressButton.svelte';
	import SelectButton from '../components/SelectButton.svelte';
	import DrawSituationList from '../components/DrawSituationList.svelte';
	import DrawBarGraph from '../components/DrawBarGraph.svelte';

	export let authInfo: AuthInfo | null;
	export let authController: AuthController;
	export let scene: string;

	let analysis: any = undefined;

	const emotions = Object.values(emotionTable);
	const emotions_selection = emotions;
	let chosenEmotion = '';

	$: if (authInfo?.signedIn()) {
		//const userId = authInfo?.getUserId();
		const userId = '0001'; // TODO: remove this line!

		fetch(`${import.meta.env.VITE_API_SERVER_ORIGIN}/analysis/${userId}`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			}
		})
			.then((res) => {
				return res.json();
			})
			.then((json) => {
				analysis = json;
			})
			.catch((e) => {
				console.error(e);
			});
	}
	
	function createSituationList(){
		let emotion_to_recent_situation = analysis["per_total"]["emotion_to_recent_situation"];
		let situations = [];
		situations = chosenEmotion ? emotion_to_recent_situation[chosenEmotion] : [];
		console.log(situations);
		return situations;
	}

	function getEmotionFreq(){
		const emotionFreq: {key: string, value: number}[] = [];
		
		emotions.forEach((emotion) => {
			let freq :number = analysis["per_total"]["emotion_freq"][emotion];
			if(freq == undefined){
				freq = 0;
			}
			console.log("freq", freq, emotion);
			emotionFreq.push({key: emotion, value: freq});
		});
		console.log("emotionFreq", emotionFreq);
		//console.log("mainn", analysis["per_total"]["emotion_freq"]);
		//const emotionFreq: {key: string, value: number}[] = analysis["per_total"]["emotion_freq"];
		return emotionFreq;
	}
</script>

<Window>
	<h1 class="text-4xl font-bold">記録</h1>
	<p class="text-lg mt-4">感情の量</p>
	<DrawBarGraph getEmotionFreq={getEmotionFreq} {analysis} />
	
	<p class="text-lg mt-4">感情の素</p>

	<div class="flex justify-start w-full gap-1 flex-wrap">
		{#each emotions_selection as emotion}
			<SelectButton
				category={emotion}
				selected={emotion === chosenEmotion}
				onClick={() => {
					chosenEmotion = emotion;
				}}
			/>
		{/each}
	</div>

	<DrawSituationList createSituationList={createSituationList} {chosenEmotion} />	
	
	
	<div class="m-x-auto m-y-5">
		<PressButton
			type="sub"
			onClick={() => {
				scene = 'title';
			}}>タイトルに戻る</PressButton
		>
	</div>
</Window>

<AccountConfig {authInfo} {authController} />
