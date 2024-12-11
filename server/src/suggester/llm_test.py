from langchain_community.llms.llamacpp import LlamaCpp
from langchain_core.prompts import PromptTemplate

# from langchain.chains.llm import LLMChain
import os

# スクリプトがあるディレクトリを取得
gguf_dir = os.path.dirname(os.path.realpath(__file__))

# 保存先ファイルパスを設定
file_path = os.path.join(gguf_dir, "resources/Llama-3-ELYZA-JP-8B-q4_k_m.gguf")
# モデルのパス
model_path = file_path

# プロンプトテンプレートの定義
question_prompt_template = """
[INST]
{question} 
[/INST]
"""

# プロンプトの設定
QUESTION_PROMPT = PromptTemplate(
    template=question_prompt_template,  # プロンプトテンプレートをセット
    input_variables=["question"],  # プロンプトに挿入する変数
)

# モデルの設定
llm = LlamaCpp(
    model_path=model_path,  # ダウンロードしたモデルのローカルパス
    n_gpu_layers=25,  # gpuに処理させるlayerの数
    # stop=["コンピュータ", "人間"], # 停止文字列
)

# 質問回答chainの設定
chain = QUESTION_PROMPT | llm

while True:
    question = input("文字列を入力してください（終了するには 'exit' を入力）：")
    if question.lower() == "exit":  # 'exit' で終了
        print("終了します。")
        break
    # print(f"入力された文字列：{question}")
    response = chain.invoke(question)
    print(response)
