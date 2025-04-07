import streamlit as st
import os
from openai import OpenAI

# ---------------------
# 🎯 챗봇 소개
# ---------------------
st.markdown("""
### 💖 힘겨운 시간을 보내고 계신가요? **보듬이**가 당신의 마음을 보듬어 드릴게요. 💖

암 진단과 치료 과정에서 겪는 우울감은 혼자만의 문제가 아니에요. 많은 분들이 어려움을 느끼고 있으며, 적절한 이해와 지지가 있다면 충분히 극복할 수 있습니다.

이 챗봇은 당신의 감정을 이해하고, 필요한 정보와 도움을 드릴 수 있도록 만들어졌습니다. 편안하게 당신의 이야기를 들려주세요.
""")

# ---------------------
# 🔑 API 키 입력
# ---------------------
openai_api_key = st.text_input("🔐 OpenAI API Key를 입력하세요", type="password")
if not openai_api_key:
    st.info("API 키를 입력하시면 챗봇을 사용할 수 있어요!", icon="🔑")
    st.stop()
else:
    os.environ["OPENAI_API_KEY"] = openai_api_key
    client = OpenAI()

# ---------------------
# 💬 이전 대화 불러오기
# ---------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------
# 💬 자유 질문 입력
# ---------------------
if prompt := st.chat_input("지금 당신의 기분이나 힘든 점을 이야기해주세요."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        with st.chat_message("assistant"):
            response = st.write_stream(stream)

        st.session_state.messages.append({"role": "assistant", "content": response})

        # 추가적인 안내 또는 정보 제공 (예시)
        if "힘들어요" in prompt or "우울해요" in prompt:
            st.markdown("혼자가 아니에요. 많은 분들이 비슷한 감정을 느낍니다. 잠시 숨을 쉬고, 당신의 감정을 천천히 이야기해보세요.")
            st.markdown("필요하다면 전문가의 도움을 받는 것도 좋은 방법입니다. 정신건강의학과 상담이나 심리 상담을 고려해보세요.")
            st.markdown("**도움이 될 수 있는 연락처:**")
            st.markdown("- 정신건강 상담전화: 1577-0199")
            st.markdown("- 희망의 전화: 1393")

        elif "어떻게 해야 할지 모르겠어요" in prompt:
            st.markdown("막막한 기분이 드시나요? 작은 것부터 시작해보는 건 어떨까요? 예를 들어, 따뜻한 물을 마시거나, 짧게 산책을 하는 것도 도움이 될 수 있습니다.")

    except Exception as e:
        st.error(f"에러가 발생했어요: {e}")
