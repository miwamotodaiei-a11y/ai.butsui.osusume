import streamlit as st
import google.generativeai as genai

# 1. ページのデザイン設定
st.set_page_config(page_title="●●社様オリジナル対話AI", layout="centered")

# --- 【カスタマイズ：画像】 ---
# 表示したいキャラクター画像のURLを入れてください
char_image_url = "https://daiei-recruit.net/company/img/i_1.jpg" 
st.image(char_image_url, width=150)

st.title("オリジナル対話トレーニング")
st.write("設定したキャラクターとの会話を始めましょう！")

# --- 2. サイドバーの設定 ---
with st.sidebar:
    st.title("設定")
    # APIキーをここで直接定義
    api_key = "AIzaSyCz8zepMKEZeYt28ZgEp1i781jXdDOx4xI"

# --- 3. AIの動作設定（ここを一番最初に持ってくる） ---
# まず鍵を登録する
genai.configure(api_key=api_key)

# モデルの定義を、最も互換性の高い名前に変更します
model = genai.GenerativeModel("gemini-pro")

# チャット履歴の初期化
if "messages" not in st.session_state:
    st.session_state.messages = []

# 保存されている過去の会話を表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# チャット入力欄
if prompt := st.chat_input("メッセージを入力..."):
    # ユーザーの入力を画面に出して保存
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AIに返答をリクエスト
    try:
        response = model.generate_content(prompt)
        ai_response = response.text
        
        # AIの返答を画面に出して保存
        with st.chat_message("assistant"):
            st.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
