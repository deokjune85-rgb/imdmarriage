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
    page_title="IMD 프리미엄 매칭 솔루션",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 프리미엄 CSS (검은 박스 제거 및 UI 최적화)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    /* 메인 배경색 */
    .stApp {
        background-color: #f8f9fa;
        color: #333;
    }

    /* 사이드바 스타일 */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e0e0e0;
    }

    /* 헤더 스타일 (심플 & 고급) */
    .main-header {
        text-align: center;
        padding: 40px 0 30px 0;
        background: white;
        margin-bottom: 30px;
    }
    .main-title {
        font-size: 2.4rem;
        font-weight: 900;
        color: #0d1b2a; /* 딥 네이비 */
        letter-spacing: -0.5px;
        margin-bottom: 10px;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #555;
        font-weight: 400;
    }

    /* 입력 폼 컨테이너 */
    .form-container {
        background-color: #ffffff;
        padding: 50px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.03);
        border: 1px solid #f0f0f0;
        max-width: 900px;
        margin: 0 auto;
    }

    /* 섹션 타이틀 */
    .section-title {
        font-size: 1.4rem;
        font-weight: 800;
        color: #1b263b;
        margin-top: 40px;
        margin-bottom: 20px;
        border-left: 5px solid #d4af37; /* 골드 */
        padding-left: 15px;
        line-height: 1;
    }
    
    /* 첫 번째 섹션 타이틀은 마진 탑 제거 */
    .first-title {
        margin-top: 0 !important;
    }

    /* 입력창 라벨 스타일링 */
    .stMarkdown p, .stRadio label, .stSelectbox label, .stTextInput label, .stTextArea label {
        color: #333333 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }

    /* 버튼 스타일 */
    .stButton > button {
        background: linear-gradient(135deg, #1b263b 0%, #0d1b2a 100%);
        color: #fff !important;
        border: none;
        padding: 22px 0 !important;
        font-size: 1.3rem !important;
        font-weight: 800 !important;
        border-radius: 12px !important;
        width: 100%;
        box-shadow: 0 10px 20px rgba(27, 38, 59, 0.2);
        transition: all 0.3s ease;
        margin-top: 30px;
    }
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 30px rgba(27, 38, 59, 0.3);
        background: linear-gradient(135deg, #2c3e50 0%, #1b263b 100%);
    }
    
    /* 인풋 필드 디자인 */
    .stSelectbox > div > div, .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: #fcfcfc;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        color: #333;
        font-size: 1rem;
    }
    .stTextArea > div > div > textarea:focus {
        border-color: #d4af37;
        box-shadow: 0 0 0 1px #d4af37;
    }

    /* 결과 리포트 스타일 */
    .result-card {
        background: #fff;
        border-top: 5px solid #1b263b;
        border-radius: 10px;
        padding: 30px;
        margin-top: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }

    /* AI 분석 박스 (포렌식) */
    .forensic-box {
        background-color: #f4f6f8;
        border: 1px solid #dae1e7;
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 25px;
    }
    .mbti-badge {
        display: inline-block;
        background: #1b263b;
        color: #d4af37;
        font-weight: 900;
        font-size: 1.5rem;
        padding: 5px 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        letter-spacing: 2px;
    }
    
    /* 자동 매칭 프로필 카드 */
    .match-profile-card {
        background: linear-gradient(135deg, #ffffff 0%, #fdfbf7 100%);
        border: 2px solid #d4af37;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        position: relative;
        overflow: hidden;
        margin-top: 20px;
    }
    .match-tag {
        background-color: #d4af37;
        color: white;
        font-weight: bold;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 0 5px;
    }
    
    /* 알림 박스 숨기기 (검은 박스 제거) */
    [data-testid="stStatusWidget"] {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# [2. 사이드바 메뉴]
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='color:#1b263b; text-align:center; font-weight:900;'>IMD MATCHING</h2>", unsafe_allow_html=True)
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
    <div style='font-size: 0.8rem; color: #888; text-align: center;'>
        <strong>VIP 전용 센터</strong><br>
        02-555-0000<br>
        (100% 예약제 운영)
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# [3. 로직 엔진 (Forensics & Matching)]
# ==========================================

# 드롭다운 데이터 (업데이트됨)
years = [f"{y}년생" for y in range(1960, 2005)]
educations = ["선택해 주세요.", "고등학교졸", "전문대졸", "대졸", "대학원졸", "박사이상", "기타"]
jobs = ["선택해 주세요.", "전문직", "공무원/공기업", "직장인", "사업", "프리랜서", "기타"]
regions = [
    "선택해 주세요.", "서울특별시", "경기북부", "경기남부", "경기성남", "인천광역시", 
    "부산광역시", "울산광역시", "세종시", "대구광역시", "대전광역시", "광주광역시", 
    "강원도", "충청남도", "충청북도", "경상남도", "경상북도", "전라남도", "전라북도", "제주도", "해외거주"
]

def analyze_deep_forensics(text, job, q_answers):
    """
    사용자의 텍스트와 설문 답변을 분석하여 MBTI, 성향, 잠재 욕망을 도출하는 시뮬레이션 엔진
    """
    # 1. MBTI 추론 로직 (단어 기반 휴리스틱 + 설문 답변 반영)
    mbti_e = "E" if any(w in text for w in ['모임', '활동', '여행', '함께', '대화', '친구']) else "I"
    mbti_n = "N" if any(w in text for w in ['미래', '꿈', '비전', '가치', '의미', '상상']) else "S"
    
    # 갈등 해결 방식(F/T) 질문 반영
    conflict_ans = q_answers.get('conflict', '')
    mbti_f = "T" if "논리적" in conflict_ans or "시간" in conflict_ans else "F"
    
    # 결혼 생활 선호(J/P) 질문 반영
    life_ans = q_answers.get('marriage_life', '')
    mbti_j = "J" if "안정적" in life_ans or "계획" in life_ans else "P"
    
    mbti_result = f"{mbti_e}{mbti_n}{mbti_f}{mbti_j}"
    
    # 2. 성향 분석 키워드
    keywords = []
    if "전문직" in job or "사업" in job: keywords.append("#성취지향")
    else: keywords.append("#안정지향")
    
    relation_ans = q_answers.get('relation', '')
    if "친구" in relation_ans: keywords.append("#동반자적_관계")
    elif "존경" in relation_ans: keywords.append("#상호존중")
    else: keywords.append("#정서적_유대")

    # 3. 잠재 욕망 (Hidden Desire) 분석
    desire = "안정적인 가정과 정서적 지지" # 기본값
    
    priority = q_answers.get('priority', '')
    if "경제력" in priority:
        desire = "함께 자산을 증식하고 풍요를 누릴 수 있는 '비즈니스 파트너' 같은 배우자"
    elif "외모" in priority:
        desire = "나의 가치를 높여줄 수 있는 '매력적이고 세련된' 배우자"
    elif "성격" in priority or "대화" in text:
        desire = "평생 친구처럼 지낼 수 있는 '소울메이트' 같은 배우자"
    elif "가정환경" in priority:
        desire = "비슷한 환경에서 자라 공감대가 깊은 '안정적인' 배우자"

    return mbti_result, keywords, desire

def get_auto_match_profile(mbti, user_job, region):
    """
    사용자의 MBTI, 직업, 지역을 기반으로 DB에서 최적의 상대를 찾아내는 시뮬레이션
    """
    # MBTI 궁합 로직
    partner_mbti = "ESFJ" # Default
    if "INT" in mbti: partner_mbti = "ENFP"
    elif "EST" in mbti: partner_mbti = "ISFJ"
    elif "INF" in mbti: partner_mbti = "ENTJ"
    
    # 직업 매칭 로직 (상호 보완)
    partner_job = "교사/공무원/공기업"
    partner_img = "지적이고 차분한 이미지"
    
    if "전문직" in user_job or "사업" in user_job:
        partner_job = "약사/교사/전문직"
        partner_img = "내조가 가능하고 밝은 에너지의 이미지"
    elif "직장인" in user_job:
        partner_job = "대기업/외국계/전문직"
        partner_img = "대화가 잘 통하는 스마트한 이미지"
    
    # 지역 매칭 (근거리 원칙)
    partner_region = region.split(" ")[0] if "경기" not in region else "수도권"
    if region == "해외거주": partner_region = "해외/수도권"

    return {
        "mbti": partner_mbti,
        "job": partner_job,
        "image": partner_img,
        "region": partner_region,
        "age": "3~4살 차이 (선호도 반영)",
        "asset": "자가 보유 및 노후 준비 완료"
    }

# 세션 상태
if 'page' not in st.session_state: st.session_state.page = 'input'
if 'user_info' not in st.session_state: st.session_state.user_info = {}

# ==========================================
# [4. 메인 화면 로직]
# ==========================================

# 헤더 출력
st.markdown("""
<div class='main-header'>
    <div class='main-title'>IMD AI 매칭 진단</div>
    <div class='sub-title'>15만 건의 빅데이터와 심리학이 분석하는 <b>당신의 운명적 상대</b></div>
</div>
""", unsafe_allow_html=True)

# --- [페이지 1: 정보 입력 폼] ---
if st.session_state.page == 'input':
    
    with st.container():
        st.markdown("<div class='form-container'>", unsafe_allow_html=True)
        
        # --- 섹션 1: 결혼 가치관 진단 (심리) ---
        st.markdown("<div class='section-title first-title'>STEP 1. 결혼 가치관 진단 (Psychology)</div>", unsafe_allow_html=True)
        
        q1 = st.radio("1. 결혼 경험이 있으십니까?", ["초혼 (미혼)", "재혼 (돌싱)"], horizontal=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        q2 = st.selectbox("2. 결혼 예정은 언제로 생각하고 계십니까?", ["1년 이내 (구체적 계획 있음)", "2~3년 이내", "좋은 사람 있으면 언제든", "아직 구체적 계획 없음"])
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_q3, col_q4 = st.columns(2)
        with col_q3:
            q3 = st.selectbox("3. 결혼이 하고 싶은 가장 큰 이유는?", ["정서적 안정감", "내 편이 생긴다는 든든함", "자녀 양육 및 가정 형성", "노후의 동반자 필요", "경제적 시너지 효과"])
        with col_q4:
            q4 = st.selectbox("4. 가장 선호하는 배우자와의 관계는?", ["친구 같은 편안한 관계", "서로 존경하고 배우는 관계", "서로의 일을 지지해주는 파트너십", "로맨틱하고 열정적인 연인 관계"])
            
        col_q5, col_q6 = st.columns(2)
        with col_q5:
            q5 = st.selectbox("5. 가장 원하는 결혼 생활은?", ["취미를 공유하는 활동적인 삶", "퇴근 후 소소하게 대화하는 일상", "각자의 시간을 존중하는 독립적인 삶", "자녀와 함께하는 북적이는 삶"])
        with col_q6:
            q6 = st.selectbox("6. 부모님은 당신의 결혼에 대해 어떻게 생각하시나요?", ["전적으로 내 의견 존중", "어느 정도 의견 제시 (조율 가능)", "부모님 의견이 매우 중요함", "상관없음"])

        st.markdown("<br>", unsafe_allow_html=True)
        q7 = st.selectbox("7. 내가 꿈꾸는 이상형의 조건 1순위는?", ["경제력/직업의 안정성", "외모/키/스타일", "성격/가치관/유머코드", "가정환경/화목함", "나이 차이"])
        st.markdown("<br>", unsafe_allow_html=True)
        q8 = st.selectbox("8. 갈등이 생겼을 때 선호하는 해결 방안은?", ["바로 대화로 풀고 털어낸다", "시간을 갖고 감정을 식힌 뒤 대화한다", "논리적으로 잘잘못을 따져 해결한다", "상대방이 맞춰주길 바란다"])

        # --- 섹션 2: 프로필 정보 (현실) ---
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>STEP 2. 프로필 입력 (Profile)</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("이름 (실명)", placeholder="이름을 입력해주세요")
        with col2:
            gender = st.radio("성별", ["남성", "여성"], horizontal=True)
        
        col3, col4 = st.columns(2)
        with col3:
            birth_year = st.selectbox("생년월일 (년)", years, index=25) 
        with col4:
            region = st.selectbox("사는 지역", regions)

        st.markdown("<br>", unsafe_allow_html=True)
        
        col5, col6 = st.columns(2)
        with col5:
            job = st.selectbox("직업", jobs)
        with col6:
            edu = st.selectbox("최종 학력", educations)

        # --- 섹션 3: 포렌식 (심층 분석) ---
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>STEP 3. AI 심층 성향 분석 (Deep Profiling)</div>", unsafe_allow_html=True)
        st.info("💡 **[AI 포렌식 엔진 작동 중]** 본인의 매력, 이상형, 가치관 등을 자유롭게 적어주세요. AI가 글의 맥락을 분석하여 **'숨겨진 성향'**과 **'MBTI'**를 도출합니다.")
        
        self_intro = st.text_area(
            "자기소개 및 배우자상 (자유 서술)", 
            height=200, 
            placeholder="예시: 저는 평소에는 차분하지만 친한 사람들과 있을 때는 활발한 편입니다. 주말에는 주로 운동을 하거나 맛집을 찾아다닙니다. 상대방은 대화가 잘 통하고 배려심이 깊은 사람이면 좋겠습니다. 특히 경제 관념이 확실하고 미래에 대한 비전이 있는 분을 선호합니다."
        )

        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # 제출 버튼
        if st.button("✨ AI 정밀 진단 및 자동 매칭 실행"):
            if name and job != "선택해 주세요." and region != "선택해 주세요." and len(self_intro) > 10:
                # 데이터 저장
                st.session_state.user_info = {
                    "name": name, "gender": gender, "year": birth_year,
                    "job": job, "edu": edu, "region": region,
                    "self_intro": self_intro,
                    "answers": {
                        "marriage_exp": q1, "timing": q2, "reason": q3, 
                        "relation": q4, "marriage_life": q5, "parents": q6,
                        "priority": q7, "conflict": q8
                    }
                }
                
                # AI 연산 시뮬레이션
                progress_text = "IMD AI 엔진 가동 중..."
                my_bar = st.progress(0, text=progress_text)

                for percent_complete in range(100):
                    time.sleep(0.02)
                    if percent_complete == 30:
                        my_bar.progress(percent_complete, text="🧠 1. 결혼 가치관 및 심리 데이터 분석 중...")
                    elif percent_complete == 60:
                        my_bar.progress(percent_complete, text="📡 2. 텍스트 포렌식(Forensics)으로 성향 추출 중...")
                    elif percent_complete == 90:
                        my_bar.progress(percent_complete, text=f"🔍 3. {name}님과 매칭되는 {region.split(' ')[0]} 지역 이성 스캐닝 중...")
                    else:
                        my_bar.progress(percent_complete)
                
                st.session_state.page = 'result'
                st.rerun()
            else:
                st.error("필수 항목을 모두 입력하고, 자기소개를 10자 이상 작성해 주십시오.")
        
        st.markdown("</div>", unsafe_allow_html=True)

# --- [페이지 2: 분석 결과 리포트] ---
elif st.session_state.page == 'result':
    
    info = st.session_state.user_info
    
    # AI 분석 실행
    mbti, keywords, desire = analyze_deep_forensics(info['self_intro'], info['job'], info['answers'])
    partner_profile = get_auto_match_profile(mbti, info['job'], info['region'])
    
    # 가상 분석 로직
    score = random.randint(85, 98)
    
    # 결과 화면 구성
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"""
        <div class='result-card'>
            <h3 style='color: #1b263b; margin-bottom: 20px;'>🧠 AI 성향 프로파일링 결과</h3>
            <div class='forensic-box'>
                <div style='text-align: center;'>
                    <span style='color:#555; font-size:0.9rem;'>텍스트 및 설문 분석을 통한 추정 MBTI</span><br>
                    <div class='mbti-badge'>{mbti}</div>
                </div>
                <hr style='border-color: #ddd;'>
                <p style='font-weight: bold; color: #1b263b;'>🔑 주요 성향 키워드</p>
                <p>{', '.join([f"#{k.replace('#','')}" for k in keywords])}</p>
                <br>
                <p style='font-weight: bold; color: #1b263b;'>👁️ AI가 발견한 숨겨진 욕망 (Hidden Desire)</p>
                <p style='color: #d4af37; font-weight: 600;'>"{desire}"</p>
                <p style='font-size: 0.9rem; color: #666; margin-top: 10px;'>
                    귀하가 작성하신 문장의 어조와 답변 패턴을 종합 분석한 결과, <br>
                    겉으로는 <strong>{keywords[0].replace('#','')}</strong>을(를) 보이지만 
                    내면 깊은 곳에서는 위와 같은 가치를 공유할 수 있는 파트너를 갈망하고 있습니다.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # 레이더 차트 (성향)
        categories = ['경제적 준비', '가치관 적합도', '가정 환경', '성격 조화', '결혼 의지']
        values = [random.randint(75, 98) for _ in range(5)]
        values += [values[0]]
        categories += [categories[0]]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            fillcolor='rgba(27, 38, 59, 0.2)',
            line=dict(color='#1b263b', width=2),
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
            margin=dict(t=40, b=20, l=40, r=40),
            title=dict(text="나의 결혼 준비도 분석", font=dict(size=16))
        )
        st.plotly_chart(fig, use_container_width=True)

    # ---------------------------------------------
    # [자동 매칭 결과]
    # ---------------------------------------------
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center; color: #1b263b;'>💘 AI Auto-Match Result</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #666;'>귀하의 프로파일링 데이터({mbti})와 가장 완벽한 궁합을 가진 상대를 DB에서 찾아냈습니다.</p>", unsafe_allow_html=True)
    
    match_count = random.randint(12, 45)
    
    st.markdown(f"""
    <div class='match-profile-card'>
        <div style='position: absolute; top: 20px; right: 20px; background: #ff6b6b; color: white; padding: 5px 10px; border-radius: 5px; font-weight: bold; font-size: 0.8rem;'>MATCH 98%</div>
        <div style='font-size: 3rem;'>👩‍❤️‍👨</div>
        <h3 style='color: #1b263b; margin-top: 10px;'>추천 매칭 그룹: [ {partner_profile['job']} ]</h3>
        <p style='color: #555; font-weight: 600;'>{partner_profile['image']} / {partner_profile['region']} 거주</p>
        <hr style='border: 0; border-top: 1px dashed #d4af37; margin: 20px 0; width: 50%; margin-left: auto; margin-right: auto;'>
        
        <div style='display: flex; justify-content: center; flex-wrap: wrap; gap: 10px;'>
            <span class='match-tag'>#{partner_profile['mbti']}</span>
            <span class='match-tag'>#{partner_profile['age']}</span>
            <span class='match-tag'>#{partner_profile['asset']}</span>
            <span class='match-tag'>#가치관_일치</span>
        </div>
        
        <p style='margin-top: 20px; color: #333; font-size: 0.95rem; line-height: 1.6;'>
            <strong>[AI 매칭 소견]</strong><br>
            귀하의 <strong>{mbti}</strong> 성향과 상호 보완이 되는 <strong>{partner_profile['mbti']}</strong> 성향을 가졌으며,<br>
            특히 <strong>'{info['answers']['conflict']}'</strong>라는 갈등 해결 방식이 서로 일치하여 안정적인 결혼 생활이 예측됩니다.<br>
            <br>
            현재 당사 DB에 해당 그룹 회원이 <strong>{match_count}명</strong> 매칭 대기 중입니다.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # CTA 버튼
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(f"매칭된 {match_count}명의 비공개 프로필 열람하기 (매니저 연결) ➔"):
        st.balloons()
        st.success("신청이 완료되었습니다. 담당 매니저가 매칭된 프로필 리스트를 가지고 연락드릴 예정입니다.")
        
    if st.button("🔄 다시 진단하기"):
        st.session_state.page = 'input'
        st.rerun()
