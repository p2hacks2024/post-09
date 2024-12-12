<script lang="ts">
	export let onClick: () => void;
	export let type: 'normal' | 'sub' = 'normal';
</script>

{#if type === 'normal'}
	<button class="shared normal" on:click={onClick}><slot></slot> </button>
{:else}
	<button class="shared sub" on:click={onClick}><slot></slot> </button>
{/if}

<style>
	.shared {
		@apply bg-buttonBack text-fwhite rounded-full shadow-md font-semibold border-2 transition-colors duration-200;
	}

	.normal {
		@apply border-pressButtonBorder hover:border-pressButtonBorderHover text-lg p-x-5 p-y-3;
	}

	.sub {
		@apply border-pressSubButtonBorder hover:border-pressSubButtonBorderHover text-sm p-x-3 p-y-2;
	}
</style>
