<script lang="ts">
	import { onMount } from "svelte";

    export let getEmotionFreq: () => {key: string, value: number}[];
    export let analysis: any;
	let emotion_freq: {key: string, value: number}[] = [];
    //let emotions :string[]= [];
    //let freq :number[] = [];
    let maxValue = 1;
    let emotions: string[] = [];
    let freqs: number[] = [];

    $: if(analysis){
        emotion_freq = getEmotionFreq();
        
        console.log("maxValue", maxValue);

        emotions = emotion_freq.map(item => item.key);
        freqs = emotion_freq.map(item => item.value);
        console.log("values", freqs);
        console.log("emotions", emotions);
        maxValue = Math.max(...freqs) > 0 ? Math.max(...freqs) : 1;
    }
</script>

<div class="flex flex-col gap-1 p-1 w-full">
    {#each freqs as freq, i}
        <div class="flex justify-between">
            <p>{emotions[i]}</p>
            <p>{freq}</p>
        </div>
        <div class="relative h-[10px] w-full">
            <div class="box2 absolute inset-0 rounded h-full bg-gray-200"></div>
            <div class="box absolute inset-0 rounded h-full bg-blue-500" style="width: {freq / maxValue * 100}%"></div>
        </div>
    {/each}
</div>

<style>
    .box:empty {
        @apply bg-blue-600;
    }
    .box2:empty {
        @apply bg-gray-600;
    }
</style>