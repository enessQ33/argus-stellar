import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Argus | Kişisel Sağlık Üssü",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- TEMA VE STİL (CSS) ---
# Beyaz ve Siyah tema seçeneğine göre renkleri dinamik ayarlar
st.markdown("""
    <style>
    .main {
        border-radius: 10px;
    }
    .stMetric {
        background-color: rgba(138, 43, 226, 0.1);
        padding: 15px;
        border-radius: 15px;
        border: 1px solid #8A2BE2;
    }
    </style>
    """, unsafe_allow_html=True)

# --- YAN PANEL (SETTINGS) ---
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/shield.png", width=100)
    st.title("🛡️ Argus Ayarlar")
    
    tema = st.selectbox("🎨 Görünüm Teması", ["Karanlık Tema", "Aydınlık Tema"])
    
    st.markdown("---")
    st.subheader("👤 Profil Verileri")
    user_name = st.text_input("İsim", "Enes")
    boy = st.number_input("Boy (cm)", value=180)
    kilo = st.number_input("Kilo (kg)", value=75)
    yas = st.slider("Yaş", 15, 100, 20)
    
    st.markdown("---")
    st.subheader("🎯 Hedefler")
    adim_hedef = st.number_input("Günlük Adım", value=10000, step=500)

# --- BMI HESAPLAMA ---
bmi = kilo / ((boy/100)**2)

# --- ANA EKRAN ---
st.title(f"Merhaba {user_name},")
st.write(f"📅 Bugün: {datetime.now().strftime('%d %B %Y
                                             
