<script lang="ts">
	export let key: number;
	export let name: string;
	export let artist: string;
	export let album: string;
	export let selected: boolean;
	export let onClick: () => void;
	$: bgClass = selected ? 'bg-buttonOrangeHover' : 'bg-buttonBack hover:bg-black';
	$: borderClass = selected
		? 'border-buttonOrange'
		: 'border-buttonBorder hover:border-buttonOrange';
</script>

<button class="shared {bgClass} {borderClass}" on:click={onClick}>
	<div class="flex gap-5 items-center">
		<div class="font-bold w-5">{key + 1}</div>
		<div class="text-left">
			<div class="font-bold text-lg">{name}</div>
			<div class="text-sm">{artist}, {album}</div>
		</div>
	</div>
</button>

<style>
	.shared {
		@apply border-l-4 border-b-1 text-fwhite p-x-5 p-y-3
		shadow-lg
		transition-colors duration-200 whitespace-nowrap;
	}
</style>
