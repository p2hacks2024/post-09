<script lang="ts">
	export let onClick: () => void;
</script>

<button
	class="bg-buttonBack text-fwhite p-x-5 p-y-3 rounded-full shadow-md font-semibold hover:bg-buttonBackHover transition-colors duration-200"
	on:click={onClick}
	><slot></slot>
</button>
