import streamlit as st
from openai import OpenAI

# 페이지 제목과 설명을 설정합니다.
st.title("❤️ 카르디아: 당신의 마음을 보듬는 대화")
st.markdown(
    """
    당신의 이야기에 귀 기울이고, 따뜻한 대화를 나눌 수 있도록 돕는 AI 챗봇입니다.
    OpenAI의 GPT-3.5 모델을 기반으로 작동합니다.
    """
)
st.markdown(
    """
    **사용 방법:** OpenAI API 키를 입력하고, 편안하게 당신의 마음을 이야기해주세요.
    """
)
st.markdown(
    """
    [OpenAI API 키 발급받기](https://platform.openai.com/account/api-keys)
    """
)

# OpenAI API 키 입력 필드를 생성합니다.
openai_api_key = st.text_input("OpenAI API 키를 입력해주세요:", type="password")

if openai_api_key:
    # OpenAI 클라이언트 초기화
    client = OpenAI(api_key=openai_api_key)

    # 감정 상태 저장을 위한 세션 상태 초기화 (주관적인 피드백 활용)
    if "mood_level" not in st.session_state:
        st.session_state.mood_level = 3  # 초기 감정 수준 (1-5)

    # 채팅 메시지 저장을 위한 세션 상태 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 기존 채팅 메시지를 화면에 표시합니다.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    st.sidebar.title("카르디아 설정")
    mood_display = st.sidebar.empty() # 감정 수준 표시를 위한 공간

    # 사용자 입력 필드를 생성합니다.
    if prompt := st.chat_input("당신의 이야기를 들려주세요"):
        # 사용자 메시지를 세션 상태에 추가하고 화면에 표시합니다.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 현재 감정 수준에 따라 temperature 조절 (간접적인 영향)
        temperature = (st.session_state.mood_level - 1) * 0.4 + 0.2 # 1->0.2, 3->1.0, 5->1.8

        try:
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
                temperature=temperature,
            )
            with st.chat_message("assistant"):
                response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})

            # 답변 후 감정 상태 업데이트를 위한 UI 표시 (주관적인 피드백)
            st.sidebar.subheader("오늘 기분은 어떠신가요?")
            col1, col2, col3, col4, col5 = st.sidebar.columns(5)
            if col1.button("😔"):
                st.session_state.mood_level = 1
            if col2.button("🙁"):
                st.session_state.mood_level = 2
            if col3.button("😐"):
                st.session_state.mood_level = 3
            if col4.button("😊"):
                st.session_state.mood_level = 4
            if col5.button("😄"):
                st.session_state.mood_level = 5

        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")

    mood_display.markdown(f"**현재 감정 수준:** {st.session_state.mood_level} / 5 (주관적인 피드백)")

else:
    st.warning("OpenAI API 키를 입력해야 서비스를 이용할 수 있습니다.")

st.markdown(
    """
    **Disclaimer:** 카르디아는 AI 챗봇이며, 정신 건강 전문가가 아닙니다. 
    만약 심리적인 어려움을 느끼신다면 전문가의 도움을 받는 것을 권장드립니다.
    """
)
