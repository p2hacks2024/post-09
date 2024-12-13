<script lang="ts">
	import { onMount } from "svelte";

    export let getEmotionFreq: () => {key: string, value: number}[];
    export let analysis: any;
	let emotion_freq: {key: string, value: number}[] = [];
    //let emotions :string[]= [];
    //let freq :number[] = [];
    let maxValue = 1;
    let keys: string[] = [];
    let values: number[] = [];

    $: if(analysis){
        emotion_freq = getEmotionFreq();
        //emotions = Object.keys(emotion_freq);
        //freq = Object.values(emotion_freq);
        
        console.log("maxValue", maxValue);

        keys = emotion_freq.map(item => item.key);
        values = emotion_freq.map(item => item.value);
        console.log("values", values);
        console.log("emotions", keys);
        maxValue = Math.max(...values);
    }
</script>

<div class="flex flex-col gap-4 p-4 w-full">
    {#each values as value}
      <div class="box rounded h-[10px]" style="width: {value/maxValue * 100}%"></div>
    {/each}
</div>

<style>
    .box:empty {
        @apply bg-blue-300;
    }
</style>