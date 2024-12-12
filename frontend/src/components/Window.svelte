<script lang="ts">
	export let noBackground: boolean = false;
</script>

<div class="flex flex-col justify-center h-full text-fwhite animation-fadein">
	{#if noBackground}
		<slot />
	{:else}
		<div class="bg-windowBack p-10 rounded-lg shadow-lg flex flex-col items-center justify-center">
			<slot />
		</div>
	{/if}
</div>

<style>
	.animation-fadein {
		animation: fadeIn 0.2s ease-out forwards;
	}

	@keyframes fadeIn {
		from {
			opacity: 0;
			transform: translateY(-1%);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}
</style>
