<script lang="ts">
	import { onMount } from 'svelte';

	export let scene: string;

	onMount(() => {
		setTimeout(() => {
			scene = 'analysis';
		}, 2000);
	});
</script>
