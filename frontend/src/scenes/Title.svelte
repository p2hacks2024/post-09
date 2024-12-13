<script lang="ts">
	import AccountConfig from '../components/AccountConfig.svelte';
	import DrawBox from '../components/DrawBox.svelte';
	import Logo from '../components/Logo.svelte';
	import PressButton from '../components/PressButton.svelte';
	import Window from '../components/Window.svelte';
	import type { AuthInfo, AuthController } from '../lib/oauth/spotify';
	import * as THREE from 'three';

	export let authInfo: AuthInfo | null;
	export let authController: AuthController;

	export let scene: string;
	class StarGeometry {
		num_points: number;
		scale: number;
		prop: number;

		constructor(num_points: number, scale: number, prop: number) {
			this.num_points = num_points;
			this.scale = scale;
			this.prop = prop;
		}

		getGeometry(t: number) {
			let points = [];
			for (let i = 0; i < this.num_points; i++) {
				const r =
					Math.pow(Math.cos(t + (i / this.num_points) * 4 * Math.PI * 2), 2) * this.prop +
					(1 - this.prop);

				const x = Math.cos((i / this.num_points) * Math.PI * 2) * r * this.scale;
				const y = Math.sin((i / this.num_points) * Math.PI * 2) * r * this.scale;
				const point = new THREE.Vector2(x, y);
				points.push(point);
			}
			let shape = new THREE.Shape(points);
			let geometry = new THREE.ShapeGeometry(shape);
			return geometry;
		}
	}

	function createDrawElement(root: HTMLCanvasElement) {
		const scene = new THREE.Scene();
		const camera = new THREE.PerspectiveCamera(30, root.clientWidth / root.clientHeight, 0.1, 80);
		const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });

		renderer.setSize(root.clientWidth, root.clientHeight);
		camera.position.z = 5;

		const star0 = new StarGeometry(40, 1.0, 0.7);
		const plane0 = new THREE.Mesh(
			star0.getGeometry(0),
			new THREE.MeshBasicMaterial({ color: 0x7755dd })
		);
		const star1 = new StarGeometry(24, 0.7, 0.5);
		const plane1 = new THREE.Mesh(
			star0.getGeometry(0),
			new THREE.MeshBasicMaterial({ color: 0xaa66ee })
		);
		const star2 = new StarGeometry(22, 0.3, 0.3);
		const plane2 = new THREE.Mesh(
			star0.getGeometry(0),
			new THREE.MeshBasicMaterial({ color: 0xddf0f0 })
		);

		scene.add(plane0);
		scene.add(plane1);
		scene.add(plane2);
		const animate = function () {
			const t = Date.now() * 0.001;
			plane0.geometry = star0.getGeometry(t);
			plane1.geometry = star1.getGeometry(t + 0.4);
			plane2.geometry = star2.getGeometry(t + 0.8);

			// rotate
			plane0.rotation.z = t * 0.1;
			plane1.rotation.z = t * 0.1 + 0.4;
			plane2.rotation.z = t * 0.1 + 0.8;

			renderer.render(scene, camera);
		};
		renderer.setAnimationLoop(animate);

		return renderer.domElement;
	}
</script>

<Window>
	<Logo />
	<h1 class="text-4xl font-bold">FlushTune</h1>
	<p class="text-lg text-center">素敵な音楽で<br />嫌な思い出をフラッシュ</p>
	<div class="h-5"></div>

	<PressButton
		onClick={() => {
			if (authInfo?.signedIn()) {
				scene = 'choice';
			} else if (authInfo != null) {
				authController.oauth2SignIn();
			} else {
				return;
			}
		}}
		>{authInfo?.signedIn()
			? '記録する'
			: authInfo != null
				? 'Spotifyで認証する'
				: '確認中...'}</PressButton
	>
	{#if authInfo?.signedIn()}
		<div class="m-t-5">
			<PressButton
				type="sub"
				onClick={() => {
					scene = 'analysis';
				}}>{authInfo.getName()}さんの記録を見る</PressButton
			>
		</div>
	{/if}
</Window>

<AccountConfig {authInfo} {authController} />
