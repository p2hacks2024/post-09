<script lang="ts">
	import AccountConfig from '../components/AccountConfig.svelte';
	import type { AuthInfo, AuthController } from '../lib/oauth/spotify';
	import { emotionTable } from '../lib/emotionTable';
	import DrawBox from '../components/DrawBox.svelte';
	import * as THREE from 'three';
	import Window from '../components/Window.svelte';
	import PressButton from '../components/PressButton.svelte';
	import SelectButton from '../components/SelectButton.svelte';
	import DrawSituationList from '../components/DrawSituationList.svelte';
	import { FontLoader } from 'three/examples/jsm/loaders/FontLoader.js';
	import { TextGeometry } from 'three/examples/jsm/geometries/TextGeometry.js';

	export let authInfo: AuthInfo | null;
	export let authController: AuthController;
	export let scene: string;

	let analysis: any = undefined;

	const emotions = Object.values(emotionTable);
	const emotions_selection = emotions;
	let chosenEmotion = '';

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

	function createDrawElement(root: HTMLCanvasElement) {
        const scene = new THREE.Scene();
		const canvasWidth = root.clientWidth * 0.7;
		const canvasHeight = root.clientHeight * 0.7;
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

		console.log(root.clientWidth, root.clientHeight)
        // ヒストグラムのバーを作成
		const barNum = Object.keys(emotionTable).length;
		const barSpacing = 5.0;
		const barWidth = (canvasWidth - barSpacing * (barNum + 1)) /barNum;  // バーの幅を計算
        const maxBarHeight = canvasHeight * 0.8;  // バーの最大高さをキャンバスの高さに基づいて設定

		console.log("barWidth", barWidth, "barSpacing", barSpacing, "maxBarHeight", maxBarHeight)
		
		const fontSize = canvasWidth * 0.03;  // テキストのフォントサイズを設定
		console.log("fontSize", fontSize);

		const maxValue = Math.max(...Object.values(emotionFreq));
		
		// emotionTable の各要素に対してバーを作成
        emotions.forEach((emotion, index) => {
            const value = emotionFreq[emotion] || 0;  // emotionFreq から値を取得、存在しない場合は 0
            const barHeight = (value / maxValue) * maxBarHeight;  // バーの高さを計算
            const geometry = new THREE.PlaneGeometry(barWidth, barHeight);
            const material = new THREE.MeshBasicMaterial({ color: 0x00cccc });
            const bar = new THREE.Mesh(geometry, material);
            bar.position.x = index * (barWidth + barSpacing) + barWidth / 2 + barSpacing;
            bar.position.y = barHeight / 2 + 50;
            scene.add(bar);

            // 感情ラベルを追加
            const loader = new FontLoader();
            loader.load('fonts/IBMPlexSansJP_Regular.json', function (font) {
                const textGeometry = new TextGeometry(emotion, {
                    font: font,
                    size: fontSize,
                    height: 0.05,
                    curveSegments: 50  // ここでテキストの滑らかさを向上させる
                });
                textGeometry.computeBoundingBox();  // バウンディングボックスを計算
                const textWidth = textGeometry.boundingBox ? textGeometry.boundingBox.max.x - textGeometry.boundingBox.min.x : 0;  // テキストの横幅を計算
                const textHeight = textGeometry.boundingBox ? textGeometry.boundingBox.max.y - textGeometry.boundingBox.min.y : 0;  // テキストの縦幅を計算
                console.log("Text width:", textWidth, "Text height:", textHeight);

                const textMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff });
                const textMesh = new THREE.Mesh(textGeometry, textMaterial);
                textMesh.position.x = bar.position.x - textWidth / 2;  // テキストを中央に配置
                textMesh.position.y = 50 - textHeight;  // バーの下に配置
                scene.add(textMesh);
            });
        });

        const animate = function () {
            renderer.render(scene, camera);
        };
        renderer.setAnimationLoop(animate);

        return renderer.domElement;
    };
	
	function createSituationList(){
		let emotion_to_recent_situation = analysis["per_total"]["emotion_to_recent_situation"];
		let situations = [];
		situations = chosenEmotion ? emotion_to_recent_situation[chosenEmotion] : [];
		console.log(situations);
		return situations;
	}
</script>

<Window>
	<h1 class="text-4xl font-bold">記録</h1>
	<p class="text-lg">記録A...</p>
	<DrawBox boxId="0" createElementFunc={createDrawElement} {analysis} />
	<p class="text-lg">記録B...</p>

	<div class="flex justify-start w-full gap-1 flex-wrap">
		{#each emotions_selection as emotion}
			<SelectButton
				category={emotion}
				selected={emotion === chosenEmotion}
				onClick={() => {
					chosenEmotion = emotion;
				}}
			/>
		{/each}
	</div>

	<DrawSituationList createSituationList={createSituationList} {chosenEmotion} />	
	
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
