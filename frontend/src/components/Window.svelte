<script lang="ts">
	export let noBackground: boolean = false;
</script>

<div class="h-screen overflow-y-auto p-5 flex flex-col items-center">
	<div class="text-fwhite animation-fadein w-full m-x-auto m-y-auto max-w-120">
		{#if noBackground}
			<slot />
		{:else}
			<div
				class="bg-windowBack p-10 rounded-lg shadow-lg flex flex-col items-center justify-center"
			>
				<slot />
			</div>
		{/if}
	</div>
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
