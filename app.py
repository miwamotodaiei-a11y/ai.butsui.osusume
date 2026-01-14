import streamlit as st
import google.generativeai as genai

# 1. ページのデザイン設定
st.set_page_config(page_title="●●社様オリジナル対話AI", layout="centered")

# --- 【カスタマイズ：画像】 ---
# 表示したいキャラクター画像のURLを入れてください
char_image_url = "https://daiei-recruit.net/company/img/i_1.jpg" 
st.image(char_image_url, width=150)

st.title("オリジナル対話トレーニング")
st.write("設定したキャラクターとの会話を始めましょう！")

# 2. サイドバーの設定（APIキー入力欄）
with st.sidebar:
    st.title("設定")
    api_key = st.text_input("AIzaSyCz8zepMKEZeYt28ZgEp1i781jXdDOx4xI", type="password")
    st.caption("AIzaSyCz8zepMKEZeYt28ZgEp1i781jXdDOx4xI")

# 3. AIの動作設定
if api_key:
    genai.configure(api_key=api_key)
    
    # --- 【カスタマイズ：AIへの指示】 ---
    # ここに「どんなキャラか」「どんな状況か」を自由に書いてください
    # 複数行になっても大丈夫です
    my_instruction = """
    【あなたの役割】
    ここにAIの性格や役割を書いてください。
    例：あなたは親切なカウンセラーです。
    
    【シチュエーション】
    ここにどんな場面かを書いてください。
    例：相談者が悩みを打ち明けるのを待っています。
    
    【ランダム要素の指示】
    ここがポイントです！
    「会話のたびに、以下のAかBかCのパターンをランダムに選んで、その振る舞いをして」と書くと、
    マンネリ化を防げます。
    
    【最初の第一声】
    「こんにちは、今日はどうしましたか？」といった風に始めてください。
    """
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-latest",
        system_instruction=my_instruction
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("メッセージを入力..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        response = model.generate_content(prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
else:
    st.warning("左側のサイドバーにAPIキーを入力してください。")
