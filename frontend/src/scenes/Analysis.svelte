<script lang="ts">
	import AccountConfig from '../components/AccountConfig.svelte';
	import type { AuthInfo, AuthController } from '../lib/oauth/spotify';
	import DrawBox from '../components/DrawBox.svelte';
	import * as THREE from 'three';

	export let authInfo: AuthInfo | null;
	export let authController: AuthController;

	let analysis: any = undefined;

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

	// 参考: Three.js
	function createDrawElement(root: HTMLCanvasElement) {
		const scene = new THREE.Scene();
		const camera = new THREE.PerspectiveCamera(40, root.clientWidth / root.clientHeight, 0.1, 100);
		const renderer = new THREE.WebGLRenderer({ alpha: true });

		renderer.setSize(root.clientWidth, root.clientHeight);
		camera.position.z = 5;

		const geometry = new THREE.PlaneGeometry(1, 1);
		const material = new THREE.MeshBasicMaterial({ color: 0x00cccc });
		const plane = new THREE.Mesh(geometry, material);

		scene.add(plane);

		const animate = function () {
			renderer.render(scene, camera);
		};
		renderer.setAnimationLoop(animate);

		return renderer.domElement;
	}

	// 参考: Canvas2D
	function createDrawElement2(root: HTMLCanvasElement) {
		const canvas = document.createElement('canvas');
		canvas.width = root.clientWidth;
		canvas.height = root.clientHeight;
		const ctx = canvas.getContext('2d') as CanvasRenderingContext2D;
		if (!ctx) {
			throw new Error('Failed to get 2D context');
		}

		// draw simple rectangle
		ctx.fillStyle = '#cc00cc';
		ctx.fillRect(canvas.width / 4, canvas.height / 4, canvas.width / 2, canvas.height / 2);

		return canvas;
	}
</script>

<div class="h-full text-fwhite flex flex-col justify-center">
	<h1 class="text-4xl font-bold">記録</h1>
	<p class="text-lg">記録A...</p>
	<DrawBox boxId="0" createElementFunc={createDrawElement} {analysis} />
	<p class="text-lg">記録B...</p>
	<DrawBox
		boxId="1"
		hasBorder={true}
		heightClass="h-20"
		createElementFunc={createDrawElement2}
		{analysis}
	/>

	<p class="text-2">{JSON.stringify(analysis)}</p>
</div>

<AccountConfig {authInfo} {authController} />
