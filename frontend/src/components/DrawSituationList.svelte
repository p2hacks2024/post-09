<script lang="ts">
	import { onMount } from 'svelte';

    export let createSituationList: () => string[];
    export let chosenEmotion: string;
	let situations: string[] = [];

    onMount(() => {
        chosenEmotion = '';
	});

    $: if(chosenEmotion){
        situations = createSituationList();
    }
</script>

<div class=situation-list>
    {#each situations as situation}
        <div class="situ">
            <p class="text-lg">{situation}</p>
        </div>
    {/each}
</div>

<style>
    
    .situation-list {
        @apply flex justify-start w-full gap-1 flex-wrap; /* カード間の間隔 */
        margin: 10px 0;
    }

    .situ {
        @apply bg-white bg-opacity-10 rounded-md shadow-md; /* カードのスタイル */
        padding: 10px; /* パディングを設定して文字を完全に覆う */
        width: calc(100%); /* 横幅を一定間隔に設定 */
        margin: 0 auto; /* カードを中央に配置 */
    }

    .text-lg {
        @apply text-sm; /* テキストのスタイル */
        margin: 0;
    }
</style>
