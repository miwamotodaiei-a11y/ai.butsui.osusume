import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="●●社様オリジナル対話AI", layout="centered")

# --- 1. 画像とタイトルの表示 ---
char_image_url = "https://daiei-recruit.net/company/img/i_1.jpg" 
st.image(char_image_url, width=150)

st.title("仏衣のご提案シミュレーター")
st.write("「仏衣って興味あるんだけどどういうメリットあるの？」")

# --- 2. サイドバーの設定 ---
with st.sidebar:
    st.title("設定")
    # APIキー
    api_key = "AIzaSyCz8zepMKEZeYt28ZgEp1i781jXdDOx4xI"

# --- 3. AIの動作設定 ---
if not api_key:
    st.error("APIキーが設定されていません。")
else:
    genai.configure(api_key=api_key)
    
    # モデルの定義（最新の安定版指定）
    # system_instructionにNotebookLMの設定を入れてください
    instruction = "あなたは葬儀の専門家です。お客様に寄り添い、仏衣のメリットを優しく丁寧に説明してください。"
    
    # モデル名を 'models/gemini-1.5-flash' とフルパスで書くことで解決する場合があります
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=instruction
    )

# --- 4. チャット履歴の初期化 ---
if "chat_session" not in st.session_state:
    # 履歴を保持するセッションを開始
    st.session_state.chat_session = model.start_chat(history=[])

# 過去の会話を表示
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# --- 5. チャット入力欄 ---
if prompt := st.chat_input("メッセージを入力..."):
    # ユーザーの入力を表示
    with st.chat_message("user"):
        st.markdown(prompt)

    # AIに返答をリクエスト
    try:
        # sendMessageを使うことで、これまでの会話の流れをAIが覚えてくれます
        response = st.session_state.chat_session.send_message(prompt)
        
        # AIの返答を表示
        with st.chat_message("assistant"):
            st.markdown(response.text)
            
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
        st.info("ヒント: ライブラリのバージョンが古い可能性があります。ターミナルで 'pip install -U google-generativeai' を実行してみてください。")
