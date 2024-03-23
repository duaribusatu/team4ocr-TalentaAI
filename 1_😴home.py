import streamlit as st 
import pandas as pd 
import numpy as np
import seaborn as sns
import numpy as np 
import requests
from streamlit_lottie import st_lottie
from sklearn.datasets import load_wine
from PIL import Image 

#----start----
st.set_page_config(
    page_icon="😁",
    layout="wide")

#----sidebar-----
with st.sidebar:
    st.success("Select a page above.")

#----asset----
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()
food_asset = load_lottieurl("https://lottie.host/00e129df-818c-427c-9129-4a5cea5e56c9/bKL6AuUSWw.json")

# ----header section----
with st.container():
    left_column, right_column = st.columns(2)
    with left_column:
        st.subheader("hi, we are _team 4_ :wave:")
        st.write("##")
        st.title(":orange[_Capture Food:_] ur personal nutrition scanner 🍧")
        st.write("""
                 Discover the Nutritional Secrets of Your Food with our Nutrition Checker🥩
                                  
                 Menggunakan teknologi OCR untuk memprediksi kandungan nutrisi suatu makanan dari label nutrisinya
                 """)
        st.write("##")
        st.page_link("pages/3_📸OCR.py", label="Analyze your Food Now (Image)", icon="🔥")
        st.page_link("pages/2_🎲recipe.py", label="Analyze your Food Now (Recipe)", icon="🧀")

    with right_column:
        st.write("##")
        st.write("##")
        st_lottie(food_asset, height=350, key="food")
