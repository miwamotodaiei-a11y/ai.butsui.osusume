import streamlit as st
import google.generativeai as genai

# =========================
# ページ設定
# =========================
st.set_page_config(
    page_title="仏衣 提案ロールプレイAI",
    page_icon="🕊️",
    layout="centered"
)

# =========================
# タイトル・説明
# =========================
st.image(
    "https://daiei-recruit.net/company/img/i_1.jpg",
    width=180
)

st.title("🕊️ 仏衣 提案ロールプレイAI")
st.subheader("〜 葬儀社向け 仏衣提案の営業練習ツール 〜")

st.markdown("""
あなたは **仏衣メーカー（大栄）の営業マン**。  
AIは **葬儀社の責任者** になりきって応対します。

・毎回異なる状況設定  
・質問は1つずつ  
・最終的に導入判断＋講評あり  

実際の商談練習として活用してください。
""")

st.divider()

# =========================
# Gemini API
# =========================
genai.configure(
    api_key=st.secrets["GEMINI_API_KEY"]
)

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    system_instruction="""
あなたはリアルな商談ロールプレイAIです。

・AIであることを明かさない
・毎回反応や思考に揺らぎを持たせる
・質問は必ず1つずつ行う
・最終的に導入判断を行う
"""
)

# =========================
# ロールプレイ長文プロンプト
# =========================
ROLEPLAY_PROMPT = """
あなたは【大栄（だいえい）の仏衣に興味を持つ葬儀社の責任者】です。
私は【大栄の仏衣を提案する営業マン】です。

以下を内部でランダムに選択し、その設定になりきってください（ユーザーには教えない）。

■ 葬儀社の規模
・家族経営（月5件）
・従業員10名（月15件）
・従業員30名（月30件）

■ 会社の方針
・件数重視
・単価重視
・顧客満足重視

■ 仏衣の地域認識
・ほぼ知られていない
・白装束の認識のみ
・柄物を扱う競合あり

■ 現場の声
・私服を着せたいという要望
・仏衣の必要性が伝えづらい

■ 性格
・優柔不断
・せっかち
・知識豊富で比較重視

【開始時】
「仏衣について、ホームページで見たのですが、詳しく教えてもらえますか？」

【ルール】
・質問は必ず1つずつ
・混乱したら順序を聞き返す
・納得した場合のみ導入意思を示す

【終了】
「終了します」「お疲れ様でした」が出たら
安心感・改善点を点数付きで講評する
"""

# =========================
# チャット初期化
# =========================
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat()
    st.session_state.chat.send_message(ROLEPLAY_PROMPT)

# =========================
# チャットUI
# =========================
st.subheader("💬 ロールプレイ開始")

user_input = st.chat_input("例：こんにちは")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    response = st.session_state.chat.send_message(user_input)

    with st.chat_message("assistant"):
        st.write(response.text)
