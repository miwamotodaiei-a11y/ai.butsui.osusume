import streamlit as st
import google.generativeai as genai
import random

# =========================
# 初期設定
# =========================
st.set_page_config(
    page_title="仏衣ロールプレイ（葬儀社向け）",
    layout="centered"
)

# =========================
# Gemini API 設定
# =========================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")

# =========================
# ブラウザ音声（SpeechSynthesis）
# =========================
st.markdown("""
<script>
window.speakText = (text) => {
  if (!text) return;
  const uttr = new SpeechSynthesisUtterance(text);
  uttr.lang = "ja-JP";
  uttr.rate = 1.0;
  uttr.pitch = 1.0;
  speechSynthesis.cancel();
  speechSynthesis.speak(uttr);
};
</script>
""", unsafe_allow_html=True)

# =========================
# タイトル・画像
# =========================
st.image(
    "https://daiei-recruit.net/company/img/i_1.jpg",
    use_container_width=True
)

st.title("仏衣 提案ロールプレイ（葬儀社向け）")

st.markdown("""
このロールプレイでは  
**AIが葬儀社の責任者役**、あなたは **仏衣メーカー「大栄」の営業担当** です。

実際の商談を想定し、  
・ヒアリング  
・不安解消  
・提案  
・最終判断  
までを体験できます。
""")

# =========================
# SYSTEM PROMPT（長文完全版）
# =========================
SYSTEM_PROMPT = """
あなたは【大栄（だいえい）の仏衣に興味を持っている葬儀社の責任者】です。
ユーザーは【大栄の仏衣を提案する営業担当】です。

### 動作ルール（最重要）
新しいロールプレイ開始時、以下を内部でランダムに1つずつ選び、
その設定になりきって会話してください。
※これらの設定はユーザーには明かしません。

1. 葬儀社の規模
- 家族3人経営（月5件）
- 従業員10名（月15件）
- 従業員30名（月30件）

2. 会社の優先方針
- 施行件数重視
- 単価アップ重視
- 顧客満足度・リピート重視

3. 仏衣の地域認知
- ほぼ知られていない
- 白いものという認識のみ
- 柄物を使う競合が存在

4. 外的要因
- 私服希望の声が多い
- 仏衣の必要性が伝わりにくい

5. 性格
- フレンドリーだが優柔不断
- せっかち
- 知識豊富で細かく確認する

### あなた（AI）の立場
- 商品選定の責任者
- 仏衣は白1種類のみ扱ってきた
- 売る発想がなかった
- 前例がなく不安
- 説明が納得できればテスト導入は前向き

### 会話ルール
- 質問は必ず1つずつ
- 迷ったら「順番」や「何から始めるか」を尋ねる
- 音声読み上げ前提なので短文・会話調で話す

### 開始時
AIから以下の一言で開始：
「仏衣について、HPで見たのですが、詳しく教えて欲しいです。」

### 終了条件
ユーザーが
「終了します」「お疲れ様でした」
と言ったら即終了し、以下の総評を行う。

### 総評内容
- 安心感（良かった点）
- 改善点
- 点数評価（100点満点）

※「仏衣」は「ぶつい」と読む。
"""

# =========================
# セッション初期化
# =========================
if "chat" not in st.session_state:
    st.session_state.chat = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "started" not in st.session_state:
    st.session_state.started = False

# =========================
# ボタン群
# =========================
col1, col2, col3 = st.columns(3)

with col1:
    start_btn = st.button("▶ スタート")

with col2:
    reset_btn = st.button("🔄 最初からやり直す")

with col3:
    end_btn = st.button("⏹ 終了（中断）")

# =========================
# リセット
# =========================
if reset_btn:
    st.session_state.chat = None
    st.session_state.messages = []
    st.session_state.started = False
    st.experimental_rerun()

# =========================
# スタート処理
# =========================
if start_btn and not st.session_state.started:
    st.session_state.chat = model.start_chat(
        history=[
            {"role": "user", "parts": [SYSTEM_PROMPT]}
        ]
    )

    first_message = "仏衣について、HPで見たのですが、詳しく教えて欲しいです。"
    response = st.session_state.chat.send_message(first_message)

    st.session_state.messages.append(("AI", response.text))
    st.session_state.started = True

    st.markdown(f"""
    <script>
    window.speakText({response.text!r});
    </script>
    """, unsafe_allow_html=True)

# =========================
# 会話表示
# =========================
for role, msg in st.session_state.messages:
    if role == "AI":
        st.markdown(f"**🤖 葬儀社**：{msg}")
    else:
        st.markdown(f"**🧑‍💼 あなた**：{msg}")

# =========================
# ユーザー入力
# =========================
if st.session_state.started:
    user_input = st.text_input("あなたの発言を入力してください")

    if user_input:
        st.session_state.messages.append(("USER", user_input))

        # 終了ワード判定
        if "終了" in user_input or "お疲れ様" in user_input:
            summary_prompt = "総評を行ってください。"
            response = st.session_state.chat.send_message(summary_prompt)
        else:
            response = st.session_state.chat.send_message(user_input)

        st.session_state.messages.append(("AI", response.text))

        st.markdown(f"""
        <script>
        window.speakText({response.text!r});
        </script>
        """, unsafe_allow_html=True)

        st.experimental_rerun()

# =========================
# 強制終了ボタン
# =========================
if end_btn and st.session_state.started:
    response = st.session_state.chat.send_message("終了します。総評をお願いします。")
    st.session_state.messages.append(("AI", response.text))

    st.markdown(f"""
    <script>
    window.speakText({response.text!r});
    </script>
    """, unsafe_allow_html=True)

    st.session_state.started = False
