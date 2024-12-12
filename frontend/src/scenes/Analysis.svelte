<script lang="ts">
	import AccountConfig from '../components/AccountConfig.svelte';
	import type { AuthInfo, AuthController } from '../lib/oauth/spotify';
	import DrawBox from '../components/DrawBox.svelte';
	import * as THREE from 'three';
	import Window from '../components/Window.svelte';
	import PressButton from '../components/PressButton.svelte';
	import { FontLoader } from 'three/examples/jsm/loaders/FontLoader.js';
	import { TextGeometry } from 'three/examples/jsm/geometries/TextGeometry.js';

	export let authInfo: AuthInfo | null;
	export let authController: AuthController;
	export let scene: string;

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
	const emotion_table: { [key: string]: string } = {
		"envious": "嫉妬",
		"disgusting": "嫌悪",
		"asshamed": "恥",
		"lonely": "孤独感",
		"angry": "怒り",
		"anxious": "不安",
		"fear": "恐怖",
		"complicated": "複雑"
	} 

	function createDrawElement(root: HTMLCanvasElement) {
        const scene = new THREE.Scene();
		const canvasWidth = root.clientWidth;
		const canvasHeight = root.clientHeight;
		const camera = new THREE.OrthographicCamera(
			0, canvasWidth, // left, right
			canvasHeight, 0, // top, bottom
			-1000, 1000 // near, far
		);
		const renderer = new THREE.WebGLRenderer({ alpha: true , antialias: true });

		renderer.setPixelRatio(window.devicePixelRatio * 2);
        renderer.setSize(root.clientWidth, root.clientHeight);

        // ヒストグラムデータ
		const emotionFreq: { [key: string]: number } = analysis["per_total"]["emotion_freq"];
		console.log(emotionFreq["sad"] || 0)
        const emotion_table = {
            "envious": "嫉妬",
            "disgusting": "嫌悪",
            "asshamed": "恥",
            "lonely": "孤独感",
            "angry": "怒り",
            "anxious": "不安",
            "fear": "恐怖",
            "complicated": "複雑"
        };

		console.log(root.clientWidth, root.clientHeight)
        // ヒストグラムのバーを作成
		const barNum = Object.keys(emotion_table).length;
		const barSpacing = 10.0;
		const barWidth = (canvasWidth - barSpacing * (barNum - 1)) /barNum;  // バーの幅を計算
        const maxBarHeight = canvasHeight * 0.8;  // バーの最大高さをキャンバスの高さに基づいて設定

		console.log("barWidth", barWidth, "barSpacing", barSpacing, "maxBarHeight", maxBarHeight)
		
		const maxValue = Math.max(...Object.values(emotionFreq));
		Object.entries(emotion_table).forEach(([emotion, emotion_text], index) => {
			const value = emotionFreq[emotion] || 0;  // emotionFreq から値を取得、存在しない場合は 0
			const barHeight = (value / maxValue) * maxBarHeight;  // バーの高さを計算
            const geometry = new THREE.PlaneGeometry(barWidth, barHeight);
			const material = new THREE.MeshBasicMaterial({ color: 0x00cccc });
			const bar = new THREE.Mesh(geometry, material);
			bar.position.x = index * (barWidth + barSpacing) + barWidth/2;
            bar.position.y = barHeight / 2 + 50;  // バーの中心をキャンバスの中央に配置
			scene.add(bar);
			console.log("pos",bar.position.x, bar.position.y)
			
			// 感情ラベルを追加
            const loader = new FontLoader();
            loader.load('../public/fonts/IBMPlexSansJP_Regular.json', function (font) {
                const textGeometry = new TextGeometry(emotion_text, {
                    font: font,
                    size: 0.2,
                    depth: 0.05,
                    curveSegments: 50  // ここでテキストの滑らかさを向上させる
                });
                const textMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff });
                const textMesh = new THREE.Mesh(textGeometry, textMaterial);
                textMesh.position.x = bar.position.x;
				textMesh.position.y = 0;
                scene.add(textMesh);
            });
			
		});

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

<Window>
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

	<div class="m-x-auto m-y-5">
		<PressButton
			type="sub"
			onClick={() => {
				scene = 'title';
			}}>タイトルに戻る</PressButton
		>
	</div>
</Window>

<AccountConfig {authInfo} {authController} />
