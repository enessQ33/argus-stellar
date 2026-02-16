import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Argus | Kişisel Sağlık Üssü",
    page_icon="https://img.icons8.com/ios-filled/50/shield.png",
    layout="wide"
)

# --- FONT AWESOME VE STİL ---
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
    .stMetric {
        background-color: rgba(138, 43, 226, 0.1);
        padding: 15px;
        border-radius: 15px;
        border: 1px solid #8A2BE2;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .metric-icon { font-size: 2.2em; color: #8A2BE2; }
    h1, h2, h3 { color: #8A2BE2 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- GOOGLE SECRETS KONTROL ---
CLIENT_ID = st.secrets.get("GOOGLE_CLIENT_ID")
CLIENT_SECRET = st.secrets.get("GOOGLE_CLIENT_SECRET")
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# --- YAN PANEL ---
with st.sidebar:
    st.image("https://img.icons8.com/ios-filled/100/shield.png", width=80)
    st.markdown("<h3><i class='fa-solid fa-gears'></i> Ayarlar</h3>", unsafe_allow_html=True)
    user_name = st.text_input("İsim", "Enes")
    
    st.markdown("---")
    if st.button("🔌 Google Fit Bağla"):
        st.info("Google Fit bağlantısı başlatılıyor... (Redirect URI hatası alırsan linki kopyalayıp Cloud'a ekle)")

# --- ANA PANEL BAŞLIK ---
st.markdown(f"<h1><i class='fa-solid fa-shield-halved'></i> ARGUS KONTROL PANELİ</h1>", unsafe_allow_html=True)
st.markdown(f"<h3><i class='fa-solid fa-circle-user'></i> Merhaba {user_name}</h3>", unsafe_allow_html=True)
st.write(f"📅 Tarih: {datetime.now().strftime('%d %B %Y')}")

# --- METRİKLER ---
col1, col2, col3, col4 = st.columns(4)

# Gerçek veri gelene kadar temsililer ama ikonlar tam profesyonel
metrics = [
    {"label": "Günlük Adım", "val": "12,450", "icon": "fa-person-walking", "delta": "↑ %15"},
    {"label": "Ort. Nabız", "val": "72 BPM", "icon": "fa-heart-pulse", "delta": "Normal"},
    {"label": "Uyku Süresi", "val": "7s 20dk", "icon": "fa-bed", "delta": "Kaliteli"},
    {"label": "VKI (BMI)", "val": "23.1", "icon": "fa-weight-scale", "delta": "İdeal"}
]

cols = [col1, col2, col3, col4]
for i, m in enumerate(metrics):
    with cols[i]:
        st.markdown(f"""
        <div class="stMetric">
            <i class="metric-icon fa-solid {m['icon']}"></i>
            <div>
                <div style="font-size: 0.8em; color: gray;">{m['label']}</div>
                <div style="font-size: 1.5em; font-weight: bold;">{m['val']}</div>
                <div style="font-size: 0.7em; color: #8A2BE2;">{m['delta']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- GRAFİKLER ---
st.markdown("---")
c1, c2 = st.columns([2, 1])

with c1:
    st.markdown("<h3><i class='fa-solid fa-chart-area'></i> Hareket Analizi</h3>", unsafe_allow_html=True)
    df = pd.DataFrame({'S': range(8,23,2), 'A': [200, 1500, 4500, 7000, 9500, 11000, 12450, 12450]})
    fig = px.area(df, x='S', y='A', color_discrete_sequence=['#8A2BE2'])
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown("<h3><i class='fa-solid fa-circle-info'></i> Durum Bilgisi</h3>", unsafe_allow_html=True)
    st.info("Şu an örnek veriler gösteriliyor. Google Fit butonuna basarak canlı verilerini çekebilirsin.")
    st.markdown(f"""
        <div style='border: 1px solid #8A2BE2; padding: 10px; border-radius: 10px;'>
            <i class="fa-solid fa-lightbulb" style="color: #8A2BE2;"></i> 
            <b>Tavsiye:</b> Bugün dükkanda çok ayakta kaldın kanka, akşam güzel bir dinlenmeyi hak ettin.
        </div>
    """, unsafe_allow_html=True)
    
