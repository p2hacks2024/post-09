# P2HACKS2024 アピールシート 

<div align="center">
</br>
<div>FlushTune</div>
<div>〜 Flashbackを音楽でFlushする 〜</div>
</br>
<img src="docs/image/top.png" alt="top"></img>
</div>


## プロダクト名  
FlushTune

## コンセプト  

**「Flashbackを音楽でFlushする」**
をテーマに、ユーザーが思い出した出来事・感情を分析し、音楽の提案を行うプロダクトです。

- ユーザーがふと思い出した嫌な出来事（フラッシュバック）を入力すると、FlushTuneが心理状態にマッチした楽曲を提案
    - 心の落ち着きを支援
- 今までのフラッシュバックの履歴を分析・可視化
    - ユーザーが自身のストレス状態を振り返り、心の不安定さの改善のきっかけに

## 対象ユーザ  
- ストレスが溜まりやすい方
- ストレスの溜まりやすい環境にいる方
- 普段音楽でストレスを解消している方
- 出来事や感情を言語化し、心を落ち着けるためのアドバイスをもらいたい方

## 利用の流れ  

<div align="center" style="display: flex; gap: 2px">
<img src="docs/image/scene-title.png" alt="title" width="200"></img>
<img src="docs/image/scene-choice.png" alt="choice" width="200"></img>
<img src="docs/image/scene-playing.png" alt="playing" width="200"></img>
<img src="docs/image/scene-analysis.png" alt="analysis" width="200"></img>
</div>

1. FlushTuneにSpotifyアカウントでログインする
1. ユーザーが出来事（フラッシュバック）や感情を入力
1. LLMがユーザーの感情を分析
1. 感情分析に基づき、Spotify上の楽曲を複数提案
3. ユーザーは楽曲を聴くことで、ストレスを和らげる
    - Spotify上の自身のプレイリストに楽曲を保存することも可能
4. 過去の入力に基づく感情の記録を表示

## 推しポイント  

- **ローカルLLMの活用**
    - 主な用途
        - ユーザーの入力から感情を分析
        - 提案する楽曲のテーマを選定
            - Spotify APIと連携し、実際に聴ける楽曲として提案
        - フラッシュバックした出来事や感情から、ストレスを和らげるアドバイスを提示
    - ローカルLLMにより、**人に知られたくない情報が流出しない**
        - プライバシーの保護を実現
- **手軽な使い勝手を意識**
    - フラッシュバックした出来事を忘れないうちに入力できるよう、シンプルなUIに
    - PWA (Progressive Web Application) を採用し、端末にインストール可能に
- 明るすぎない・鮮やかすぎない見た目
    - フラッシュバックの多い夜の時間に、眠気を阻害しない


## 開発体制  

### 役割分担

#### jigsaw-glitch (a)

- **LLM開発**
- バックエンド開発
- プロダクトのコンセプト提案

#### 多田 瑛貴 (peruki)

- **フロントエンド開発**
- システムの全体構成策定・技術選定

#### 吉野 颯真 (moqumo)

- **バックエンド開発**
- 記録の可視化


## 開発における工夫した点  

### チームワーク

- 複雑系コースならではの**各メンバーの高い専門性**を考慮し、それぞれの役割に注力できるよう工夫
    - ソフトウェアの各部品の**入出力を最優先で定義**
        ![全体構成図](docs/image/architecture.webp)
        - 入出力: 関数の引数/返り値、HTTPリクエスト/レスポンスなど
    - 入出力に合わせた各部品の具体的な実装を、担当者に全面的に委任
    - コードやブランチ運用のスタイルは、PEP8やGitHubフローを意識しつつ、規則や信条で強制しない方針に
        - (リンタ・フォーマッタ等により) 自動化できる範囲のみ、一貫性を守る
        - 変数・ブランチの命名をはじめ、開発に直接関わらない細かなコミュニケーションを削減
- Webフロントエンドの自動デプロイ
    - 正しくビルドできるかを確認
    - 見た目や画面遷移を全員で共有できるように



### 情報共有
- Discord中心の情報共有
    - ソースを見失わないために、意図的にDiscordに情報を集積させる
    - 開発に役立つ・役立ちそうな知識を共有 (#knowledge)
        - 技術に関する知識
        - トラブルシューティング記事
        - 方向性の似た既存のプロダクトの事例
    - GitHubのWebhookでコードの更新を自動キャッチアップ (#github-notify)
    - 重要な情報や他ツールへのリンク (#url置き場-保存用)
        - 手書きの全体構成図やプロダクト概要を添付
- FigJam
    - アイデアのブレインストーミング
- Github Projectsを必要な場面で適宜利用し、issueを整理
- 対面での共同作業時間を明確に確保


## 開発技術 

![システム構成](docs/image/system.png)

### LLM開発
- フレームワーク：**LangChain**
    - LLMの出力を効率的に管理 
    - Pythonのデータバリデーションライブラリ Pydantic と連携
        - 入力データの型や内容の厳密なバリデーションをLLMに強制
    - LLMの出力を構造化
        - 後続の処理にシームレスに渡している

- モデル：**Llama-3-ELYZA-JP-8B-GGUF**
ライセンス：[META LLAMA 3 COMMUNITY LICENSE AGREEMENT](https://www.llama.com/llama3/license/)
    - ELYZA, Inc. による80億パラメータの日本語特化LLM 
    - Meta社によるLLMモデル Meta-Llama-3-8B-Instructsを日本語での使用向けにチューニングしたモデル
    - 4bit量子化
        - 計算資源が限られた環境でも効率よく動作
        - ベンチマークELYZA-tasks-100 GPT4 scoreにおいて量子化前からの性能劣化が小さい


### バックエンド

AI分野のスタンダードであるPythonを軸とした技術選定です。
- 現代的なツールの導入
    - 特に、パッケージマネージャ Rye・静的型チェッカー Pyright
    - パッケージ管理や実行の安全性といった、Python特有の問題点に対処
        - 一般的な静的型付け言語と変わらない開発効率へ
- 共通のVSCodeの設定と拡張機能を、事前に個別の環境に導入
    - 自動の型チェックやフォーマットを、齟齬なく行えるように
    - CI/CDの構築も不要に

#### 使用言語

- Python3
- (SQL)

#### フレームワーク

- FastAPI
  - swaggerUI生成機能により、実装と差異のないドキュメント・テスト環境を整備
- SQLite
  - RDBMS

#### 開発ツール


- Rye
     - パッケージ・仮想環境管理
- Pytest
     - 動的解析
- Pydantic
    - データバリデーション
- Pylance (VSCode拡張)
     - linter
- Pyright
     - 型チェック
- Ruff (VSCode拡張)
     - フォーマッタ
     - formatOnSaveを有効化

### フロントエンド

動きのあるUIや視覚効果に特化した技術選定です。またPWA (Progressive Web Application) を採用し、PC・モバイルの双方でネイティブアプリケーションに近い使用感を実現しています。

PWA・UIのアニメーション・描画APIといった制約の多い開発要件から、純粋なTypeScriptでのWeb開発に近い、必要最小限のツール構成を意識しています。

#### 使用言語

- TypeScript

#### フレームワーク

- Svelte
     - UI構築ライブラリ
     - UIのアニメーションや描画APIとの親和性から採用
     - ルーティング不要のため、SvelteKitは不使用
- UnoCSS
     - Utility-first CSS
     - Tailwind CSS (PostCSSに依存) の代替として導入
     - アイコンプリセット機能も活用
- Three.js
     - 描画ライブラリ
     - 記録の可視化に使う予定であったが、Svelte+UnoCSSで十分であったため、最終的にはロゴ描画のみに使用

#### 開発支援ツール

- Vite
    - ビルドツール
- Vite PWA
    - PWA導入のためのVite Plugin


### その他の開発技術

- OAuth (Spotify)
