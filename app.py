import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="●●社様オリジナル対話AI", layout="centered")

# --- 【カスタマイズ：画像】 ---
char_image_url = "https://daiei-recruit.net/company/img/i_1.jpg" 
st.image(char_image_url, width=150)

st.title("仏衣のご提案シミュレーター")
st.write("「仏衣って興味あるんだけどどういうメリットあるの？」")

# --- 2. サイドバーの設定 ---
with st.sidebar:
    st.title("設定")
    # APIキー（※本来は st.secrets 等で管理するのが安全です）
    api_key = "AIzaSyCz8zepMKEZeYt28ZgEp1i781jXdDOx4xI"

# --- 3. AIの動作設定 ---
genai.configure(api_key=api_key)

# 【ここが重要】モデル名の変更と、NotebookLMの設定（システム指示）の追加
# system_instruction の中に NotebookLM で使っていた指示文を入れてください
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", 
    system_instruction="ここにNotebookLMからインポートした『設定（振る舞いや知識）』を貼り付けてください。"
)

# チャット履歴の初期化
if "messages" not in st.session_state:
    st.session_state.messages = []

# 保存されている過去の会話を表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# チャット入力欄
if prompt := st.chat_input("メッセージを入力..."):
    # ユーザーの入力を表示・保存
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AIに返答をリクエスト
    try:
        # 過去の文脈を含めて送信したい場合は start_chat を使うのが理想的ですが、
        # 今回はシンプルに generate_content で実装します。
        response = model.generate_content(prompt)
        ai_response = response.text
        
        # AIの返答を表示・保存
        with st.chat_message("assistant"):
            st.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
