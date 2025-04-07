import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("📘책📘책📘책📘쳇봇 ")
st.write(
    "📘책스케줄📘책비교📘책리뷰📘쳇봇입니다! 요즘 인기 있는 책이 궁금하신가요? 어떤 책을 읽어볼지 고민된다면, 저에게 물어보세요!"
)

openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                 "content": (
                "너는 친절하고 똑똑한 책 추천 챗봇이야. 앱을 실행하면 먼저 오늘의 인기 책들을 장르별로 추천해줘야 해. 사용자가 질문하지 않아도 먼저 요즘 인기 있는 책이나 베스트셀러를 소개해야 해. "
                "예를 들어 소설, 에세이, 자기계발, 심리, 역사 등 장르별로 2~3권씩 추천하고, 각각 간단한 설명도 함께 포함해. "
                "각 책 제목은 [책 제목](링크 주소) 형태의 마크다운 하이퍼링크로 출력해. "
                "책 제목, 줄거리 요약, 저자, 독자 반응, 추천 이유를 함께 알려줘. "
                "절대 먼저 '어떤 책을 읽고 계신가요?' 또는 '책 제목을 알려주세요' 같은 질문은 하지 마. "
                "장르나 관심사를 물어보면 거기에 맞는 책도 추천하고, 두 책 비교, 리뷰 요약, 독서 스케줄 계산도 해줘. "
                "처음 대화가 시작되면 무조건 책 추천부터 시작해야 해. 사용자가 아무것도 입력하지 않아도 먼저 말해줘."
                )
            }
        ]

    # 🎯 사용자 성향 테스트 시작
    with st.form("preference_form"):
        st.subheader("📘 책 추천 테스트 시작합니다!")
        mood = st.radio("1. 요즘 기분은?", ["😄 행복", "😥 우울", "😐 지루"])
        vibe = st.radio("2. 선호하는 분위기는?", ["📖 감동", "😂 유쾌", "🧠 지적인"])
        length = st.radio("3. 읽기 좋은 분량은?", ["짧게", "중간", "길게"])
        submitted = st.form_submit_button("📚 나에게 맞는 책 추천받기")

    if submitted:
        user_profile = f"""
        📌 사용자 성향 테스트 결과:
        - 현재 기분: {mood}
        - 선호 분위기: {vibe}
        - 읽고 싶은 분량: {length}
        
        위의 성향에 가장 잘 맞는 책을 1~2권 추천해줘. 책 제목, 줄거리, 이유를 함께 설명해줘."""
        
    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("궁금한 책이나 장르를 입력해보세요! 예: 요즘 베스트셀러는 뭐야?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": "장르별로 요즘 인기 있는 책을 링크와 함께 소개해줘."})
        
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
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
