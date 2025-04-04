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
        st.session_state.mood_level = 2.5  # 초기 기분 수준 (0.0 - 5.0)

    # 답변 창의성 저장을 위한 세션 상태 초기화
    if "creativity" not in st.session_state:
        st.session_state.creativity = 0.7  # 초기 창의성 (0.0 - 2.0)

    # 채팅 메시지 저장을 위한 세션 상태 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 기존 채팅 메시지를 화면에 표시합니다.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    st.sidebar.title("카르디아 설정")

    # 답변의 창의성 조절 슬라이더
    st.sidebar.subheader("답변의 창의성 (0.0: 낮음, 2.0: 높음)")
    st.session_state.creativity = st.sidebar.slider(
        "창의성 수준:", min_value=0.0, max_value=2.0, value=st.session_state.creativity, step=0.1
    )
    st.sidebar.caption("낮은 값은 더 정확하고 예측 가능한 답변을, 높은 값은 더 창의적이고 무작위적인 답변을 생성합니다.")

    # 사용자 기분 수준 입력 슬라이더
    st.sidebar.subheader("현재 기분 수준 (0.0: 매우 침울, 5.0: 매우 활기)")
    st.session_state.mood_level = st.sidebar.slider(
        "기분 수준:", min_value=0.0, max_value=5.0, value=st.session_state.mood_level, step=0.1
    )
    st.sidebar.caption("이 기분 수준은 챗봇의 응답 방식에 영향을 줄 수 있습니다.")

    mood_display = st.sidebar.empty() # 기분 수준 표시를 위한 공간

    # 사용자 입력 필드를 생성합니다.
    if prompt := st.chat_input("당신의 이야기를 들려주세요"):
        # 사용자 메시지를 세션 상태에 추가하고 화면에 표시합니다.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 답변 생성 시 temperature 값 결정: 창의성 슬라이더 값 사용 (기분 수준은 다른 방식으로 활용 가능)
        temperature = st.session_state.creativity

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

        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")

    mood_display.markdown(f"**현재 기분 수준:** {st.session_state.mood_level:.1f} / 5.0 (주관적인 피드백)")

else:
    st.warning("OpenAI API 키를 입력해야 서비스를 이용할 수 있습니다.")

st.markdown(
    """
    **Disclaimer:** 카르디아는 AI 챗봇이며, 정신 건강 전문가가 아닙니다.
    만약 심리적인 어려움을 느끼신다면 전문가의 도움을 받는 것을 권장드립니다.
    """
)
