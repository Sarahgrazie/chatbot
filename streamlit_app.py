import streamlit as st
import os
from openai import OpenAI

# ---------------------
# 🎯 장소별 이미지 & 설명 사전
# ---------------------
place_images = {
    "오페라 하우스": {
        "image": "https://upload.wikimedia.org/wikipedia/commons/4/40/Sydney_Opera_House_Sails.jpg",
        "desc": "시드니의 랜드마크! 독특한 지붕 디자인으로 세계적으로 유명한 공연 예술 공간이에요."
    },
    "하버 브리지": {
        "image": "https://upload.wikimedia.org/wikipedia/commons/b/bb/Sydney_Harbour_Bridge_night.jpg",
        "desc": "시드니 항구를 잇는 거대한 철제 아치형 다리. 도보로 건널 수도 있어요!"
    },
    "본다이 비치": {
        "image": "https://upload.wikimedia.org/wikipedia/commons/5/5a/Bondi_Beach_aerial.jpg",
        "desc": "서핑, 산책, 여유로운 하루 보내기에 완벽한 아름다운 해변이에요."
    },
    "타롱가 동물원": {
        "image": "https://upload.wikimedia.org/wikipedia/commons/4/41/Taronga_Zoo_skyline.jpg",
        "desc": "코알라, 캥거루를 직접 볼 수 있는 시드니 최고의 동물원!"
    },
    "블루마운틴": {
        "image": "https://upload.wikimedia.org/wikipedia/commons/4/47/Three_Sisters_BM_NSW_Australia.jpg",
        "desc": "장엄한 자연 절경과 '세 자매 바위'로 유명한 국립공원. 당일치기 여행으로 인기!"
    }
}

# ---------------------
# 🏝️ 문도리 스타일 소개
# ---------------------
st.markdown("""
### 🐨🦘 귀여운 문도리와 함께하는 호주 시드니 여행 🦘🐨  

GPT-3.5를 기반으로 여행지에서 보다 즐겁고 풍성한 시간을 보내실 수 있도록 안내해 드립니다. 

지금 바로 시드니 여행을 시작해볼까요? 🌏✈️
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
# ✈️ 여행 정보 입력
# ---------------------
travel_days = st.slider("⏳ 여행은 며칠 예정인가요?", 1, 14, 4)

with st.expander("🎒 여행 스타일 선택"):
    travel_styles = st.multiselect(
        "복수 선택 가능!",
        ["맛집 탐방", "자연 힐링", "문화 체험", "사진 찍기", "쇼핑", "혼자 여행", "가족 여행", "커플 여행"]
    )

# ---------------------
# 💬 이전 대화 불러오기
# ---------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------
# 🗺️ GPT로 여행 일정 추천
# ---------------------
if st.button("🗺️ 나만의 여행 일정 추천받기"):
    if not travel_styles:
        st.warning("여행 스타일을 최소 1개 이상 선택해주세요!")
    else:
        user_prompt = f"""
        저는 {travel_days}일 동안 시드니 여행을 할 예정입니다.
        여행 스타일은 {', '.join(travel_styles)} 입니다.
        이 스타일에 맞는 여행 일정과 추천 장소를 알려주세요.
        """

        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

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

            # 🔍 GPT 응답 중 장소 이름 포함된 것 찾기
            for place, data in place_images.items():
                if place in response:
                    st.image(data["image"], caption=place, use_container_width=True)
                    st.markdown(f"📝 {data['desc']}")

        except Exception as e:
            st.error(f"에러가 발생했어요: {e}")

# ---------------------
# 💬 자유 질문 입력
# ---------------------
if prompt := st.chat_input("시드니 여행이 궁금한가요? 자유롭게 질문해보세요!"):
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

        for place, data in place_images.items():
            if place in response:
                st.image(data["image"], caption=place, use_column_width=True)
                st.markdown(f"📝 {data['desc']}")

    except Exception as e:
        st.error(f"에러가 발생했어요: {e}")
