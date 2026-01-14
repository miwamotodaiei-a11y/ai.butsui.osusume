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

# 2. サイドバーの設定（APIキー入力欄）
with st.sidebar:
    st.title("設定")
    api_key = "AIzaSyCz8zepMKEZeYt28ZgEp1i781jXdDOx4xI"

# 3. AIの動作設定
# if not api_key:
#     st.info("左側のサイドバーにAPIキーを入力してください。")
#     st.stop()

# --- 3. AIの動作設定 ---
# ここで確実にAPIキーを登録し、モデルを準備します
genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-1.5-flash")

# チャット履歴の保存
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
