<script lang="ts">
	export let category: string;
	export let selected: boolean;
	export let onClick: () => void;
	$: bgClass = selected ? 'bg-buttonOrange hover:bg-buttonOrangeHover' : 'bg-buttonBack';
	$: borderClass = selected
		? 'border-buttonOrange'
		: 'border-buttonBorder hover:border-buttonOrange';
</script>

<button class="shared {bgClass} {borderClass}" on:click={onClick}>{category}</button>

<style>
	.shared {
		@apply border-2 text-fwhite p-x-5 p-y-3
		rounded-md shadow-lg font-semibold
		transition-colors duration-200 whitespace-nowrap;
	}
</style>
