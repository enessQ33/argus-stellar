import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Argus | Kişisel Sağlık Üssü",
    page_icon="https://img.icons8.com/ios-filled/50/shield.png", # Kalkan ikonu
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- TEMA VE STİL (CSS) ---
# Font Awesome ikon kütüphanesini ekle
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
    .main {
        border-radius: 10px;
    }
    .stMetric {
        background-color: rgba(138, 43, 226, 0.1);
        padding: 15px;
        border-radius: 15px;
        border: 1px solid #8A2BE2;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .metric-icon {
        font-size: 2em;
        color: #8A2BE2;
    }
    h1 {
        color: #8A2BE2;
        text-align: center;
    }
    .stSelectbox label, .stTextInput label, .stNumberInput label, .stSlider label {
        color: #8A2BE2;
    }
    </style>
    """, unsafe_allow_html=True)

# --- YAN PANEL (SETTINGS) ---
with st.sidebar:
    st.image("https://img.icons8.com/ios-filled/100/shield.png", width=80) # Daha keskin kalkan
    st.markdown("<h2 style='color: #8A2BE2;'>⚙️ Argus Ayarlar</h2>", unsafe_allow_html=True)
    
    tema = st.selectbox("🎨 Görünüm Teması", ["Karanlık Tema", "Aydınlık Tema"])
    
    st.markdown("---")
    st.markdown("<h3 style='color: #8A2BE2;'>👤 Profil Verileri</h3>", unsafe_allow_html=True)
    user_name = st.text_input("İsim", "Enes")
    boy = st.number_input("Boy (cm)", value=180)
    kilo = st.number_input("Kilo (kg)", value=75)
    yas = st.slider("Yaş", 15, 100, 20)
    
    st.markdown("---")
    st.markdown("<h3 style='color: #8A2BE2;'>🎯 Hedefler</h3>", unsafe_allow_html=True)
    adim_hedef = st.number_input("Günlük Adım Hedefi", value=10000, step=500)

# --- BMI HESAPLAMA ---
bmi = kilo / ((boy/100)**2)

# --- ANA EKRAN ---
st.markdown(f"<h1><i class='fa-solid fa-shield-halved'></i> ARGUS KONTROL PANELİ</h1>", unsafe_allow_html=True)
st.subheader(f"👋 Merhaba {user_name},")
st.write(f"📅 Bugün: {datetime.now().strftime('%d %B %Y')}")

# --- ÜST METRİK KARTLARI (İKONLU) ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stMetric">
        <i class="metric-icon fa-solid fa-person-walking"></i>
        <div>
            <div style="font-size: 0.8em; color: gray;">Günlük Adım</div>
            <div style="font-size: 1.5em; font-weight: bold;">12,450</div>
            <div style="font-size: 0.7em; color: green;">↑ %15</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="stMetric">
        <i class="metric-icon fa-solid fa-heart-pulse"></i>
        <div>
            <div style="font-size: 0.8em; color: gray;">Ort. Nabız</div>
            <div style="font-size: 1.5em; font-weight: bold;">72 <span style='font-size:0.6em;'>BPM</span></div>
            <div style="font-size: 0.7em; color: orange;">Normal</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="stMetric">
        <i class="metric-icon fa-solid fa-bed"></i>
        <div>
            <div style="font-size: 0.8em; color: gray;">Uyku Süresi</div>
            <div style="font-size: 1.5em; font-weight: bold;">7s 20dk</div>
            <div style="font-size: 0.7em; color: green;">Kaliteli</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="stMetric">
        <i class="metric-icon fa-solid fa-weight-scale"></i>
        <div>
            <div style="font-size: 0.8em; color: gray;">VKI (BMI)</div>
            <div style="font-size: 1.5em; font-weight: bold;">{bmi:.1f}</div>
            <div style="font-size: 0.7em; color: blue;">İdeal Aralık</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- GRAFİKLER BÖLÜMÜ ---
c1, c2 = st.columns([2, 1])

with c1:
    st.markdown("<h3 style='color: #8A2BE2;'><i class='fa-solid fa-chart-line'></i> Günlük Hareket Analizi</h3>", unsafe_allow_html=True)
    df = pd.DataFrame({
        'Saat': ['08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00'],
        'Adım': [200, 1500, 4500, 6000, 8500, 10000, 11500, 12450]
    })
    fig_line = px.area(df, x='Saat', y='Adım', title="Adım İlerleme Grafiği", 
                        color_discrete_sequence=['#8A2BE2'])
    fig_line.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color="#333333" if tema == "Aydınlık Tema" else "white")
    st.plotly_chart(fig_line, use_container_width=True)

with c2:
    st.markdown("<h3 style='color: #8A2BE2;'><i class='fa-solid fa-moon'></i> Uyku Evreleri</h3>", unsafe_allow_html=True)
    labels = ['Derin Uyku', 'Hafif Uyku', 'REM']
    values = [2.5, 4, 0.8]
    fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, marker_colors=['#8A2BE2', '#DDA0DD', '#FF69B4'])])
    fig_pie.update_layout(showlegend=True, paper_bgcolor='rgba(0,0,0,0)', font_color="#333333" if tema == "Aydınlık Tema" else "white")
    st.plotly_chart(fig_pie, use_container_width=True)

# --- AKILLI ANALİZ ---
st.markdown("---")
st.markdown("<h3 style='color: #8A2BE2;'><i class='fa-solid fa-brain'></i> Argus Akıllı Analiz</h3>", unsafe_allow_html=True)

if bmi > 25:
    st.warning(f"🚨 **Analiz:** Enes, BMI değerin biraz yüksek. Akşam dükkan kapanışında 30 dakika yürüyüş öneriyorum.")
elif 18.5 <= bmi <= 24.9:
    st.success(f"✅ **Analiz:** Formun harika! Vücut verilerin jilet gibi. Bugün o tıraşları sanat eseri gibi yapacaksın.")
else:
    st.info(f"💪 **Analiz:** Kilo alman gerekiyor kanka. Beslenmene dikkat et, protein ağırlıklı git.")

# Alt Bilgi
st.caption("Argus Sağlık Paneli | Google Health API Entegrasyonu Yakında")

# Tema değiştirme için CSS
if tema == "Karanlık Tema":
    st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    h1, h2, h3, h4, h5, h6, .stMarkdown, p, label { color: white !important; }
    .stSelectbox label, .stTextInput label, .stNumberInput label, .stSlider label { color: white !important; }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #333333; }
    h1, h2, h3, h4, h5, h6, .stMarkdown, p, label { color: #333333 !important; }
    .stSelectbox label, .stTextInput label, .stNumberInput label, .stSlider label { color: #8A2BE2 !important; }
    </style>
    """, unsafe_allow_html=True)
