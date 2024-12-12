<script lang="ts">
	import { onMount } from 'svelte';

	export let track: string | undefined = undefined;
	let iframeElement: HTMLIFrameElement;

	$: if (track && iframeElement) {
		iframeElement.src = `https://open.spotify.com/embed/track/${track}?utm_source=generator&theme=0`;
		let rootPlayer = document.getElementById('root-player');
		if (rootPlayer) {
			rootPlayer.innerHTML = '';
			rootPlayer.appendChild(iframeElement);
		}
	}

	onMount(() => {
		iframeElement = document.createElement('iframe');
		iframeElement.style.borderRadius = '12px';
		iframeElement.width = '100%';
		iframeElement.height = '152';
		iframeElement.allow =
			'autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture';
		iframeElement.loading = 'lazy';
	});
</script>

<div id="root-player"></div>
