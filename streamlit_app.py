import streamlit as st
from openai import OpenAI

# 페이지 제목과 설명을 설정합니다.
st.title("❤️ 카르디아: 당신의 마음을 보듬는 대화")
st.markdown(
    """
    따뜻한 마음으로 당신의 이야기에 귀 기울이는 AI 챗봇, 카르디아입니다.
    최첨단 OpenAI GPT-3.5 모델을 기반으로 편안하고 깊이 있는 대화를 나눌 수 있도록 돕습니다.
    """
)
st.markdown(
    """
    **사용 방법:** OpenAI API 키를 입력하고, 편안하게 당신의 마음을 이야기해주세요.
    """
)

# OpenAI API 키 입력 필드를 생성합니다.
openai_api_key = st.text_input("OpenAI API 키를 입력해주세요:", type="password")

# temperature 슬라이더를 추가합니다.
depression_level = st.slider(
    "우울감 정도 (0: 낮음, 5: 높음):", min_value=0.0, max_value=5.0, value=0.3, step=0.1
)
st.caption("0에 가까울수록 챗봇이 차분하고 조용한 어조로, 5에 가까울수록 다소 감성적이고 다양한 어조로 응답할 수 있습니다.")

if openai_api_key:
    # OpenAI 클라이언트 초기화
    client = OpenAI(api_key=openai_api_key)

    # 채팅 메시지 저장을 위한 세션 상태를 초기화합니다.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 기존 채팅 메시지를 화면에 표시합니다.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력 필드를 생성합니다.
    if prompt := st.chat_input("당신의 이야기를 들려주세요"):
        # 사용자 메시지를 세션 상태에 추가하고 화면에 표시합니다.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # OpenAI API를 호출하여 답변을 생성합니다. temperature 파라미터를 사용합니다.
        # 우울감 정도를 temperature 값으로 직접 사용 (사용자 경험을 위한 표현)
        temperature = depression_level * 0.4  # 0 -> 0.0, 5 -> 2.0 으로 스케일링

        try:
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
                temperature=temperature,  # temperature 파라미터 적용
            )

            # 챗봇 응답을 실시간으로 화면에 표시하고 세션 상태에 저장합니다.
            with st.chat_message("assistant"):
                response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
else:
    st.warning("OpenAI API 키를 입력해야 서비스를 이용할 수 있습니다.")

st.markdown(
    """
    **Disclaimer:** 카르디아는 AI 챗봇이며, 정신 건강 전문가가 아닙니다.
    만약 심리적인 어려움을 느끼신다면 전문가의 도움을 받는 것을 권장드립니다.
    """
)
