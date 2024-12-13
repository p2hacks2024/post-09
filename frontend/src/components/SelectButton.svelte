<script lang="ts">
	export let category: string;
	export let selected: boolean;
	export let onClick: () => void;
	$: bgClass = selected ? 'bg-buttonOrangeHover' : 'bg-buttonBack';
	$: borderClass = selected
		? 'border-buttonOrange'
		: 'border-buttonBorder hover:border-buttonOrange';
</script>

<button class="shared {bgClass} {borderClass}" on:click={onClick}>{category}</button>

<style>
	.shared {
		@apply border-2 text-fwhite px-3 py-2
		rounded-full shadow-lg font-semibold text-xs
		transition-colors duration-200 whitespace-nowrap;
	}
</style>