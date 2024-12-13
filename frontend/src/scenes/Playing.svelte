<script lang="ts">
	import { onMount } from 'svelte';
	import AccountConfig from '../components/AccountConfig.svelte';
	import Player from '../components/Player.svelte';
	import PlaylistButton from '../components/PlaylistButton.svelte';
	import PressButton from '../components/PressButton.svelte';
	import Typewriter from '../components/Typewriter.svelte';
	import Window from '../components/Window.svelte';
	import type { AuthInfo, AuthController } from '../lib/oauth/spotify';

	export let authInfo: AuthInfo | null;
	export let authController: AuthController;
	export let scene: string;

	export let chosenEmotion: string;
	export let prompt: string;
	export let alert: string;

	type Track = {
		id: string;
		key: number;
		name: string;
		artist: string;
		album: string;
	};

	let tracks: Track[] = [];
	let comment: string = '';

	function rejected(e: any) {
		console.error(e);
		alert = 'エラーが発生しました。もう一度お試しください。(エラー: ' + e + ')';
		scene = 'choice';
	}

	onMount(() => {
		if (!authInfo?.signedIn()) {
			rejected('Not signed in');
		}

		new Promise((resolve, reject) => {
			const userId = authInfo?.getUserId();

			fetch(`${import.meta.env.VITE_API_SERVER_ORIGIN}/suggester/${userId}`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					emotion: chosenEmotion || '',
					prompt: prompt || ''
				})
			})
				.then((res) => {
					return res.json();
				})
				.then((json) => {
					if (json['musics'] && json['comment']) {
						const rawTracks = json['musics'].map((track: any) => track.track_id);
						const rawComment = json['comment'];
						resolve([rawTracks, rawComment]);
					} else {
						reject('Invalid response');
					}
				})
				.catch((e) => {
					reject(e);
				});
		})
			.then((result) => {
				const [rawTracks, rawComment] = result as [string[], string];
				comment = rawComment;
				const data = (rawTracks as string[]).map((track, i) => {
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

				Promise.all(data)
					.then((ts) => {
						tracks = ts;
						chosenEmotion = '';
						prompt = '';
						alert = '';
					})
					.catch((e) => {
						rejected(e);
					});
			})
			.catch((e) => {
				rejected(e);
			});
	});

	$: chosenTrack = tracks ? tracks[0] : undefined;
</script>

<Window>
	{#if chosenTrack}
		<div class="text-lg m-b-3">このような音楽はいかがでしょうか？</div>
		<div class="text-md m-b-3"><Typewriter text={comment} /></div>
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
		<div class="text-lg m-b-3"><Typewriter text="考えています..." /></div>
		<div class="text-4xl m-auto text-center bg-transparent animate-spin">
			<div class="i-tabler-loader-2"></div>
		</div>
	{/if}
</Window>

<AccountConfig {authInfo} {authController} />
