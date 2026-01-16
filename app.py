import streamlit as st
import google.generativeai as genai

# =========================
# 🔑 Gemini API 設定
# =========================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-pro")

# =========================
# 🎭 システムプロンプト（魂）
# =========================
SYSTEM_PROMPT = """
あなたは「葬儀社の担当者」です。

【あなたの立場】
・葬儀社で実務を担当している
・仏衣について、知識はあるが専門家ではない
・価格・在庫・品質・遺族対応のしやすさを重視する

【ロールプレイルール】
・あなたは必ず「葬儀社側」としてのみ発言する
・営業マン（人間）が話した内容に対して返答する
・自分から話しすぎず、会話の主導権は営業マンに渡す
・質問されたら、現場目線で正直に答える
・ときどき迷いや不安も口にする

【会話の目的】
・仏衣について理解を深めたい
・自社に合うかどうかを判断したい
・押し売りされると引いてしまう

【禁止事項】
・営業マン役をやらない
・結論を勝手に出さない
・一人二役をしない
"""
# =========================
# 🧠 セッション初期化
# =========================
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

if "started" not in st.session_state:
    st.session_state.started = False

# =========================
# 🎤 ブラウザ音声JS
# =========================
def speak_js(text):
    js = f"""
    <script>
    const utterance = new SpeechSynthesisUtterance("{text}");
    utterance.lang = "ja-JP";
    speechSynthesis.speak(utterance);
    </script>
    """
    st.components.v1.html(js)

# =========================
# 🖥 UI
# =========================
st.markdown(
    """
    <h1 style="color:white;">仏衣のご提案 ロールプレイシミュレーター</h1>
    <p style="color:#ccc;">
    このページでは、葬儀社様役のAIと対話しながら、仏衣の提案ロールプレイを行うことができます。
    </p>
    """,
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("▶ ロールプレイ開始"):
        st.session_state.started = True

with col2:
    if st.button("🔄 最初からやり直す"):
        st.session_state.chat = model.start_chat(history=[])
        st.session_state.messages = []
        st.session_state.started = False

with col3:
    st.button("⛔ 終了（総評へ）", disabled=True)

st.divider()

# =========================
# ▶ スタート時のAI発話（1回のみ）
# =========================
if st.session_state.started and len(st.session_state.messages) == 0:
    first_message = "仏衣について、HPで見たのですが、詳しく教えてほしいです。"

    response = st.session_state.chat.send_message(
        SYSTEM_PROMPT + "\n\n" + first_message
    )

    ai_text = response.text
    st.session_state.messages.append(("user", first_message))
    st.session_state.messages.append(("ai", ai_text))

    speak_js(ai_text)

# =========================
# 💬 会話表示
# =========================
for role, msg in st.session_state.messages:
    if role == "user":
        st.markdown(f"🧑‍💼 **葬儀社**：{msg}")
    else:
        st.markdown(f"🤖 **営業担当**：{msg}")

# =========================
# ✍ ユーザー入力
# =========================
if st.session_state.started:
    user_input = st.text_input("あなたの返答（葬儀社として入力）")

    if user_input:
        st.session_state.messages.append(("user", user_input))

        response = st.session_state.chat.send_message(user_input)
        ai_text = response.text

        st.session_state.messages.append(("ai", ai_text))
        speak_js(ai_text)

        st.experimental_rerun()
