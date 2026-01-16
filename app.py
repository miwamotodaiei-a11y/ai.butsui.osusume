import streamlit as st
import google.generativeai as genai

# ===============================
# 1. ページ設定
# ===============================
st.set_page_config(
    page_title="●●社様オリジナル対話AI",
    layout="centered"
)

# ===============================
# 2. 画像・タイトル表示
# ===============================
char_image_url = "https://daiei-recruit.net/company/img/i_1.jpg"
st.image(char_image_url, width=150)

st.title("仏衣のご提案シミュレーター")
st.write("「仏衣って興味あるんだけど、どういうメリットがあるの？」")

# ===============================
# 3. サイドバー（設定）
# ===============================
with st.sidebar:
    st.title("設定")
    st.write("このページは仏衣のご提案ロールプレイング用AIです。")

# ===============================
# 4. APIキー設定（Secrets使用）
# ===============================
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except KeyError:
    st.error("GOOGLE_API_KEY が設定されていません。")
    st.stop()

genai.configure(api_key=api_key)

# ===============================
# 5. AIモデル設定
# ===============================
instruction = """
あなたは葬儀の専門家です。
お客様の気持ちに寄り添いながら、仏衣について
・無理に売り込まず
・やさしく
・わかりやすく
メリットや考え方を説明してください。
"""

model = genai.GenerativeModel(
    model_name="models/gemini-1.5-pro",
    system_instruction=instruction
)

# ===============================
# 6. チャットセッション初期化
# ===============================
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# ===============================
# 7. 過去の会話表示
# ===============================
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# ===============================
# 8. チャット入力
# ===============================
prompt = st.chat_input("メッセージを入力してください")

if prompt:
    # ユーザー発言表示
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # AI応答
        response = st.session_state.chat_session.send_message(prompt)

        with st.chat_message("assistant"):
            st.markdown(response.text)

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
        st.info(
            "モデル名やライブラリのバージョンをご確認ください。\n"
            "必要であれば `pip install -U google-generativeai` を実行してください。"
        )
