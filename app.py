import streamlit as st
import google.generativeai as genai

# =====================
# 初期設定
# =====================
st.set_page_config(page_title="仏衣営業ロープレ", layout="centered")

# =====================
# APIキー
# =====================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# =====================
# SYSTEM PROMPT（長文OK）
# =====================
SYSTEM_PROMPT = """
あなたは「葬儀社の担当者」です。
ユーザーは「大栄の営業マン」で、仏衣を提案してきます。

ルール：
・あなたは営業しません
・質問・懸念・比較・現場目線のツッコミを行います
・1回の発話は短すぎず、長すぎず
・会話は自然な日本語
・ランダムに反応の温度感を変えてください
・最後に「総評」は行いません（ユーザー操作時のみ）

立場：
あなた＝葬儀社
相手＝仏衣メーカー営業（大栄）
"""

# =====================
# セッション初期化
# =====================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat" not in st.session_state:
    model = genai.GenerativeModel(
        model_name="models/gemini-1.5-flash"
    )

    # ★ SYSTEM PROMPT はここでのみ渡す
    st.session_state.chat = model.start_chat(
        history=[
            {
                "role": "system",
                "parts": [SYSTEM_PROMPT]
            }
        ]
    )

# =====================
# タイトル & 画像
# =====================
st.title("仏衣 営業ロールプレイ")

st.image(
    "https://daiei-recruit.net/company/img/i_1.jpg",
    use_column_width=True
)

st.markdown("""
**想定**
- あなた：大栄の営業担当
- 相手：葬儀社の担当者（AI）

スタートを押すとロールプレイが始まります。
""")

# =====================
# スタートボタン
# =====================
if st.button("▶ スタート"):
    first_message = "それでは仏衣の件で少しお時間よろしいですか？"

    response = st.session_state.chat.send_message(first_message)

    st.session_state.messages.append(
        {"role": "assistant", "content": response.text}
    )

# =====================
# チャット表示
# =====================
for msg in st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown(msg["content"])

# =====================
# ユーザー入力
# =====================
user_input = st.chat_input("あなたの発言を入力してください")

if user_input:
    # ユーザー発話 → AI
    response = st.session_state.chat.send_message(user_input)

    st.session_state.messages.append(
        {"role": "assistant", "content": response.text}
    )

    st.rerun()

# =====================
# 音声読み上げ（ブラウザ）
# =====================
if st.session_state.messages:
    latest = st.session_state.messages[-1]["content"]

    st.components.v1.html(
        f"""
        <script>
        const msg = new SpeechSynthesisUtterance({latest!r});
        msg.lang = 'ja-JP';
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
