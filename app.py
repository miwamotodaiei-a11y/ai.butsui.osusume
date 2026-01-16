import streamlit as st
import google.generativeai as genai

# =========================
# ページ設定
# =========================
st.set_page_config(
    page_title="●●社様オリジナル対話AI",
    layout="centered"
)

# =========================
# Gemini API 設定
# =========================
genai.configure(
    api_key=st.secrets["GEMINI_API_KEY"]
)

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash"
)

# =========================
# 画面上部（画像＋タイトル）
# =========================
char_image_url = "https://daiei-recruit.net/company/img/i_1.jpg"
st.image(char_image_url, width=150)

st.title("仏衣のご提案シミュレーター")
st.write("「仏衣って興味あるんだけど、どういうメリットがあるの？」")

st.divider()

# =========================
# チャット履歴の初期化
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# これまでの会話を表示
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =========================
# チャット入力
# =========================
user_input = st.chat_input("こんにちは、って話しかけてみて😊")

if user_input:
    # ユーザーの発言を保存・表示
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        # Gemini 呼び出し（system role は使わない）
        response = model.generate_content(user_input)
        reply = response.text

    except Exception as e:
        reply = f"⚠️ エラーが発生しました\n\n{e}"

    # Gemini の返答を保存・表示
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )
    with st.chat_message("assistant"):
        st.markdown(reply)
