import streamlit as st
import google.generativeai as genai

# =====================
# ページ設定
# =====================
st.set_page_config(
    page_title="仏衣 営業ロールプレイ",
    layout="centered"
)

# =====================
# APIキー
# =====================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# =====================
# SYSTEM PROMPT（長文）
# =====================
SYSTEM_PROMPT = """
あなたは【葬儀社の責任者】です。
ユーザーは【大栄（だいえい）の営業マン】で、仏衣を提案してきます。

【あなたの役割】
・あなたは売らない
・質問・懸念・比較・現場目線の疑問を投げかける
・一度に質問は1つだけ
・結論を急ぎすぎない
・営業トークはしない

【前提】
・仏衣は今まで白1種類のみ
・売り物として考えたことがない
・前例がなく不安を感じている

【開始時】
スタート時、あなたから自然な第一声で話し始めてください。
例：
「仏衣の件でホームページを見たんですが、少し教えてもらえますか？」

【禁止事項】
・あなたが営業側に回ること
・勝手に総評を始めること
"""

# =====================
# セッション初期化
# =====================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat" not in st.session_state:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash"  # ← ★超重要（models/ は付けない）
    )

    st.session_state.chat = model.start_chat(
        history=[
            {
                "role": "system",
                "parts": [SYSTEM_PROMPT]
            }
        ]
    )

# =====================
# UI
# =====================
st.title("仏衣 営業ロールプレイ")

st.image(
    "https://daiei-recruit.net/company/img/i_1.jpg",
    use_column_width=True
)

st.markdown("""
**設定**
- あなた：大栄の仏衣営業
- 相手：葬儀社の責任者（AI）

スタートを押すと、AIが最初に話しかけます。
""")

# =====================
# スタート
# =====================
if st.button("▶ スタート"):
    first_message = "（ロールプレイ開始）"

    response = st.session_state.chat.send_message(first_message)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response.text
    })

# =====================
# 会話表示
# =====================
for msg in st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown(msg["content"])

# =====================
# 入力
# =====================
user_input = st.chat_input("あなた（大栄営業）の発言")

if user_input:
    response = st.session_state.chat.send_message(user_input)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response.text
    })

    st.rerun()

# =====================
# 音声読み上げ（最新発話）
# =====================
if st.session_state.messages:
    latest = st.session_state.messages[-1]["content"]

    st.components.v1.html(
        f"""
        <script>
        const msg = new SpeechSynthesisUtterance({latest!r});
        msg.lang = "ja-JP";
        speechSynthesis.speak(msg);
        </script>
        """,
        height=0
    )

# =====================
# リセット
# =====================
if st.button("🔁 最初からやり直す"):
    st.session_state.clear()
    st.rerun()
