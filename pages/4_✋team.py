import streamlit as st 

st.set_page_config(
    page_icon="",
    layout="wide")

#----start-----
st.title("Meet our team⚽")
st.text("")

# ----mentor section----
with st.container():
    st.subheader("mentor")
    col1, col2, col3 = st.columns(3)
    
    with col2:
        st.image("D:\Talenta AI - OCR Web\cat3.jpeg", use_column_width="none", caption='Mentor')

# ----team AI section----
with st.container():
    st.subheader("team AI")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("D:\Talenta AI - OCR Web\image\cat1.jpeg", use_column_width="always", caption='Dandi Septiandi - Team 4 AI')
    with col2:
        st.image("D:\Talenta AI - OCR Web\image\cat2.jpeg", use_column_width="always", caption='Team 4 AI')
    with col3:
        st.image("D:\Talenta AI - OCR Web\image\cat3.jpeg", use_column_width="always", caption='Team 4 AI')

# ----team data section----
with st.container():
    st.subheader("team Data")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("D:\Talenta AI - OCR Web\cat1.jpeg", use_column_width="always", caption='Team 4 Data')
    with col2:
        st.image("D:\Talenta AI - OCR Web\cat2.jpeg", use_column_width="always", caption='Team 4 Data')
    with col3:
        st.image("D:\Talenta AI - OCR Web\cat3.jpeg", use_column_width="always", caption='Team 4 Data')

# ----team cyber section----
with st.container():
    st.subheader("team Cybersecurity")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("D:\Talenta AI - OCR Web\cat1.jpeg", use_column_width="always", caption='Team 4 Cyber')
    with col2:
        st.image("D:\Talenta AI - OCR Web\cat2.jpeg", use_column_width="always", caption='Team 4 Cyber')
    with col3:
        st.image("D:\Talenta AI - OCR Web\cat3.jpeg", use_column_width="always", caption='Team 4 Cyber')