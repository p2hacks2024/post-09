<script lang="ts">
	import { onMount } from 'svelte';

	export let createElementFunc: (canvas: HTMLCanvasElement) => any;
	export let boxId: string;
	export let hasBorder: boolean = false;
	export let heightClass: string = 'h-50';

	onMount(() => {
		const canvas = document.getElementById('canvas' + boxId) as HTMLCanvasElement;
		if (!canvas) {
			return;
		}

		if (hasBorder) {
			canvas.style.border = '1px solid #000';
		}

		canvas.classList.add(heightClass);

		const domElement = createElementFunc(canvas);
		canvas.appendChild(domElement);
	});
</script>

<div class="w-full overflow-hidden bg-transparent" id={`canvas${boxId}`}></div>
