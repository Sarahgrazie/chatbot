import streamlit as st
from openai import OpenAI

# 화면 제목과 서비스 설명을 표시합니다.
st.title("💬 K의 여행 가이드 서비스")
st.write(
    "OpenAI의 GPT-3.5 모델을 활용하여 답변을 생성하는 간단한 챗봇입니다. "
     "어서오세요! 평범한 챗봇과는 차원이 다른, 당신만을 위한 맞춤형 여행 경험을 선사합니다. K의 여행 가이드 서비스는 최첨단 AI 기술인 OpenAI의 GPT-3.5 모델을 기반으로, 당신의 모든 여행 관련 질문에 명확하고 창의적인 답변을 제공합니다."
     "더 이상 복잡한 정보 검색에 시간을 낭비하지 마세요. K의 여행 가이드 서비스는 당신이 꿈꾸는 완벽한 여행을 현실로 만들어 줄 여정을 안내합니다."
  
)

# 사용자로부터 OpenAI API 키를 입력받는 텍스트 입력 필드를 생성합니다.
# `type="password"` 설정을 통해 입력 내용이 가려지도록 합니다.
openai_api_key = st.text_input("OpenAI API 키를 입력해주세요", type="password")

# OpenAI API 키가 입력되지 않았을 경우, 안내 메시지를 표시합니다.
if not openai_api_key:
    st.info("OpenAI API 키를 입력하여 서비스를 이용해주세요. 🗝️")
else:
    # OpenAI 클라이언트를 생성합니다. API 키를 사용하여 인증합니다.
    client = OpenAI(api_key=openai_api_key)

    # 채팅 메시지 목록을 저장하기 위한 세션 상태 변수를 초기화합니다.
    # 세션 상태는 앱이 다시 실행되어도 값을 유지합니다.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 저장된 채팅 메시지들을 화면에 표시합니다.
    # 각 메시지는 역할("user" 또는 "assistant")에 따라 다른 스타일로 표시됩니다.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자로부터 채팅 메시지를 입력받는 입력 필드를 생성합니다.
    # 사용자가 메시지를 입력하고 Enter 키를 누르면 `prompt` 변수에 내용이 저장됩니다.
    if prompt := st.chat_input("궁금한 여행 정보를 입력해주세요"):

        # 사용자의 입력(프롬프트)을 세션 상태의 메시지 목록에 추가하고 화면에 표시합니다.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # OpenAI API를 사용하여 챗봇의 응답을 생성합니다.
        # `gpt-3.5-turbo` 모델을 사용하며, 이전 대화 내용을 함께 전달하여 맥락을 유지합니다.
        # `stream=True` 설정을 통해 응답을 실시간으로 받아 화면에 표시할 수 있습니다.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # 챗봇의 응답을 실시간으로 화면에 표시하고, 세션 상태에 저장합니다.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
