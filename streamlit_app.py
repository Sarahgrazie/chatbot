# streamlit_app.py

import streamlit as st
from datetime import datetime, timedelta
from openai import OpenAI
import json
import os
import pandas as pd

# ✅ OpenAI API 설정 (본인 API 키 입력)
client = OpenAI(api_key="")

# ✅ 페이지 설정
st.set_page_config(page_title="하이닥봇 - 병원 예약 챗봇", page_icon="🤖", layout="centered")

# ✅ 상단 로고 및 안내
st.markdown("""
<style>
.title {
    font-size: 38px;
    font-weight: bold;
    text-align: center;
    color: #2C3E50;
    margin-bottom: 10px;
}
.sub {
    text-align: center;
    font-size: 17px;
    color: #7F8C8D;
}
.section {
    margin-top: 30px;
    padding: 20px;
    border-radius: 12px;
    background-color: #F9FAFB;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
</style>

<div class="title">🤖 하이닥봇</div>
<div class="sub">병원 예약, 클릭 또는 말 한마디로 쉽게 완료하세요!</div>
""", unsafe_allow_html=True)

# ✅ 1. 자연어 기반 예약 요청
예약GPT = {}  # 기본값 미리 초기화

with st.expander("💬 자연어로 대화하며 예약하기", expanded=False):
    if "step" not in st.session_state:
        st.session_state.step = 0
        st.session_state.예약정보 = {}
        st.session_state.chat_history = []

    user_input = st.chat_input("예: 치과요 → 이번 주 금요일 오전 10시요 → 홍길동, 010-1234-5678")

    for msg in st.session_state.chat_history:
        st.chat_message(msg["role"]).write(msg["content"])

    if user_input:
        st.chat_message("user").write(user_input)
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        step = st.session_state.step
        info = st.session_state.예약정보

        if step == 0:
            info["진료과"] = user_input
            msg = f"{user_input} 예약 좋습니다. 언제로 예약하시겠어요? (예: 4월 6일 오후 3시)"
            st.session_state.step = 1

        elif step == 1:
            info["예약일시"] = user_input
            msg = "예약자 성함과 연락처를 알려주세요. (예: 홍길동, 010-1234-5678)"
            st.session_state.step = 2

        elif step == 2:
            try:
                이름, 연락처 = [x.strip() for x in user_input.split(",")]
                info["성함"] = 이름
                info["연락처"] = 연락처

                # 예약 저장
                예약기록 = {
                    "예약일시": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "진료과": info['진료과'],
                    "예약날짜": info['예약일시'].split()[0] if ' ' in info['예약일시'] else info['예약일시'],
