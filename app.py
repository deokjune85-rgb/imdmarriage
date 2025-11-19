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

# 프리미엄 CSS (글자 안 보임 현상 완벽 수정 + 임팩트 디자인)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    /* 메인 배경색 */
    .stApp {
        background-color: #f4f7f6;
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
        padding: 40px 0 30px 0;
        background: white;
        margin-bottom: 30px;
        border-bottom: 3px solid #1a237e;
    }
    .main-title {
        font-size: 2.4rem;
        font-weight: 900;
        color: #1a237e; /* 딥 네이비 */
        letter-spacing: -0.5px;
        margin-bottom: 10px;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #555;
        font-weight: 500;
    }

    /* 입력 폼 컨테이너 */
    .form-container {
        background-color: #ffffff;
        padding: 50px;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.08);
        border: 1px solid #fff;
        max-width: 900px;
        margin: 0 auto;
    }

    /* 섹션 타이틀 */
    .section-title {
        font-size: 1.5rem;
        font-weight: 800;
        color: #1a237e;
        margin-top: 40px;
        margin-bottom: 25px;
        border-left: 6px solid #d4af37; /* 골드 */
        padding-left: 15px;
        background: linear-gradient(90deg, #f8f9fa 0%, #ffffff 100%);
        padding-top: 5px;
        padding-bottom: 5px;
    }
    
    .first-title { margin-top: 0 !important; }

    /* ★★★ 중요: 입력창/라디오버튼 글자색 강제 지정 (안 보임 해결) ★★★ */
    .stMarkdown p, .stRadio label, .stSelectbox label, .stTextInput label, .stTextArea label {
        color: #111111 !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
    }
    
    /* 라디오 버튼 선택지 텍스트 */
    div[role="radiogroup"] label p {
        color: #111111 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }

    /* 버튼 스타일 (고급형) */
    .stButton > button {
        background: linear-gradient(135deg, #1a237e 0%, #0d47a1 100%);
        color: #fff !important;
        border: none;
        padding: 20px 0 !important;
        font-size: 1.3rem !important;
        font-weight: 800 !important;
        border-radius: 50px !important;
        width: 100%;
        box-shadow: 0 10px 25px rgba(26, 35, 126, 0.25);
        transition: all 0.3s ease;
        margin-top: 30px;
    }
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 15px 35px rgba(26, 35, 126, 0.35);
        background: linear-gradient(135deg, #283593 0%, #1565c0 100%);
    }
    
    /* 인풋 필드 디자인 */
    .stSelectbox > div > div, .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: #f8f9fa;
        border: 1px solid #ced4da;
        border-radius: 10px;
        color: #333;
        font-size: 1rem;
    }
    .stTextArea > div > div > textarea:focus {
        border-color: #1a237e;
        box-shadow: 0 0 0 2px rgba(26, 35, 126, 0.2);
    }

    /* ===========================
       결과 화면 임팩트 디자인
       =========================== */
    
    /* 1. 프로파일링 카드 (좌측) */
    .profile-card {
        background: #fff;
        border-top: 5px solid #333;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.05);
        height: 100%;
    }

    /* 2. 매칭 결과 카드 (우측 - 시크릿 문서 느낌) */
    .secret-file {
        background: white;
        border: 2px solid #d4af37;
        border-radius: 15px;
        padding: 0;
        box-shadow: 0 10px 30px rgba(212, 175, 55, 0.15);
        overflow: hidden;
        position: relative;
    }
    
    .file-header {
        background: #d4af37;
        color: #fff;
        padding: 15px;
        text-align: center;
        font-weight: 900;
        font-size: 1.2rem;
        letter-spacing: 2px;
    }
    
    .file-body {
        padding: 30px;
        background: linear-gradient(180deg, #fff 0%, #fdfbf7 100%);
    }

    /* 태그 스타일 */
    .tag-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        justify-content: center;
        margin-top: 15px;
    }
    .ai-tag {
        background-color: #1a237e;
        color: white;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        box-shadow: 0 3px 6px rgba(26, 35, 126, 0.2);
    }
    
    /* 텍스트 강조 */
    .highlight-text {
        background: linear-gradient(120deg, #fff176 0%, #ffd54f 100%);
        padding: 0 5px;
        font-weight: bold;
        color: #000;
    }
    
    /* 점수판 */
    .score-board {
        display: flex;
        justify-content: space-between;
        background: #f1f3f5;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .score-item {
        text-align: center;
        width: 33%;
    }
    .score-num {
        font-size: 1.8rem;
        font-weight: 900;
        color: #1a237e;
    }
    .score-label {
        font-size: 0.8rem;
        color: #666;
        text-transform: uppercase;
    }

    /* 시스템 메시지 숨김 */
    [data-testid="stStatusWidget"] {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# [2. 사이드바 메뉴]
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='color:#1a237e; text-align:center; font-weight:900; margin-top:0;'>IMD AI MATCHING</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#666; font-size:0.8rem;'>Professional Marriage System</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    menu_options = [
        "💘 이상형 정밀 진단",
        "💞 연애 스타일 분석",
        "🧠 결혼 심리 테스트",
        "📊 내 결혼 등급 확인",
        "🔄 재혼 성공률 예측",
        "💰 가입비 산출 계산기"
    ]
    
    for menu in menu_options:
        if st.button(menu, use_container_width=True, key=menu):
            st.toast(f"'{menu}' 모듈은 기업 전용 데모입니다.", icon="🔒")
    
    st.markdown("---")
    st.info("**[CEO 전용]**\n이 사이드바 메뉴는 귀사의 서비스 구성에 맞춰 커스터마이징됩니다.")

# ==========================================
# [3. 로직 엔진]
# ==========================================

# 드롭다운 데이터
years = [f"{y}년생" for y in range(1960, 2005)]
educations = ["선택해 주세요.", "고등학교졸", "전문대졸", "대졸", "대학원졸", "박사이상", "기타"]
jobs = ["선택해 주세요.", "전문직 (의/약사)", "전문직 (법조계)", "대기업/금융", "공기업/공무원", "사업가/CEO", "교육직/교수", "프리랜서/예술", "기타"]
regions = [
    "선택해 주세요.", "서울특별시", "경기북부", "경기남부", "경기성남", "인천광역시", 
    "부산광역시", "울산광역시", "세종시", "대구광역시", "대전광역시", "광주광역시", 
    "강원도", "충청남도", "충청북도", "경상남도", "경상북도", "전라남도", "전라북도", "제주도", "해외거주"
]

def analyze_deep_forensics(text, job, q_answers):
    """AI 프로파일링 시뮬레이션"""
    # 1. MBTI 추론
    mbti_e = "E" if any(w in text for w in ['모임', '활동', '여행', '함께', '대화', '친구']) else "I"
    mbti_n = "N" if any(w in text for w in ['미래', '꿈', '비전', '가치', '의미', '상상']) else "S"
    conflict_ans = q_answers.get('conflict', '')
    mbti_f = "T" if "논리적" in conflict_ans or "시간" in conflict_ans else "F"
    life_ans = q_answers.get('marriage_life', '')
    mbti_j = "J" if "안정적" in life_ans or "계획" in life_ans else "P"
    mbti_result = f"{mbti_e}{mbti_n}{mbti_f}{mbti_j}"
    
    # 2. 성향 키워드
    keywords = []
    if "전문직" in job or "사업" in job: keywords.append("#성취지향형_엘리트")
    else: keywords.append("#안정추구형_인재")
    
    priority = q_answers.get('priority', '')
    if "경제력" in priority: keywords.append("#현실감각_상위1%")
    elif "성격" in priority: keywords.append("#정서적_교감_중시")
    elif "외모" in priority: keywords.append("#심미적_가치_추구")
    
    # 3. 욕망 분석
    desire = "서로의 성장을 돕는 안정적인 가정"
    if "돈" in text or "경제" in text: desire = "경제적 자유를 함께 누릴 비즈니스 파트너"
    elif "대화" in text: desire = "영혼이 통하는 소울메이트"

    return mbti_result, keywords, desire

def get_auto_match_profile(user_job, region):
    """자동 매칭 프로필 생성"""
    partner_job = "교사/공무원"
    partner_img = "지적이고 차분한 이미지"
    
    if "의" in user_job or "법" in user_job or "사업" in user_job:
        partner_job = "약사/교사/아나운서"
        partner_img = "내조가 가능하고 밝은 에너지의 이미지"
    elif "대기업" in user_job or "금융" in user_job:
        partner_job = "전문직/대기업/공기업"
        partner_img = "대화가 잘 통하는 스마트한 커리어우먼"
    
    region_clean = region.split(" ")[0] if "경기" not in region else "수도권"
    if region == "해외거주": region_clean = "해외/수도권"

    return {
        "job": partner_job,
        "image": partner_img,
        "region": region_clean,
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
    <div class='main-title'>IMD AI Premium Matchmaker</div>
    <div class='sub-title'>15만 건의 빅데이터가 증명하는 <b>상위 1% 성혼 알고리즘</b></div>
</div>
""", unsafe_allow_html=True)

# --- [페이지 1: 정보 입력 폼] ---
if st.session_state.page == 'input':
    
    with st.container():
        st.markdown("<div class='form-container'>", unsafe_allow_html=True)
        
        # 섹션 1: 심리 진단
        st.markdown("<div class='section-title first-title'>STEP 1. 결혼 가치관 진단 (Psychology)</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            q1 = st.radio("1. 결혼 경험이 있으십니까?", ["초혼 (미혼)", "재혼 (돌싱)"], horizontal=True)
        with col2:
            q2 = st.selectbox("2. 결혼 예정은 언제로 생각하십니까?", ["1년 이내 (구체적 계획)", "2~3년 이내", "좋은 사람 있으면 언제든", "아직 미정"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        col3, col4 = st.columns(2)
        with col3:
            q3 = st.selectbox("3. 결혼의 가장 큰 목적은?", ["정서적 안정감", "내 편이 생긴다는 든든함", "자녀 양육 및 가정", "경제적 시너지", "부모님으로부터의 독립"])
        with col4:
            q4 = st.selectbox("4. 이상적인 배우자 관계는?", ["친구 같은 편안함", "존경할 수 있는 멘토", "상호 보완적인 파트너십", "열정적인 연인"])

        st.markdown("<br>", unsafe_allow_html=True)
        q7 = st.selectbox("5. 배우자 선택 시 절대 포기 못하는 1순위는?", ["경제력/직업 안정성", "외모/키/스타일", "성격/가치관/유머", "가정환경/화목함", "나이 차이"])
        
        q8_dummy = "논리적" # 내부 변수용
        q5_dummy = "안정적" # 내부 변수용

        # 섹션 2: 프로필
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>STEP 2. 프로필 입력 (Profile)</div>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("이름 (실명)", placeholder="홍길동")
        with c2:
            gender = st.radio("성별", ["남성", "여성"], horizontal=True)
        
        c3, c4 = st.columns(2)
        with c3:
            birth_year = st.selectbox("생년월일 (년)", years, index=25) 
        with c4:
            region = st.selectbox("거주 지역", regions)

        st.markdown("<br>", unsafe_allow_html=True)
        c5, c6 = st.columns(2)
        with c5:
            job = st.selectbox("직업군", jobs)
        with c6:
            edu = st.selectbox("최종 학력", educations)

        # 섹션 3: AI 포렌식
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>STEP 3. AI 심층 성향 분석 (Deep Profiling)</div>", unsafe_allow_html=True)
        st.info("💡 **[AI 포렌식 엔진 가동]** 본인의 매력, 이상형, 가치관을 자유롭게 적어주세요. (길게 적을수록 매칭 정확도가 올라갑니다)")
        
        self_intro = st.text_area(
            "자기소개 및 배우자상 (자유 서술)", 
            height=200, 
            placeholder="예: 저는 대기업 연구원으로 일하고 있으며, 평소에는 차분하지만 취미 생활을 할 때는 열정적입니다. 주말에는 골프나 캠핑을 즐깁니다. 상대방은 대화가 잘 통하고 감정 기복이 크지 않은 사람이면 좋겠습니다. 특히 미래에 대한 비전이 확실한 분을 선호합니다."
        )

        # 제출 버튼
        if st.button("✨ AI 정밀 진단 및 매칭 상대 확인하기"):
            if name and job != "선택해 주세요." and region != "선택해 주세요." and len(self_intro) > 10:
                st.session_state.user_info = {
                    "name": name, "gender": gender, "year": birth_year,
                    "job": job, "edu": edu, "region": region,
                    "self_intro": self_intro,
                    "answers": {"priority": q7, "conflict": "논리적", "marriage_life": "안정적"}
                }
                
                # 화려한 로딩 효과
                with st.status("🚀 IMD AI 매칭 엔진 가동 중...", expanded=True) as status:
                    st.write("🧠 1. 심리/가치관 데이터 백터화(Vectorizing)...")
                    time.sleep(1)
                    st.write("🔍 2. 텍스트 포렌식 분석으로 MBTI 및 성향 추출...")
                    time.sleep(1)
                    st.write(f"📂 3. {region.split(' ')[0]} 지역 거주, {job} 선호 이성 DB 스캐닝...")
                    time.sleep(1)
                    st.write("✅ 매칭 알고리즘 연산 완료!")
                    time.sleep(0.5)
                    status.update(label="분석 완료!", state="complete", expanded=False)
                
                st.session_state.page = 'result'
                st.rerun()
            else:
                st.error("⚠️ 필수 항목을 모두 입력하고, 자기소개를 10자 이상 작성해 주십시오.")
        
        st.markdown("</div>", unsafe_allow_html=True)

# --- [페이지 2: 분석 결과 리포트] ---
elif st.session_state.page == 'result':
    
    info = st.session_state.user_info
    mbti, keywords, desire = analyze_deep_forensics(info['self_intro'], info['job'], info['answers'])
    partner = get_auto_match_profile(info['job'], info['region'])
    
    match_count = random.randint(15, 42)
    
    # 결과 레이아웃
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # 1. 내 프로파일링 카드
        st.markdown(f"""
        <div class='profile-card'>
            <h3 style='color:#1a237e; margin-bottom:10px;'>🧠 {info['name']}님 성향 분석 리포트</h3>
            <hr style='margin: 15px 0;'>
            <div class='score-board'>
                <div class='score-item'>
                    <div class='score-label'>결혼 준비도</div>
                    <div class='score-num'>A+</div>
                </div>
                <div class='score-item'>
                    <div class='score-label'>매칭 경쟁력</div>
                    <div class='score-num'>92<span style='font-size:1rem'>점</span></div>
                </div>
                <div class='score-item'>
                    <div class='score-label'>추정 MBTI</div>
                    <div class='score-num' style='color:#d4af37;'>{mbti}</div>
                </div>
            </div>
            <p><strong>🔑 핵심 키워드:</strong> {', '.join(keywords)}</p>
            <p><strong>👁️ AI가 발견한 내면의 욕망:</strong><br>
            <span class='highlight-text'>"{desire}"</span></p>
            <br>
            <div style='background:#f8f9fa; padding:15px; border-radius:10px; border:1px solid #eee; font-size:0.9rem; line-height:1.6;'>
                귀하는 <strong>{keywords[0].replace('#','')}</strong> 성향이 강하며, 
                단순한 조건 만남보다는 <strong>{info['answers']['priority']}</strong> 코드가 맞는 사람과 만났을 때 
                성혼 확률이 <strong>3.8배</strong> 상승합니다.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 레이더 차트
        categories = ['경제력', '외모/스타일', '가정환경', '성격/사회성', '결혼의지']
        values = [random.randint(75, 95) for _ in range(5)]
        values += [values[0]]
        categories += [categories[0]]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values, theta=categories,
            fill='toself', fillcolor='rgba(26, 35, 126, 0.1)',
            line=dict(color='#1a237e', width=2), marker=dict(color='#d4af37', size=4)
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100], color='#aaa')),
            showlegend=False, height=300, margin=dict(t=20, b=20, l=30, r=30),
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # 2. 매칭 결과 (시크릿 파일 컨셉)
        st.markdown(f"""
        <div class='secret-file'>
            <div class='file-header'>CONFIDENTIAL: MATCHING RESULT</div>
            <div class='file-body'>
                <div style='text-align:center; margin-bottom:20px;'>
                    <span style='background:#ff5252; color:white; padding:5px 10px; border-radius:5px; font-weight:bold; font-size:0.8rem;'>MATCH 98.5%</span>
                    <h2 style='color:#1a237e; margin:10px 0;'>Best Match Group</h2>
                    <h3 style='color:#333;'>[ {partner['job']} ]</h3>
                    <p style='color:#666; font-weight:600;'>{partner['image']}</p>
                </div>
                
                <div class='tag-container'>
                    <span class='ai-tag'>#{partner['region']}거주</span>
                    <span class='ai-tag'>#가치관_일치</span>
                    <span class='ai-tag'>#MBTI_상호보완</span>
                    <span class='ai-tag'>#{partner['asset']}</span>
                </div>
                
                <hr style='border:0; border-top:1px dashed #ccc; margin:25px 0;'>
                
                <p style='font-size:1rem; line-height:1.6; color:#333;'>
                    <strong>[AI 매칭 소견]</strong><br>
                    귀하의 <strong>{mbti}</strong> 성향과 가장 완벽한 조화를 이루는 그룹입니다.
                    특히 귀하가 1순위로 꼽은 <strong>'{info['answers']['priority']}'</strong> 부분을
                    완벽하게 충족시켜 줄 수 있는 검증된 회원들입니다.
                </p>
                
                <div style='background:#e8eaf6; padding:15px; border-radius:10px; margin-top:20px; text-align:center;'>
                    <p style='color:#1a237e; font-weight:bold; margin:0;'>
                        현재 매칭 가능한 1차 리스트: <span style='font-size:1.4rem; color:#d4af37;'>{match_count}명</span>
                    </p>
                </div>
                
                <div style='margin-top:30px;'>
                    </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # CTA 버튼 (HTML 안에서 동작 안 하므로 밖으로 뺌)
        st.markdown("")
        if st.button(f"매칭된 {match_count}명의 비공개 프로필 무료로 받기 ➔"):
            st.balloons()
            st.success("✅ 신청 완료! 담당 커플 매니저가 24시간 내에 '비공개 프로필 리스트'를 보내드립니다.")
            
        if st.button("🔄 다시 진단하기"):
            st.session_state.page = 'input'
            st.rerun()
