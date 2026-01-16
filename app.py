import streamlit as st
from google import genai

# ===============================
# 1. ページ設定
# ===============================
st.set_page_config(
    page_title="●●社様オリジナル対話AI",
    layout="centered"
)

# ===============================
# 2. 画像・タイトル
# ===============================
char_image_url = "https://daiei-recruit.net/company/img/i_1.jpg"
st.image(char_image_url, width=150)

st.title("仏衣のご提案シミュレーター")
st.write("「仏衣って興味あるんだけど、どういうメリットがあるの？」")

# ===============================
# 3. APIキー取得（Secrets）
# ===============================
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except KeyError:
    st.error("GOOGLE_API_KEY が設定されていません。")
    st.stop()

# ===============================
# 4. Gemini クライアント生成（新SDK）
# ===============================
client = genai.Client(api_key=api_key)

# ===============================
# 5. システム指示（ロール設定）
# ===============================
SYSTEM_INSTRUCTION = """
あなたは葬儀の専門家です。
お客様の気持ちに寄り添いながら、
仏衣について無理に売り込まず、
やさしく、わかりやすく説明してください。
"""

# ===============================
# 6. チャット履歴初期化
# ===============================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ===============================
# 7. 過去メッセージ表示
# ===============================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ===============================
# 8. チャット入力
# ===============================
prompt = st.chat_input("メッセージを入力してください")

if prompt:
    # ユーザー入力を保存・表示
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Gemini 呼び出し（新方式）
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                {
                    "role": "system",
                    "parts": [{"text": SYSTEM_INSTRUCTION}]
                },
                *[
                    {
                        "role": m["role"],
                        "parts": [{"text": m["content"]}]
                    }
                    for m in st.session_state.messages
                ],
            ],
        )

        reply = response.text

        # AI応答を保存・表示
        st.session_state.messages.append(
            {"role": "assistant", "content": reply}
        )
        with st.chat_message("assistant"):
            st.markdown(reply)

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
