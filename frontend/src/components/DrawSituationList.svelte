<script lang="ts">
	import { onMount } from 'svelte';

    export let createSituationList: () => string[];
    export let chosenEmotion: string;
	let outputText: string[] = [];

    onMount(() => {
		outputText = ["ここに状況が表示されます"];
	});

    $: if(chosenEmotion){
        outputText = createSituationList();
    }
</script>

{#each outputText as text}
        <p class="text-lg">{text}</p>
{/each}
