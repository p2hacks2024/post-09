<script lang="ts">
	import { onMount } from 'svelte';

	export let createElementFunc: (canvas: HTMLCanvasElement) => any;
	export let boxId: string;
	export let analysis: any;
	export let hasBorder: boolean = false;
	export let heightClass: string = 'h-50';
	let canvas: HTMLCanvasElement;

	function update() {
		canvas.innerHTML = '';
		const domElement = createElementFunc(canvas);
		canvas.appendChild(domElement);
	}

	onMount(() => {
		canvas = document.getElementById('canvas' + boxId) as HTMLCanvasElement;
		if (hasBorder) {
			canvas.style.border = '1px solid #000';
		}
		canvas.classList.add(heightClass);
	});

	$: if (analysis) {
		update();
	}
</script>

<div class="w-full overflow-hidden bg-transparent" id={`canvas${boxId}`}></div>
