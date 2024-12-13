<script lang="ts">
	import { onMount } from 'svelte';

	export let text: string;
	export let speed: number = 60;
	export let interval: number = 1000;

	let index = 0;
	let display = '';

	onMount(() => {
		const timer = setInterval(() => {
			if (index < text.length) {
				display += text[index];
				index++;
			} else {
				clearInterval(timer);
			}
		}, speed);
	});
</script>

<p>{display}</p>
