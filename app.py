import streamlit as st
from streamlit.components.v1 import html

# =====================
# 初期設定
# =====================
st.set_page_config(page_title="AI会話デモ", layout="centered")

if "started" not in st.session_state:
    st.session_state.started = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if "ended" not in st.session_state:
    st.session_state.ended = False


# =====================
# 音声読み上げ関数（JS）
# =====================
def speak(text):
    html(
        f"""
        <script>
        const msg = new SpeechSynthesisUtterance("{text}");
        msg.lang = "ja-JP";
        window.speechSynthesis.speak(msg);
        </script>
        """,
        height=0
    )


# =====================
# タイトル
# =====================
st.title("🗣️ AI 音声会話デモ")


# =====================
# ボタンエリア
# =====================
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("▶ スタート"):
        st.session_state.started = True
        st.session_state.ended = False
        st.session_state.messages = []

        first_message = "こんにちは！今日はどんなお話をしましょうか？"
        st.session_state.messages.append(("AI", first_message))
        speak(first_message)

with col2:
    if st.button("🔄 最初からやり直す"):
        st.session_state.started = False
        st.session_state.ended = False
        st.session_state.messages = []

with col3:
    if st.button("⛔ 終了（中断）"):
        st.session_state.ended = True
        st.session_state.started = False

        summary = "ここまでのお話、ありがとうございました。今回はここで終了します。"
        st.session_state.messages.append(("AI", summary))
        speak(summary)


# =====================
# 会話表示
# =====================
st.divider()

for speaker, msg in st.session_state.messages:
    if speaker == "AI":
        st.markdown(f"**🤖 AI**：{msg}")
    else:
        st.markdown(f"**🧑 あなた**：{msg}")


# =====================
# 入力欄（会話中のみ）
# =====================
if st.session_state.started and not st.session_state.ended:
    user_input = st.text_input("あなたの発言を入力してください")

    if user_input:
        st.session_state.messages.append(("あなた", user_input))

        # ここは仮のAI応答（後でChatGPT / Gemini差し替え可）
        ai_reply = f"なるほど、「{user_input}」なんですね。もう少し教えてください。"
        st.session_state.messages.append(("AI", ai_reply))
        speak(ai_reply)
