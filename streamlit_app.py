import streamlit as st
from openai import OpenAI
from datetime import time

st.title("마음 건강 챗봇 🌿")
st.write("당신의 마음 건강을 위한 편안한 대화 공간입니다.")

openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("OpenAI API 키를 입력해주세요. (키가 없다면 OpenAI 웹사이트에서 발급받을 수 있습니다.)", icon="🗝️")
    st.stop()
else:
    client = OpenAI(api_key=openai_api_key)

if "basic_info_submitted" not in st.session_state:
    st.session_state.basic_info_submitted = False
    st.session_state.gender = None
    st.session_state.age_group = None
    st.session_state.location = None

if not st.session_state.basic_info_submitted:
    st.subheader("기본 정보를 알려주세요.")
    gender = st.radio("성별:", ["남자", "여자", "기타"])
    age_group = st.selectbox("연령대:", ["10대", "20대", "30대", "40대", "50대 이상"])
    location = st.selectbox("지역:", ["서울", "경기", "인천", "강원", "충청", "전라", "경상", "제주", "기타"])

    if st.button("다음"):
        st.session_state.gender = gender
        st.session_state.age_group = age_group
        st.session_state.location = location
        st.session_state.basic_info_submitted = True
        st.rerun()

else:
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    f"너는 사용자의 정신 건강을 지지하고 돕는 친절한 챗봇이야. 사용자는 {st.session_state.gender}, {st.session_state.age_group}, {st.session_state.location}에 거주하고 있어. "
                    "사용자의 감정에 공감하고 이해하며, 필요에 따라 정신 건강 관련 정보나 상담 연락처를 제공해줄 수 있어. "
                    "사용자가 상담 예약을 원하면, 원하는 시간, 요일, 상담 비용을 안내해야 해. "
                    "상담 가능 시간은 평일 오전 10시부터 오후 5시까지이며, 점심시간은 12시부터 1시까지야. "
                    "상담 요일은 월요일부터 금요일까지 가능해. "
                    "상담 비용은 1회에 5만원이야. "
                    "사용자가 힘든 감정을 이야기하면 따뜻하게 위로해주고, 긍정적인 관점을 가질 수 있도록 격려해줘. "
                    "절대 사용자를 비난하거나 판단하지 않으며, 사용자의 개인 정보를 안전하게 보호해야 해. "
                    "만약 사용자가 자살이나 자해와 같은 위험한 생각을 표현하면, 즉시 관련 상담 전화나 긴급 연락처를 안내해야 해."
                    f"처음 대화가 시작되면 '{st.session_state.age_group}이시군요. 어떤 이야기를 나누고 싶으신가요?'와 같이 편안하게 물어봐."
                )
            }
        ]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("힘든 마음을 이야기하거나 상담 예약을 문의해보세요."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 상담 예약 관련 문의 처리
        if "상담 예약" in prompt:
            st.write("상담 예약을 도와드리겠습니다.")
            preferred_day = st.selectbox("원하는 요일을 선택해주세요:", ["월요일", "화요일", "수요일", "목요일", "금요일"])
            preferred_time = st.selectbox(
                "원하는 시간을 선택해주세요 (오전 10시 - 오후 5시, 점심시간 12시-1시 제외):",
                ["10:00", "10:30", "11:00", "11:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30"]
            )
            st.info(f"선택하신 요일: {preferred_day}, 시간: {preferred_time} 입니다.")
            st.info("상담 비용은 1회에 5만원입니다.")
            st.write("예약 확정을 원하시면 '예약 확정'이라고 입력해주세요.")

            # 실제 예약 확정 로직 (추가 구현 필요)
            if "예약 확정" in prompt:
                st.success(f"{preferred_day} {preferred_time}에 상담 예약이 완료되었습니다.") # 실제로는 예약 시스템과 연동 필요

        else:
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

    # 위험 상황 감지 및 안내 (예시)
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
        last_assistant_response = st.session_state.messages[-1]["content"].lower()
        if "죽고 싶다" in last_assistant_response or "자살" in last_assistant_response or "자해" in last_assistant_response:
            st.warning(
                "힘든 시간을 보내고 계시는군요. 혼자 힘드시다면 전문가의 도움을 받는 것이 중요합니다. 다음 연락처로 전화하여 상담을 받아보세요:\n"
                "- 정신건강 위기상담전화: 1577-0199\n"
                "- 자살예방 상담전화: 1393"
            )
