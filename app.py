import streamlit as st
import plotly.graph_objects as go
import time
import random
import datetime

# ==========================================
# [1. 시스템 설정 및 디자인]
# ==========================================
st.set_page_config(
    page_title="IMD 프리미엄 매칭",
    page_icon="💍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 프리미엄 CSS (수정본: 텍스트 컬러 강제 지정 & 버튼 확대)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    /* 메인 배경색 */
    .stApp {
        background-color: #f0f2f5;
        color: #333;
    }

    /* 사이드바 스타일 */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e0e0e0;
    }

    /* 헤더 스타일 */
    .main-header {
        text-align: center;
        padding: 30px 0 30px 0;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 30px;
    }
    .main-title {
        font-size: 2.2rem;
        font-weight: 900;
        color: #1a237e; /* 딥 네이비 */
        letter-spacing: -1px;
        margin-bottom: 5px;
    }
    .sub-title {
        font-size: 1rem;
        color: #555;
        font-weight: 400;
    }

    /* 입력 폼 컨테이너 */
    .form-container {
        background-color: #ffffff;
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border: 1px solid #eaeaea;
    }

    /* 섹션 타이틀 */
    .section-title {
        font-size: 1.3rem;
        font-weight: 800;
        color: #1a237e;
        margin-bottom: 25px;
        border-bottom: 2px solid #1a237e;
        padding-bottom: 10px;
        display: inline-block;
    }

    /* ★ 중요 수정: 입력창 라벨 텍스트 색상 강제 변경 (안보임 해결) ★ */
    .stMarkdown p, .stRadio label, .stSelectbox label, .stTextInput label {
        color: #333333 !important; /* 진한 회색으로 강제 */
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    
    /* 라디오 버튼 텍스트 색상 */
    div[role="radiogroup"] label p {
        color: #333333 !important;
        font-weight: 500 !important;
    }

    /* 버튼 스타일 대폭 수정 (박스 크기 확대) */
    .stButton > button {
        background: linear-gradient(135deg, #1a237e 0%, #0d47a1 100%);
        color: #fff !important;
        border: none;
        padding: 20px 0 !important; /* 높이 키움 */
        font-size: 1.3rem !important; /* 글자 키움 */
        font-weight: 800 !important;
        border-radius: 12px !important;
        width: 100%;
        box-shadow: 0 10px 20px rgba(26, 35, 126, 0.2);
        transition: all 0.3s ease;
        margin-top: 20px;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 30px rgba(26, 35, 126, 0.3);
        background: linear-gradient(135deg, #283593 0%, #1565c0 100%);
    }
    
    /* 인풋 필드 디자인 */
    .stSelectbox > div > div {
        background-color: #f8f9fa;
        border: 1px solid #ddd;
        border-radius: 8px;
        color: #333;
    }
    .stTextInput > div > div > input {
        background-color: #f8f9fa;
        border: 1px solid #ddd;
        border-radius: 8px;
        color: #333;
    }

    /* 결과 리포트 스타일 */
    .result-card {
        background: #fff;
        border: 1px solid #d4af37;
        border-radius: 10px;
        padding: 30px;
        margin-top: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }

    /* 챗봇 메시지 */
    .bot-msg {
        background-color: #f8f9fa;
        border-left: 4px solid #1a237e;
        padding: 20px;
        border-radius: 0 10px 10px 0;
        margin-bottom: 15px;
        line-height: 1.7;
        font-size: 1rem;
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# [2. 사이드바 (더미 메뉴)]
# ==========================================
with st.sidebar:
    # 로고 대신 텍스트 로고 사용
    st.markdown("<h2 style='color:#1a237e; text-align:center;'>IMD 결혼정보</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    menu_options = [
        "💘 이상형 진단",
        "💞 연애 스타일 진단",
        "🧠 결혼 심리 진단",
        "📊 내 결혼 점수/등급",
        "🔄 재혼 가능성 진단",
        "💰 가입비 산출 계산기"
    ]
    
    for menu in menu_options:
        if st.button(menu, use_container_width=True, key=menu):
            st.toast(f"'{menu}' 서비스는 준비 중입니다.", icon="🚧")
    
    st.markdown("---")
    st.markdown("""
    <div style='font-size: 0.8rem; color: #666; text-align: center;'>
        <strong>고객센터</strong><br>
        1588-0000<br>
        (평일 09:00 ~ 18:00)
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# [3. 데이터 및 로직]
# ==========================================

# 드롭다운 데이터 리스트
years = [f"{y}년생" for y in range(1950, 2016)]
jobs = [
    "선택해 주세요.", "일반사무직", "기업 임원", "공무원", "전문직(의료)", 
    "전문직(법률)", "전문직(기술)", "자영업", "기업 경영", "프리랜서", "기타"
]
educations = [
    "선택해 주세요.", "고등학교졸", "전문대졸", "대졸", "대학원졸", "박사이상", "기타"
]
regions = [
    "선택해 주세요.", "서울", "경기", "인천", "대전", "대구", "부산", "광주", "울산", "세종", "강원", "충북", "충남", "전북", "전남", "경북", "경남", "제주", "해외"
]

# 세션 상태
if 'page' not in st.session_state: st.session_state.page = 'input'
if 'user_info' not in st.session_state: st.session_state.user_info = {}

# ==========================================
# [4. 메인 화면 로직]
# ==========================================

# 헤더 출력
st.markdown("""
<div class='main-header'>
    <div class='main-title'>IMD 프리미엄 매칭 진단</div>
    <div class='sub-title'>15만 건의 성혼 데이터가 분석하는 귀하의 <b>결혼 점수</b>와 <b>최적의 상대</b></div>
</div>
""", unsafe_allow_html=True)

# --- [페이지 1: 정보 입력 폼] ---
if st.session_state.page == 'input':
    
    with st.container():
        st.markdown("<div class='form-container'>", unsafe_allow_html=True)
        
        # 섹션 1: 기본 인적사항
        st.markdown("<div class='section-title'>01. 기본 인적사항</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("이름 *", placeholder="실명을 입력해주세요")
        with col2:
            gender = st.radio("성별 *", ["여성", "남성"], horizontal=True)
        
        col3, col4 = st.columns(2)
        with col3:
            birth_year = st.selectbox("생년 *", years, index=35) # 1985년생 쯤을 기본으로
        with col4:
            region = st.selectbox("지역 *", regions)

        st.markdown("<br>", unsafe_allow_html=True)

        # 섹션 2: 사회적 지표
        st.markdown("<div class='section-title'>02. 사회적 지표</div>", unsafe_allow_html=True)
        
        col5, col6 = st.columns(2)
        with col5:
            job = st.selectbox("직업 *", jobs)
        with col6:
            edu = st.selectbox("학력 *", educations)
            
        # 추가 질문 (심층 매칭용)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>03. 매칭 선호도 (선택)</div>", unsafe_allow_html=True)
        
        col7, col8 = st.columns(2)
        with col7:
            priority = st.selectbox("배우자 선택 1순위", ["경제력", "외모/스타일", "성격/가치관", "가정환경", "나이차이"])
        with col8:
            style = st.selectbox("선호 데이트 스타일", ["활동적/레저", "정적/문화생활", "맛집탐방/카페", "여행/휴양"])

        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # 제출 버튼 (크고 아름답게)
        if st.button("✨ AI 정밀 진단 결과보기"):
            if name and job != "선택해 주세요." and edu != "선택해 주세요." and region != "선택해 주세요.":
                # 데이터 저장
                st.session_state.user_info = {
                    "name": name, "gender": gender, "year": birth_year,
                    "job": job, "edu": edu, "region": region,
                    "priority": priority
                }
                
                # 로딩 애니메이션 (전문가 느낌)
                with st.spinner("IMD 매칭 엔진이 15만 건의 데이터를 분석 중입니다..."):
                    time.sleep(2) 
                
                st.session_state.page = 'result'
                st.rerun()
            else:
                st.error("정확한 진단을 위해 필수 항목(*)을 모두 선택해 주십시오.")
        
        st.markdown("</div>", unsafe_allow_html=True)

# --- [페이지 2: 분석 결과 리포트] ---
elif st.session_state.page == 'result':
    
    info = st.session_state.user_info
    
    # 가상 분석 로직
    score = random.randint(82, 96)
    
    # 직업군에 따른 티어 설정 (시뮬레이션)
    tier = "노블레스"
    if "전문직" in info['job'] or "임원" in info['job'] or "경영" in info['job']:
        tier = "로얄 블랙"
        match_pool = "의사, 변호사, 500억대 자산가 자제 등"
    elif "공무원" in info['job'] or "대졸" in info['edu']:
        tier = "노블레스"
        match_pool = "공기업, 대기업, 교사, 공무원 등"
    else:
        tier = "스탠다드"
        match_pool = "일반 직장인, 자영업, 프리랜서 등"

    # 차트 생성
    def create_radar():
        categories = ['경제적 안정성', '외모/스타일', '가정환경', '성격/사회성', '매칭 적극성']
        # 직업과 학력에 따라 점수 차등 (시각적 효과)
        base_score = 70
        if "전문직" in info['job']: base_score += 20
        if "박사" in info['edu']: base_score += 10
        
        values = [
            min(base_score, 95), 
            random.randint(70, 90), 
            random.randint(75, 95), 
            random.randint(80, 98), 
            90
        ]
        values += [values[0]]
        categories += [categories[0]]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            fillcolor='rgba(26, 35, 126, 0.2)',
            line=dict(color='#1a237e', width=2),
            marker=dict(color='#d4af37', size=4)
        ))
        fig.update_layout(
            polar=dict(
                bgcolor='white',
                radialaxis=dict(visible=True, range=[0, 100], color='#aaa'),
                angularaxis=dict(color='#333')
            ),
            showlegend=False,
            height=350,
            margin=dict(t=30, b=30, l=40, r=40)
        )
        return fig

    # 결과 화면 구성
    st.markdown(f"""
    <div class='result-card'>
        <h3 style='text-align: center; color: #1a237e;'>📑 {info['name']}님의 매칭 분석 리포트</h3>
        <hr style='border: 0; border-top: 1px solid #eee; margin: 20px 0;'>
        <div style='display: flex; justify-content: space-around; text-align: center; margin-bottom: 20px;'>
            <div>
                <div style='font-size: 0.9rem; color: #666;'>종합 매칭 점수</div>
                <div style='font-size: 2rem; font-weight: 900; color: #d4af37;'>{score}점</div>
            </div>
            <div>
                <div style='font-size: 0.9rem; color: #666;'>추천 등급</div>
                <div style='font-size: 2rem; font-weight: 900; color: #1a237e;'>{tier}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📊 경쟁력 분석")
        st.plotly_chart(create_radar(), use_container_width=True)

    with col2:
        st.markdown("### 📝 AI 매칭 소견")
        st.markdown(f"""
        <div class='bot-msg'>
            <strong>[스펙 분석]</strong><br>
            귀하의 직업({info['job']})과 학력({info['edu']})을 고려했을 때, 
            경제적 안정성 및 사회적 지위 항목에서 높은 점수를 기록했습니다.<br><br>
            <strong>[매칭 전략]</strong><br>
            귀하가 선호하는 <strong>'{info['priority']}'</strong> 가치를 최우선으로 고려할 때,
            일반적인 소개팅보다는 검증된 신원의 <strong>[{tier}]</strong> 그룹 내에서의 매칭이
            성혼 성공률을 <strong>3.5배</strong> 이상 높일 수 있습니다.<br><br>
            <strong>[추천 매칭 풀]</strong><br>
            👉 {match_pool}
        </div>
        """, unsafe_allow_html=True)

    # CTA 버튼
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("내 등급에 맞는 이성 프로필 무료로 받아보기 ➔"):
        st.balloons()
        st.success("신청이 완료되었습니다. 담당 매니저가 24시간 내에 비공개 프로필을 보내드립니다.")
        
    if st.button("🔄 다시 진단하기"):
        st.session_state.page = 'input'
        st.rerun()
