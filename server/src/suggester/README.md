# APIキーやLLMの実体の配置について

## APIキー
- post-09/server（requirements.lockと同じ階層）に.envファイルを作る
- 以下の形式で記述
  SPOTIFY_CLIENT_ID = "XXXXXXXXXXXXXXXXXXXXXXXXX"
  SPOTIFY_CLIENT_SECRET = "XXXXXXXXXXXXXXXXXXXXXXXXX"
  
## LLM 
- 以下にファイルを配置
  post-09/server/src/suggester/resources/Llama-3-ELYZA-JP-8B-q4_k_m.gguf
- ggufファイルは以下のURLからwgetできる
  https://huggingface.co/elyza/Llama-3-ELYZA-JP-8B-GGUF/resolve/main/Llama-3-ELYZA-JP-8B-q4_k_m.gguf

※別のgguf、もしくは.binを使うこともできる
