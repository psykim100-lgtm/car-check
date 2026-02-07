import streamlit as st

# 페이지 설정 (앱 이름과 아이콘)
st.set_page_config(page_title="차량 판독기", page_icon="🚗")

# 스타일 설정 (글씨 크기를 크게 만드는 CSS)
st.markdown("""
    <style>
    .big-font { font-size:50px !important; font-weight: bold; }
    .medium-font { font-size:30px !important; }
    </style>
    """, unsafe_allow_html=True)

def load_car_data():
    car_dict = {}
    try:
        # 파일명을 본인의 txt 파일명과 맞춰주세요
        with open('numbers.txt', 'r', encoding='utf-8') as f:
            for line in f:
                full_num = line.strip()
                if len(full_num) >= 4:
                    car_dict[full_num[-4:]] = full_num
        return car_dict
    except FileNotFoundError:
        return None

# 데이터 로드
car_data = load_car_data()

st.title("🚗 차량 출입 판독기")

if car_data is None:
    st.error("numbers.txt 파일을 찾을 수 없습니다.")
else:
    # 입력창 (글씨가 잘 보이도록 설명 추가)
    user_input = st.text_input("차량번호 뒷 4자리를 입력하세요", max_chars=4)

    if st.button("조회하기") or user_input:
        if len(user_input) == 4 and user_input.isdigit():
            if user_input in car_data:
                full_num = car_data[user_input]
                st.success("확인되었습니다!")
                st.markdown(f'<p class="big-font">✅ 직원차량</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="medium-font">전체번호: {full_num}</p>', unsafe_allow_html=True)
            else:
                st.error("미등록 차량입니다.")
                st.markdown(f'<p class="big-font">❌ 외부차량</p>', unsafe_allow_html=True)
        elif user_input:
            st.warning("숫자 4자리를 정확히 입력해주세요.")

# 하단에 현재 등록된 대수 표시
if car_data:
    st.caption(f"현재 데이터베이스에 {len(car_data)}대의 차량이 등록되어 있습니다.")