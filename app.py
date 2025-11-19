import streamlit as st
import plotly.graph_objects as go
import time
import random
import datetime
import re

# ==========================================
# [1. 시스템 설정 및 디자인]
# ==========================================
st.set_page_config(
    page_title="IMD 프리미엄 매칭",
    page_icon="💍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 프리미엄 CSS (입력창 라벨 색상 강제 수정 포함)
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

    /* 입력창 라벨 텍스트 색상 강제 변경 */
    .stMarkdown p, .stRadio label, .stSelectbox label, .stTextInput label, .stTextArea label {
        color: #333333 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    
    div[role="radiogroup"] label p {
        color: #333333 !important;
        font-weight: 500 !important;
    }

    /* 버튼 스타일 */
    .stButton > button {
        background: linear-gradient(135deg, #1a237e 0%, #0d47a1 100%);
        color: #fff !important;
        border: none;
        padding: 20px 0 !important;
        font-size: 1.3rem !important;
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
    .stSelectbox > div > div, .stTextInput > div > div > input, .stTextArea > div > div > textarea {
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

    /* AI 분석 박스 */
    .ai-insight-box {
        background-color: #e8eaf6;
        border-left: 4px solid #1a237e;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    .ai-title {
        color: #1a237e;
        font-weight: 800;
        font-size: 1.1rem;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* 키워드 뱃지 */
    .keyword-badge {
        display: inline-block;
        background-color: #fff;
        color: #1a237e;
        border: 1px solid #1a237e;
        padding: 5px 12px;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 8px;
        margin-bottom: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# [2. 사이드바 (더미 메뉴)]
# ==========================================
with st.sidebar:
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
years = [f"{y}년생" for y in range(1960, 2005)]
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

# 텍스트 포렌식 분석 함수 (AI 시뮬레이션)
def analyze_text_forensics(text):
    """
    사용자가 입력한 비정형 텍스트를 분석하여 심리/성향을 도출하는 척하는 함수
    """
    keywords = []
    insights = []
    
    # 1. 키워드 추출 로직 (시뮬레이션)
    if len(text) > 50:
        keywords.append("#진중한_성격")
    else:
        keywords.append("#직관적_성격")
        
    if any(w in text for w in ['돈', '경제', '연봉', '능력', '일']):
        keywords.append("#현실주의")
        insights.append("경제적 가치를 중시하며, 상대방의 비전과 능력을 1순위로 평가하는 경향이 있음.")
    if any(w in text for w in ['사랑', '배려', '대화', '마음', '가정']):
        keywords.append("#관계지향")
        insights.append("정서적 교감과 소통을 중요시하며, 갈등 상황에서 대화로 풀기를 원함.")
    if any(w in text for w in ['여행', '취미', '운동', '맛집']):
        keywords.append("#라이프스타일")
        insights.append("함께 즐길 수 있는 활동적인 파트너를 선호하며, 워라밸을 중시함.")
    
    # 기본값이 없을 경우
    if not keywords:
        keywords = ["#신중함", "#안정추구"]
        insights = ["신중하고 차분한 성향으로, 급격한 변화보다는 안정을 추구함."]
        
    return keywords, insights

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
            birth_year = st.selectbox("생년 *", years, index=25) 
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
            
        # 섹션 3: 매칭 선호도
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>03. 매칭 선호도</div>", unsafe_allow_html=True)
        
        col7, col8 = st.columns(2)
        with col7:
            priority = st.selectbox("배우자 선택 1순위", ["경제력/능력", "외모/스타일", "성격/가치관", "가정환경", "나이차이"])
        with col8:
            style = st.selectbox("선호 데이트 스타일", ["활동적/레저", "정적/문화생활", "맛집탐방/카페", "여행/휴양"])

        # ★ [신규 추가] 섹션 4: AI 텍스트 포렌식 분석 ★
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>04. 심층 성향 분석 (AI Text Forensics)</div>", unsafe_allow_html=True)
        st.info("💡 본인의 매력, 이상형, 가치관 등을 자유롭게 서술해 주세요. AI가 문맥을 분석하여 숨겨진 성향을 도출합니다.")
        
        self_intro = st.text_area(
            "자기소개 및 배우자상 (100자 내외 권장)", 
            height=150, 
            placeholder="예: 저는 성실함을 가장 중요하게 생각합니다. 주말에는 주로 등산을 가거나..."
        )

        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # 제출 버튼
        if st.button("✨ AI 정밀 진단 결과보기"):
            if name and job != "선택해 주세요." and edu != "선택해 주세요." and region != "선택해 주세요.":
                # 데이터 저장
                st.session_state.user_info = {
                    "name": name, "gender": gender, "year": birth_year,
                    "job": job, "edu": edu, "region": region,
                    "priority": priority, "self_intro": self_intro
                }
                
                # 로딩 애니메이션 (전문가 느낌 - 텍스트 분석 과정 보여주기)
                with st.status("IMD AI 엔진 구동 중...", expanded=True) as status:
                    st.write("📡 1. 기본 스펙 데이터베이스 대조 중...")
                    time.sleep(1)
                    st.write("🧠 2. 텍스트 마이닝(Text Mining) 및 성향 추출 중...")
                    time.sleep(1.5)
                    st.write("⚖️ 3. 최적 매칭 그룹 시뮬레이션 중...")
                    time.sleep(1)
                    status.update(label="분석 완료!", state="complete", expanded=False)
                
                st.session_state.page = 'result'
                st.rerun()
            else:
                st.error("필수 항목(*)을 모두 입력해 주십시오.")
        
        st.markdown("</div>", unsafe_allow_html=True)

# --- [페이지 2: 분석 결과 리포트] ---
elif st.session_state.page == 'result':
    
    info = st.session_state.user_info
    
    # 가상 분석 로직
    score = random.randint(82, 96)
    keywords, ai_insights = analyze_text_forensics(info.get('self_intro', ''))
    
    # 직업군에 따른 티어 설정
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
        base_score = 75
        if "전문직" in info['job']: base_score += 15
        
        values = [
            min(base_score + random.randint(-5, 10), 99), 
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
        # ★ AI 포렌식 분석 결과 출력 ★
        st.markdown("### 🧠 AI 텍스트 포렌식(Forensics)")
        
        # 키워드 배지 생성
        badges_html = "".join([f"<span class='keyword-badge'>{k}</span>" for k in keywords])
        
        st.markdown(f"""
        <div class='ai-insight-box'>
            <div class='ai-title'>🔍 심층 성향 분석 결과</div>
            <div style='margin-bottom: 15px;'>{badges_html}</div>
            <div style='font-size: 0.95rem; line-height: 1.6; color: #333;'>
                {ai_insights[0] if ai_insights else "입력된 텍스트가 부족하여 심층 분석이 제한적입니다."}<br><br>
                작성하신 내용의 문맥(Context)을 분석했을 때, 귀하는 <strong>'{info['priority']}'</strong>을(를) 중요시하면서도 
                내면적으로는 <strong>안정적인 유대감</strong>을 갈망하는 성향이 관찰됩니다.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style='background-color: #fff; border: 1px solid #eee; padding: 15px; border-radius: 8px;'>
            <strong style='color: #1a237e;'>💡 최종 매칭 전략</strong><br>
            일반 매칭보다는 신원이 검증된 <strong>[{tier}]</strong> 그룹 내에서, 
            귀하의 성향을 이해해 줄 수 있는 <strong>전문직/안정적 직군</strong>과의 매칭이 
            성혼 확률을 <strong>3.5배</strong> 높일 수 있습니다.
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
