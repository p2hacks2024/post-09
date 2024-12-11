<script lang="ts">
	import { onMount } from 'svelte';
	import AccountConfig from '../components/AccountConfig.svelte';
	import type { AuthInfo, AuthController } from '../lib/oauth/spotify';
	import * as THREE from 'three';

	export let authInfo: AuthInfo | null;
	export let authController: AuthController;

	let analysis: any;

	$: if (authInfo?.signedIn()) {
		//const userId = authInfo?.getUserId();
		const userId = '0001'; // TODO: remove this line!

		fetch(`${import.meta.env.VITE_API_SERVER_ORIGIN}/analysis/${userId}`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			}
		})
			.then((res) => {
				return res.json();
			})
			.then((json) => {
				analysis = json;
			})
			.catch((e) => {
				console.error(e);
			});
	}

	onMount(() => {
		const canvas = document.getElementById('canvas');
		if (!canvas) {
			return;
		}

		const scene = new THREE.Scene();
		const camera = new THREE.PerspectiveCamera(
			40,
			canvas.clientWidth / canvas.clientHeight,
			0.1,
			100
		);
		const renderer = new THREE.WebGLRenderer({ alpha: true });

		renderer.setSize(canvas.clientWidth, canvas.clientHeight);
		camera.position.z = 5;

		// draw simple plane
		const geometry = new THREE.PlaneGeometry(1, 1);
		const material = new THREE.MeshBasicMaterial({ color: 0x00cccc });
		const plane = new THREE.Mesh(geometry, material);

		scene.add(plane);

		const animate = function () {
			renderer.render(scene, camera);
		};
		renderer.setAnimationLoop(animate);

		canvas.appendChild(renderer.domElement);
	});
</script>

<div class="h-full text-fwhite flex flex-col justify-center">
	<h1 class="text-4xl font-bold">記録</h1>
	<p class="text-lg">記録をフラッシュ</p>

	<div class="w-full h-50 overflow-hidden bg-transparent" id="canvas"></div>

	<p class="text-sm">{JSON.stringify(analysis)}</p>
</div>

<AccountConfig {authInfo} {authController} />
