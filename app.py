import streamlit as st

# 페이지 설정
st.set_page_config(page_title="차량 판독기", page_icon="🚗")

# 스타일 설정
st.markdown("""
    <style>
    .big-font { font-size:50px !important; font-weight: bold; }
    .medium-font { font-size:50px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 비밀번호 확인 함수 ---
def check_password():
    """비밀번호가 맞으면 True를 반환합니다."""
    def password_entered():
        # 본인이 사용할 비밀번호를 입력하세요
        if st.session_state["password"] == "1234": 
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # 보안을 위해 세션에서 비밀번호 삭제
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # 로그인 전 화면
        st.title("🔒 보안 인증")
        st.text_input("액세스 비밀번호를 입력하세요", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        # 비밀번호가 틀렸을 때
        st.title("🔒 보안 인증")
        st.text_input("액세스 비밀번호를 입력하세요", type="password", on_change=password_entered, key="password")
        st.error("비밀번호가 틀렸습니다. 다시 시도해주세요.")
        return False
    else:
        # 인증 성공
        return True

def load_car_data():
    car_dict = {}
    try:
        with open('numbers.txt', 'r', encoding='utf-8') as f:
            for line in f:
                full_num = line.strip()
                if len(full_num) >= 4:
                    car_dict[full_num[-4:]] = full_num
        return car_dict
    except FileNotFoundError:
        return None

# --- 메인 로직 시작 ---
if check_password():
    # 데이터 로드
    car_data = load_car_data()

    st.markdown('<p class="big-font">🚗 차량 판독기</p>', unsafe_allow_html=True)
    
    # 로그아웃 버튼 (선택사항)
    if st.sidebar.button("로그아웃"):
        st.session_state["password_correct"] = False
        st.rerun()

    if car_data is None:
        st.error("numbers.txt 파일을 찾을 수 없습니다.")
    else:
        st.markdown('<p class="medium-font">차량번호 뒷 4자리를 입력하세요</p>', unsafe_allow_html=True)
        user_input = st.text_input("", max_chars=4, key="car_input")
        import streamlit.components.v1 as components

components.html(
    """
    <script>
    var input = window.parent.document.querySelectorAll('input[type="text"]');
    for (var i = 0; i < input.length; i++) {
        input[i].setAttribute('inputmode', 'numeric');
        input[i].setAttribute('pattern', '[0-9]*');
    }
    </script>
    """,
    height=0,
)

        if st.button("조회하기") or user_input:
            if len(user_input) == 4 and user_input.isdigit():
                if user_input in car_data:
                    full_num = car_data[user_input]
                    st.success("확인되었습니다!")
                    st.markdown(f'<p class="big-font">✅ 직원차량</p>', unsafe_allow_html=True)
                    st.markdown(f'<p class="medium-font"> {full_num}</p>', unsafe_allow_html=True)
                else:
                    st.error("미등록 차량입니다.")
                    st.markdown(f'<p class="big-font">❌ 외부차량</p>', unsafe_allow_html=True)
            elif user_input:
                st.warning("숫자 4자리를 정확히 입력해주세요.")

    if car_data:
        st.caption(f"현재 데이터베이스에 {len(car_data)}대의 차량이 등록되어 있습니다.")








