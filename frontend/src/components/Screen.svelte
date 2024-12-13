<script lang="ts">
	import { onMount } from 'svelte';

	export let scene: string;
	let cover0: HTMLElement | undefined = undefined;

	onMount(() => {
		cover0 = document.getElementById('cover0');
	});

	$: if (scene === 'analysis' || scene === 'satisfied') {
		if (cover0) {
			cover0.style.opacity = '1';
		}
	} else {
		if (cover0) {
			cover0.style.opacity = '0';
		}
	}
</script>

<main class="shared main-bg">
	<div id="cover1" class="shared cover mainwave-bg animation-wave"></div>
	<div id="cover0" class="shared cover satisfied-bg"></div>
	<slot />
</main>

<style>
	.shared {
		@apply h-screen w-screen;
	}

	.cover {
		@apply transition-opacity duration-3000 absolute top-0 left-0;
	}

	.main-bg {
		background-image: linear-gradient(-15deg, #7f2c85 0%, #4f307a 40% 70%, #193c9c 100%);
	}

	.mainwave-bg {
		background-image: linear-gradient(-15deg, #3f2c85 0%, #3b4788 30% 60%, #4a218b 100%);
	}

	.satisfied-bg {
		background-image: linear-gradient(-15deg, rgb(89, 122, 165) 0%, #3b6d8f 40% 60%, #4a8f77 100%);
	}

	.animation-wave {
		animation: wave 20s infinite;
		animation-timing-function: ease-in-out;
	}

	@keyframes wave {
		0% {
			opacity: 0;
		}
		50% {
			opacity: 1;
		}

		100% {
			opacity: 0;
		}
	}
</style>
