import streamlit as st
import plotly.graph_objects as go
import time
import random
import datetime

# ==========================================
# [1. 시스템 설정 및 디자인]
# ==========================================
st.set_page_config(
    page_title="IMD 매치메이커 AI",
    page_icon="💍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 럭셔리 & 로맨틱 테마 (핑크/골드/네이비)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    .stApp {
        background-color: #fdfbf7; /* 따뜻한 아이보리 */
        color: #2c3e50;
    }

    /* 상단 배너 */
    .news-ticker {
        background: #1a237e; /* 딥 네이비 */
        border-left: 4px solid #d4af37; /* 골드 */
        color: #fff;
        padding: 12px 20px;
        font-size: 0.9rem;
        border-radius: 4px;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        letter-spacing: 0.5px;
    }

    /* 신뢰 배지 */
    .trust-badges {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin: 20px 0;
        flex-wrap: wrap;
    }
    .badge {
        background: #fff;
        border: 1px solid #d4af37;
        color: #d4af37;
        padding: 8px 18px;
        border-radius: 25px;
        font-size: 0.85rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 6px;
        box-shadow: 0 2px 5px rgba(212, 175, 55, 0.2);
    }

    /* 채팅 컨테이너 */
    .chat-container {
        max-width: 750px;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        gap: 15px;
        padding-bottom: 50px;
    }
    
    .bot-message {
        background-color: #fff;
        border: 1px solid #e0e0e0;
        border-left: 3px solid #ff6b6b; /* 로맨틱 핑크 */
        border-radius: 0 15px 15px 15px;
        color: #333;
        padding: 18px;
        font-size: 1rem;
        line-height: 1.6;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        animation: fadeIn 0.6s ease-out;
        max-width: 90%;
    }
    
    .user-message {
        background: linear-gradient(135deg, #ff8a80, #ff6b6b);
        color: #fff;
        padding: 15px 25px;
        border-radius: 15px 0 15px 15px;
        align-self: flex-end;
        margin-left: auto;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(255, 107, 107, 0.3);
        animation: fadeIn 0.6s ease-out;
        max-width: 80%;
        text-align: right;
    }

    .phase-tag {
        font-size: 0.75rem;
        color: #999;
        margin-bottom: 6px;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 700;
    }

    /* 최종 리포트 대시보드 */
    .final-dashboard {
        background-color: #fff;
        border: 1px solid #d4af37;
        border-radius: 15px;
        padding: 30px;
        margin-top: 30px;
        box-shadow: 0 10px 30px rgba(212, 175, 55, 0.15);
    }
    
    .kpi-box {
        background-color: #fcfcfc;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #eee;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 900;
        color: #1a237e;
    }
    .kpi-label {
        font-size: 0.85rem;
        color: #777;
        margin-top: 5px;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        background-color: #fff;
        color: #2c3e50;
        border: 1px solid #ccc;
        border-radius: 8px;
        padding: 12px;
        font-size: 1rem;
        transition: all 0.3s;
        width: 100%;
    }
    .stButton > button:hover {
        border-color: #ff6b6b;
        color: #ff6b6b;
        background-color: #fff5f5;
    }

    /* 최종 CTA 버튼 */
    .final-cta-button {
        background: linear-gradient(90deg, #1a237e, #283593);
        color: #fff;
        border: none;
        padding: 18px 40px;
        font-weight: 700;
        font-size: 1.1rem;
        border-radius: 50px;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(26, 35, 126, 0.3);
        transition: transform 0.2s;
        display: block;
        margin: 0 auto;
        text-align: center;
        text-decoration: none;
    }
    .final-cta-button:hover {
        transform: translateY(-2px);
    }

    /* 입력창 자동 포커스 */
    .stTextInput > div > div > input {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# [2. 로직 및 차트 함수]
# ==========================================

def create_match_chart(user_data):
    """5각 매칭 분석 레이더 차트"""
    # 입력 데이터 기반 가상 점수 산정 (시뮬레이션 로직)
    
    # 경제력: 전문직/대기업이면 높게
    job_score = 90 if any(x in user_data.get('job', '') for x in ['전문직', '사업가', '대기업']) else 70
    
    # 성격/가치관: MBTI나 성향에 따라 다르게 (여기선 랜덤성 부여하되 높게)
    personality_score = 80
    
    # 외모/스타일: 입력값은 없지만 자신감 점수로 가정
    appearance_score = 75 
    
    # 가정환경/배경
    family_score = 85 if "화목" in user_data.get('background', '') else 70

    # 매칭 가능성 (종합)
    overall_match = (job_score + personality_score + appearance_score + family_score) / 4 + 5

    categories = ['경제적 안정성', '성격/가치관', '외모/스타일', '가정 환경', '결혼 의지']
    values = [job_score, personality_score, appearance_score, family_score, 95] # 결혼 의지는 높게 설정
    values += [values[0]]
    categories += [categories[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(255, 107, 107, 0.2)',
        line=dict(color='#ff6b6b', width=2),
        marker=dict(color='#1a237e', size=4),
    ))
    
    fig.update_layout(
        polar=dict(
            bgcolor='#fff',
            radialaxis=dict(visible=True, range=[0, 100], color='#aaa', gridcolor='#eee'),
            angularaxis=dict(color='#333', gridcolor='#eee')
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(t=30, b=30, l=30, r=30),
        height=350,
        title=dict(
            text="AI 매칭 경쟁력 분석",
            font=dict(size=15, color='#333'),
            x=0.5
        )
    )
    return fig

# 가상 멤버십 라인업
membership_tiers = {
    "노블레스 (Noblesse)": {
        "desc": "전문직, 대기업, 공무원 등 안정적인 경제력을 갖춘 회원을 위한 스탠다드 클래스.",
        "pool": "의사, 변호사, 회계사, 대기업 재직자 등",
        "price": "300~500만원 대"
    },
    "로얄 (Royal)": {
        "desc": "자산가, CEO, 명문가 자제 등 상위 10% 회원을 위한 프리미엄 매칭 클래스.",
        "pool": "300억 이상 자산가, 기업 오너 2세, 고위 공직자 자녀",
        "price": "1,000만원 대 ~"
    },
    "블랙 (Black)": {
        "desc": "철저한 비공개 심사를 통과한 최상위 VVIP만을 위한 시크릿 매칭.",
        "pool": "비공개 (최상위 엘리트 그룹)",
        "price": "별도 문의 (Private)"
    }
}

# 질문 시나리오
questions = [
    {
        "phase": "STEP 1. BASIC PROFILE",
        "question": "반갑습니다. **IMD 매치메이커 AI**입니다.\n빅데이터 매칭 알고리즘을 통해 귀하의 **'결혼 점수'**와 **'최적의 배우자 그룹'**을 진단합니다.\n\n먼저, 귀하의 **성별**과 **생년월일(나이)**을 입력해 주세요.",
        "key": "age_gender",
        "type": "text",
        "confirm": "기본 프로필 확인되었습니다. 매칭 풀(Pool)을 스캐닝합니다."
    },
    {
        "phase": "STEP 2. SOCIAL STATUS",
        "question": "결혼 매칭에서 중요한 **직업군**과 대략적인 **연봉 대**를 선택해 주세요.\n(이 정보는 매칭 정확도를 위해 암호화되어 처리됩니다.)",
        "key": "job",
        "type": "select",
        "options": ["전문직 (의사/변호사/약사 등)", "대기업/공기업/외국계", "사업가/CEO", "공무원/교사", "일반 사무직/기타", "프리랜서/예술"],
        "confirm": "사회적 지표 데이터가 입력되었습니다. **'{value}'** 그룹의 매칭 성공률을 계산 중입니다."
    },
    {
        "phase": "STEP 3. IDEAL TYPE",
        "question": "배우자를 선택할 때 **가장 중요하게 생각하는 가치 1순위**는 무엇입니까?",
        "key": "value_1",
        "type": "select",
        "options": ["경제력/능력", "외모/스타일", "성격/가치관", "가정환경/집안", "나이 차이"],
        "confirm": "**'{value}'** 데이터를 가중치 1순위로 설정했습니다."
    },
    {
        "phase": "STEP 4. LIFESTYLE",
        "question": "선호하는 **라이프스타일**이나 **성향**을 알려주세요. (예: 집돌이/집순이, 여행/레저 즐김, 자기계발 중시 등)",
        "key": "lifestyle",
        "type": "text",
        "confirm": "성향 분석이 완료되었습니다. 귀하와 라이프스타일 매칭도가 높은 그룹을 찾았습니다."
    },
    {
        "phase": "STEP 5. BACKGROUND",
        "question": "마지막으로, 본인이 생각하는 **가정 환경**이나 **종교적 성향**에 대해 간략히 말씀해 주실 수 있나요?",
        "key": "background",
        "type": "select",
        "options": ["무관/상관없음", "화목한 가정 중요", "특정 종교 선호", "비흡연/비음주 선호"],
        "confirm": "모든 진단 데이터 수집이 완료되었습니다. 15만 건의 성혼 데이터를 기반으로 최종 리포트를 생성합니다."
    }
]

# ==========================================
# [3. 메인 실행 코드]
# ==========================================

# 세션 상태
if 'step' not in st.session_state: st.session_state.step = 0
if 'history' not in st.session_state: st.session_state.history = []
if 'user_data' not in st.session_state: st.session_state.user_data = {}
if 'analyzed' not in st.session_state: st.session_state.analyzed = False

# 1. 헤더 영역
current_time = datetime.datetime.now().strftime("%H:%M")
news = [
    "30대 전문직 남성, IMD 매칭으로 3개월 만에 성혼",
    "이번 주 신규 가입: 의사/변호사 그룹 45명 입회",
    "AI 매칭 정확도 94% 달성 (업계 1위)",
    "지금 가입 시 '노블레스 등급' 무료 업그레이드 이벤트"
]
st.markdown(f"""
<div class='news-ticker'>
    <span style='color: #ffeb3b; font-weight:bold; margin-right: 10px;'>🔔 LIVE NEWS</span> {random.choice(news)}
</div>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #1a237e; font-size: 2.8rem; font-weight: 900;'>IMD Private Matchmaker</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555;'>빅데이터가 제안하는, 실패 없는 만남의 공식</p>", unsafe_allow_html=True)

st.markdown("""
<div class="trust-badges">
    <div class="badge">💎 신원 인증 100%</div>
    <div class="badge">🔒 시크릿 보장</div>
    <div class="badge">⚖️ AI 밸런스 매칭</div>
</div>
""", unsafe_allow_html=True)

st.divider()

# 2. 채팅 인터페이스
chat_placeholder = st.container()

with chat_placeholder:
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for idx, msg in enumerate(st.session_state.history):
        if msg['role'] == 'bot':
            st.markdown(f"""
            <div style='align-self: flex-start; width: 100%;'>
                <div class='phase-tag'>{msg.get('phase', '')}</div>
                <div class='bot-message'>{msg['text']}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='align-self: flex-end; width: 100%;'>
                <div class='user-message'>{msg['text']}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 3. 입력 및 로직
if st.session_state.step < len(questions):
    q = questions[st.session_state.step]
    
    # 봇 메시지 출력 (중복 방지)
    last_bot_msg = ""
    for m in reversed(st.session_state.history):
        if m['role'] == 'bot':
            last_bot_msg = m['text']
            break
            
    if q['question'] not in last_bot_msg:
        st.session_state.history.append({"role": "bot", "text": q['question'], "phase": q['phase']})
        st.rerun()

    # 입력 위젯
    with st.container():
        st.write("")
        
        if q['type'] == 'text':
            with st.form(key=f"form_{st.session_state.step}"):
                user_val = st.text_input("답변 입력", key=f"input_{st.session_state.step}")
                submit = st.form_submit_button("입력 ➔")
                
            if submit and user_val:
                st.session_state.history.append({"role": "user", "text": user_val})
                st.session_state.user_data[q['key']] = user_val
                
                with st.spinner("분석 중..."):
                    time.sleep(0.6)
                confirm_text = q['confirm'].format(value=user_val)
                st.session_state.history.append({"role": "bot", "text": confirm_text, "phase": "시스템 기록"})
                st.session_state.step += 1
                st.rerun()
                
        elif q['type'] == 'select':
            cols = st.columns(2)
            for idx, opt in enumerate(q['options']):
                with cols[idx % 2]:
                    if st.button(opt, key=f"btn_{st.session_state.step}_{idx}", use_container_width=True):
                        st.session_state.history.append({"role": "user", "text": opt})
                        st.session_state.user_data[q['key']] = opt
                        
                        with st.spinner("매칭 그룹 탐색 중..."):
                            time.sleep(0.6)
                        confirm_text = q['confirm'].format(value=opt)
                        st.session_state.history.append({"role": "bot", "text": confirm_text, "phase": "시스템 기록"})
                        st.session_state.step += 1
                        st.rerun()
    
    # 스크롤 확보
    st.markdown("<br>"*5, unsafe_allow_html=True)

# 4. 최종 결과 (리포트)
else:
    if not st.session_state.analyzed:
        with st.spinner("성혼 가능성 시뮬레이션 실행 중..."):
            time.sleep(1.5)
        st.session_state.analyzed = True
        st.rerun()

    # 데이터 가공
    ud = st.session_state.user_data
    
    # 등급 추천 로직
    job = ud.get('job', '')
    tier_name = "노블레스 (Noblesse)"
    if "전문직" in job or "사업가" in job:
        tier_name = "로얄 (Royal)"
    elif "대기업" in job:
        tier_name = "노블레스 (Noblesse)"
    
    tier_info = membership_tiers.get(tier_name, membership_tiers["노블레스 (Noblesse)"])
    
    # 결과 출력
    st.markdown("<div class='final-dashboard'>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='color: #1a237e; text-align: center;'>💎 IMD Premium Matching Report</h2>", unsafe_allow_html=True)
    st.write("")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""<div class='kpi-box'><div class='kpi-label'>나의 매칭 점수</div><div class='kpi-value' style='color:#ff6b6b;'>88점</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class='kpi-box'><div class='kpi-label'>추천 등급</div><div class='kpi-value'>{tier_name.split(' ')[0]}</div></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class='kpi-box'><div class='kpi-label'>성혼 예상 기간</div><div class='kpi-value'>5개월</div></div>""", unsafe_allow_html=True)
        
    st.divider()
    
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown("### 📊 매칭 경쟁력 분석")
        fig = create_match_chart(ud)
        st.plotly_chart(fig, use_container_width=True)
        
    with c2:
        st.markdown("### 📝 AI Logic Trace (진단 근거)")
        st.markdown(f"""
        <div style='background: #f9f9f9; padding: 20px; border-radius: 10px; line-height: 1.8; border: 1px solid #e0e0e0; color: #333;'>
            <span style='color: #1a237e; font-weight:bold;'>[SPEC]</span> 직업군 <strong>'{job}'</strong> 확인 → 경제적 안정성 점수 상향<br>
            <span style='color: #1a237e; font-weight:bold;'>[NEEDS]</span> 중요 가치 <strong>'{ud.get('value_1', '가치관')}'</strong> 분석 → 매칭 알고리즘 필터링 적용<br>
            <span style='color: #1a237e; font-weight:bold;'>[MATCH]</span> <strong>'{ud.get('lifestyle', '성향')}'</strong> 성향과 매칭도 높은 <strong>[전문직/안정적]</strong> 그룹 추출<br>
            <hr style='border-color: #ddd;'>
            <strong style='color: #d4af37; font-size: 1.2rem;'>💡 최종 매칭 전략</strong><br>
            귀하의 스펙과 이상형을 고려할 때, 일반 매칭보다는<br>
            <strong>[{tier_name}]</strong> 멤버십을 통한 비공개 매칭이 성혼 확률을 <strong>2.5배</strong> 높입니다.
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown(f"""
    <div style='background: #1a237e; color: white; padding: 20px; border-radius: 10px; margin-top: 20px;'>
        <h3 style='color: #d4af37; margin:0;'>🏆 추천: {tier_name}</h3>
        <p style='color: #ccc; margin-top:5px;'>{tier_info['desc']}</p>
        <ul style='line-height: 1.8;'>
            <li><strong>매칭 풀:</strong> {tier_info['pool']}</li>
            <li><strong>예상 가입비:</strong> {tier_info['price']}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; margin-top: 30px;'>
        <a class='final-cta-button' href='#'>
            내 등급으로 매칭 가능한 이성 프로필 받기 (무료) ➔
        </a>
        <p style='color: #888; font-size: 0.8rem; margin-top: 10px;'>* 개인정보는 상담 목적 외에 사용되지 않습니다.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
