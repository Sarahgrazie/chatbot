import streamlit as st
from openai import OpenAI

# 페이지 제목과 설명을 설정합니다.
st.title("✈️ K의 스마트 여행 가이드")
st.markdown(
    """
    AI 기반의 맞춤형 여행 가이드 서비스입니다. 
    OpenAI의 GPT-3.5 모델을 활용하여 여행 계획, 정보 검색 등 다양한 도움을 드립니다.
    """
)
st.markdown(
    """
    **사용 방법:** OpenAI API 키를 입력하고, 궁금한 여행 관련 질문을 입력하세요.
    """
)
st.markdown(
    """
    [OpenAI API 키 발급받기](https://platform.openai.com/account/api-keys)
    """
)

# OpenAI API 키 입력 필드를 생성합니다.
openai_api_key = st.text_input("OpenAI API 키를 입력해주세요:", type="password")

# temperature 슬라이더를 추가합니다.
temperature = st.slider(
    "답변의 창의성 (Temperature):", min_value=0.0, max_value=2.0, value=0.7, step=0.1
)
st.caption("낮은 값은 더 정확하고 예측 가능한 답변을, 높은 값은 더 창의적이고 무작위적인 답변을 생성합니다.")

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
    if prompt := st.chat_input("여행에 대해 궁금한 점을 물어보세요"):
        # 사용자 메시지를 세션 상태에 추가하고 화면에 표시합니다.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # OpenAI API를 호출하여 답변을 생성합니다. temperature 파라미터를 사용합니다.
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
