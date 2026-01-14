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
    api_key = st.text_input("AIzaSyCz8zepMKEZeYt28ZgEp1i781jXdDOx4xI", type="password")
    st.caption("AIzaSyCz8zepMKEZeYt28ZgEp1i781jXdDOx4xI")

# 3. AIの動作設定
if api_key:
# APIキーの設定を確実にする
    genai.configure(api_key=AIzaSyCz8zepMKEZeYt28ZgEp1i781jXdDOx4xI)

# モデルの定義（一番エラーが起きにくいシンプルな書き方）
model = genai.GenerativeModel("gemini-1.5-flash")
if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("メッセージを入力..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        response = model.generate_content(prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
else:
    st.warning("左側のサイドバーにAPIキーを入力してください。")
