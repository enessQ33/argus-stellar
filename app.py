import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from datetime import datetime

st.set_page_config(page_title="Argus Pro", layout="wide")

# CSS
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .card {
        background: #1a1a2e;
        border-radius: 15px;
        padding: 20px;
        border-left: 4px solid #8A2BE2;
    }
    .metric {
        color: white;
        font-size: 32px;
        font-weight: bold;
    }
    .label {
        color: #888;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# Session
if 'water' not in st.session_state:
    st.session_state.water = 0

# Sidebar
with st.sidebar:
    st.title("Argus Pro")
    
    st.subheader("Su Takibi")
    if st.button("+250ml"):
        st.session_state.water = min(st.session_state.water + 250, 3000)
    
    water_pct = (st.session_state.water / 3000) * 100
    st.progress(water_pct / 100)
    st.write(f"{st.session_state.water}ml / 3000ml")

# Ana ekran
st.title("Dashboard")

# Strava token al
try:
    if "STRAVA_CLIENT_ID" in st.secrets:
        r = requests.post("https://www.strava.com/oauth/token", data={
            'client_id': st.secrets["STRAVA_CLIENT_ID"],
            'client_secret': st.secrets["STRAVA_CLIENT_SECRET"],
            'refresh_token': st.secrets["STRAVA_REFRESH_TOKEN"],
            'grant_type': 'refresh_token'
        })
        
        if r.status_code == 200:
            token = r.json()['access_token']
            
            # Aktiviteleri al
            acts = requests.get(
                "https://www.strava.com/api/v3/athlete/activities",
                headers={"Authorization": f"Bearer {token}"},
                params={"per_page": 10}
            ).json()
            
            if acts:
                # Metrikler
                total_dist = sum(a.get('distance', 0) for a in acts) / 1000
                total_cal = sum(a.get('calories', 0) for a in acts)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                        <div class="card">
                            <div class="label">Toplam Mesafe</div>
                            <div class="metric">{total_dist:.1f} km</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                        <div class="card">
                            <div class="label">Toplam Kalori</div>
                            <div class="metric">{total_cal:.0f}</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                        <div class="card">
                            <div class="label">Aktivite</div>
                            <div class="metric">{len(acts)}</div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Aktivite bulunamadı")
        else:
            st.error(f"Strava hatası: {r.status_code}")
    else:
        st.warning("Strava bilgileri secrets'a eklenmemiş")
except Exception as e:
    st.error(f"Hata: {str(e)}")
