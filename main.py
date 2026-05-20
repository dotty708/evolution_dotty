import streamlit as st
import random
import time

# 1. 페이지 기본 설정 (웹 브라우저 탭에 표시될 이름과 아이콘)
st.set_page_config(
    page_title="각성 도티의 다이아몬드 999개 캐기!!",
    page_icon="💎",
    layout="centered"
)

# 2. 게임 데이터 저장을 위한 Session State 초기화
# (새로고침이 되어도 여태까지 모은 다이아몬드와 클릭 횟수를 기억합니다!)
if 'diamonds' not in st.session_state:
    st.session_state.diamonds = 0
if 'clicks' not in st.session_state:
    st.session_state.clicks = 0
if 'log' not in st.session_state:
    st.session_state.log = []

# 3. 타이틀 및 오프닝 꾸미기
st.markdown("<h1 style='text-align: center; color: #00F0FF;'>⚡ 각성 도티의 다이아몬드 999개 캐기!! ⚡</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #E0E0E0;'>“여러분 안녕~ 오늘은 다이아몬드 999개를 캐볼 거에요!!😁”</h3>", unsafe_allow_html=True)
st.write("---")

# 4. 사이드바 (도티의 실시간 인벤토리 정보)
with st.sidebar:
    st.header("🎒 도티의 인벤토리")
    st.metric(label="💎 보유한 다이아몬드", value=f"{st.session_state.diamonds} / 999")
    st.metric(label="⛏️ 곡괭이질 횟수", value=f"{st.session_state.clicks}회")
    
    # 처음부터 다시 하고 싶을 때 사용할 리셋 버튼
    if st.button("🔄 게임 초기화"):
        st.session_state.diamonds = 0
        st.session_state.clicks = 0
        st.session_state.log = []
        st.rerun()

# 5. 진행도 표시 (수집한 다이아몬드의 백분율 프로그레스 바)
progress_percentage = min(st.session_state.diamonds / 999, 1.0)
st.subheader("📊 다이아몬드 목표 진행도")
st.progress(progress_percentage)
st.write(f"현재 목표 달성률: **{progress_percentage * 100:.1f}%**")

# 6. 메인 게임 영역 (화면을 가로로 분할하여 시각 효과 극대화)
col1, col2 = st.columns([1, 1.2])

with col1:
    # 멋진 네온 박스로 마이닝 구역 시각화
    st.markdown("""
    <div style="background-color: #1E1E1E; padding: 25px; border-radius: 15px; border: 2px solid #00F0FF; text-align: center;">
        <h1 style="font-size: 70px; margin: 0;">⛏️</h1>
        <h3 style="color: #00F0FF; margin-top: 10px;">신비한 광산</h3>
        <p style="color: #888888; font-size: 13px;">돌을 깰 때마다 무언가 일어납니다!</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.write("### 🔥 곡괭이를 휘두르세요!")
    st.write("버튼을 누르면 랜덤하게 다이아몬드를 발견합니다. 대박 광맥이 터질 수도 있지만, 크리퍼를 조심하세요!")
    
    # 광질하기 버튼 클릭 시 동작하는 로직
    if st.button("💥 광산 캐기!! ⛏️", use_container_width=True):
        st.session_state.clicks += 1
        
        # 확률에 따른 다양한 이벤트 발생!
        event = random.randint(1, 100)
        
        if event <= 12:  # 12% 확률로 잭팟!
            mined = random.randint(50, 120)
            st.session_state.diamonds += mined
            st.session_state.log.insert(0, f"💎 **초대박!** 전설의 다이아 광맥 발견! **+{mined}개**")
            st.balloons()  # 화면에 축하 풍선 날리기!
            
        elif event <= 40:  # 28% 확률로 많이 캐기
            mined = random.randint(15, 45)
            st.session_state.diamonds += mined
            st.session_state.log.insert(0, f"✨ 반짝이는 광석들을 무더기로 캐냈습니다! **+{mined}개**")
            
        elif event <= 85:  # 45% 확률로 일반 마이닝
            mined = random.randint(2, 9)
            st.session_state.diamonds += mined
            st.session_state.log.insert(0, f"⛏️ 영차영차! 돌 속에서 다이아를 찾아냈습니다. **+{mined}개**")
            
        else:  # 15% 확률로 꽝(크리퍼의 습격!)
            lost = random.randint(10, 30)
            if st.session_state.diamonds >= lost:
                st.session_state.diamonds -= lost
                st.session_state.log.insert(0, f"💥 **크리퍼 출현!!** 콰광! 다이아몬드를 **-{lost}개** 잃었습니다...😭")
            else:
                st.session_state.diamonds = 0
                st.session_state.log.insert(0, "💥 크리퍼가 나타나 다이아몬드가 전부 터져 날아갔습니다! 😭")
            st.snow()  # 먼지가 휘날리는 효과를 위해 눈 내리는 효과 사용!

        # 목표 999개 달성 체크!
        if st.session_state.diamonds >= 999:
            st.session_state.diamonds = 999  # 999개로 고정
            st.success("👑 축하합니다! 각성 도티가 마침내 다이아몬드 999개를 모두 모아 광부왕이 되었습니다! 🎉")
            st.balloons()
            time.sleep(0.5)
            st.balloons()
        
        # 화면 새로고침하여 누적치 바로 반영하기
        st.rerun()

# 7. 실시간 모험 일지 (로그 기록 출력)
st.write("---")
st.subheader("📜 도티의 모험 일지")
if st.session_state.log:
    # 최근 5개의 행동만 보여주어 화면 깔끔하게 유지
    for entry in st.session_state.log[:5]:
        st.write(entry)
else:
    st.write("아직 광질을 시작하지 않았습니다. 위에서 곡괭이 버튼을 눌러보세요!")
