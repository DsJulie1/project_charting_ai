from chart_part import run_chartting
import streamlit as st

# 레이아웃, 어플리케이션 탭 제목 및 아이콘 설정
st.set_page_config(layout="wide", page_title="한의원 상담 chart", page_icon=":alembic:")

st.title('	:alembic: 한의원 상담 chart')

st.write("상담 텍스트 파일을 넣어주세요.")
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file:
    result = run_chartting(uploaded_file)
    result_with_double_newline = result.replace('\n', '\n\n')
    st.info(result_with_double_newline)
    



