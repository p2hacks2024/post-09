<script lang="ts">
	import AccountConfig from '../components/AccountConfig.svelte';
	import Player from '../components/Player.svelte';
	import PlaylistButton from '../components/PlaylistButton.svelte';
	import PressButton from '../components/PressButton.svelte';
	import Window from '../components/Window.svelte';
	import type { AuthInfo, AuthController } from '../lib/oauth/spotify';

	export let authInfo: AuthInfo | null;
	export let authController: AuthController;
	export let scene: string;

	type Track = {
		id: string;
		key: number;
		name: string;
		artist: string;
		album: string;
	};

	let tracks: Track[] = [];

	$: if (authInfo?.signedIn()) {
		new Promise((resolve) => {
			setTimeout(() => {
				const fakeTracks = [
					'3AoEQRuFf8zVXWqSLo2UOi',
					'4gxEY3Mh5FZZDAJAKPNrCS',
					'74X2u8JMVooG2QbjRxXwR8',
					'21ZvC8aUTJIe5IBT34sLbG',
					'2O4Bb2WCkjlTPO827OnBMI'
				];
				resolve(fakeTracks);
			}, 1000);
		})
			.then((fakeTracks) => {
				const data = (fakeTracks as string[]).map((track, i) => {
					return fetch(`https://api.spotify.com/v1/tracks/${track}`, {
						headers: {
							Authorization: `Bearer ${authInfo?.getAccessToken()}`
						}
					})
						.then((res) => {
							return res.json();
						})
						.then((json) => {
							return {
								id: json.id,
								key: i,
								name: json.name,
								artist: json.artists.map((artist: any) => artist.name).join(', '),
								album: json.album.name
							};
						});
				});

				Promise.all(data).then((ts) => {
					tracks = ts;
				});
			})
			.catch((e) => {
				console.error(e);
			});
	}

	$: chosenTrack = tracks ? tracks[0] : undefined;
</script>

<Window>
	{#if chosenTrack}
		<div class="w-full flex flex-col gap-6">
			<Player track={chosenTrack ? chosenTrack.id : undefined} />
			<div class="h-60 overflow-y-auto flex flex-col">
				{#each tracks as track}
					<PlaylistButton
						key={track.key}
						name={track.name}
						artist={track.artist}
						album={track.album}
						selected={track === chosenTrack}
						onClick={() => {
							chosenTrack = track;
						}}>{track}</PlaylistButton
					>
				{/each}
			</div>
			<PressButton
				type="sub"
				onClick={() => {
					scene = 'satisfied';
				}}>落ち着けました</PressButton
			>
		</div>
	{:else}
		<div class="text-4xl m-auto text-center bg-transparent animate-spin">
			<div class="i-tabler-loader-2"></div>
		</div>
	{/if}
</Window>

<AccountConfig {authInfo} {authController} />
