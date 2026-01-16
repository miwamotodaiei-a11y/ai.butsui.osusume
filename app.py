import streamlit as st
import google.generativeai as genai

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
# Streamlit UI
# =========================
st.set_page_config(page_title="Gemini チャット", page_icon="🤖")
st.title("🤖 Gemini チャット")

# チャット履歴を保存
if "messages" not in st.session_state:
    st.session_state.messages = []

# これまでの会話表示
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 入力欄
user_input = st.chat_input("こんにちは、って話しかけてみて😊")

# =========================
# Gemini 呼び出し
# =========================
if user_input:
    # ユーザー発言を保存
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        # ★ system は使わない ★
        response = model.generate_content(user_input)
        reply = response.text

    except Exception as e:
        reply = f"⚠️ エラーが発生しました\n\n{e}"

    # Geminiの返答を保存
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

    with st.chat_message("assistant"):
        st.markdown(reply)
