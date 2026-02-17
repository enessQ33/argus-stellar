import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from datetime import datetime
import time

# -------------------- KONFİGÜRASYON --------------------
st.set_page_config(
    page_title="Argus Pro v3",
    page_icon="◈",
    layout="wide"
)

# -------------------- ÖZEL CSS --------------------
st.markdown("""
<style>
    .stApp { background: #0A0A0F; }
    .stat-card {
        background: rgba(20, 20, 30, 0.95);
        border: 1px solid rgba(138, 43, 226, 0.15);
        border-radius: 24px;
        padding: 1.8rem 1.5rem;
    }
    .stat-value {
        font-size: 2.8rem;
        font-weight: 500;
        color: #FFFFFF;
        margin: 0.5rem 0;
    }
    .stat-label {
        font-size: 0.85rem;
        color: #6B6B7B;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    .progress-container {
        background: rgba(30, 30, 40, 0.8);
        border-radius: 100px;
        height: 6px;
        margin: 1rem 0;
    }
    .progress-bar {
        background: #8A2BE2;
        height: 100%;
        border-radius: 100px;
    }
    .title {
        font-size: 2.2rem;
        color: #FFFFFF;
        font-weight: 500;
    }
    .error-box {
        background: rgba(255, 75, 75, 0.1);
        border: 1px solid rgba(255, 75, 75, 0.3);
        border-radius: 12px;
        padding: 1rem;
        color: #ff4b4b;
    }
</style>
""", unsafe_allow_html=True)

# -------------------- SESSION STATE --------------------
if 'water' not in st.session_state:
    st.session_state.water = 0
if 'token' not in st.session_state:
    st.session_state.token = None
if 'activities' not in st.session_state:
    st.session_state.activities = None
if 'error' not in st.session_state:
    st.session_state.error = None

# -------------------- STRAVA --------------------
def get_token():
    try:
        # Secrets kontrolü
        if "STRAVA_CLIENT_ID" not in st.secrets:
            st.session_state.error = "STRAVA_CLIENT_ID secrets'da yok"
            return None
        if "STRAVA_CLIENT_SECRET" not in st.secrets:
            st.session_state.error = "STRAVA_CLIENT_SECRET secrets'da yok"
            return None
        if "STRAVA_REFRESH_TOKEN" not in st.secrets:
            st.session_state.error = "STRAVA_REFRESH_TOKEN secrets'da yok"
            return None
            
        r = requests.post("https://www.strava.com/oauth/token", data={
            'client_id': st.secrets["STRAVA_CLIENT_ID"],
            'client_secret': st.secrets["STRAVA_CLIENT_SECRET"],
            'refresh_token': st.secrets["STRAVA_REFRESH_TOKEN"],
            'grant_type': 'refresh_token'
        })
        
        if r.status_code == 200:
            st.session_state.error = None
            return r.json()['access_token']
        else:
            st.session_state.error = f"Strava token hatası: {r.status_code}"
            return None
    except Exception as e:
        st.session_state.error = f"Bağlantı hatası: {str(e)}"
        return None

def get_activities():
    if not st.session_state.token:
        st.session_state.token = get_token()
        if not st.session_state.token:
            return None
    
    try:
        r = requests.get(
            "https://www.strava.com/api/v3/athlete/activities",
            headers={"Authorization": f"Bearer {st.session_state.token}"},
            params={"per_page": 20}
        )
        
        if r.status_code == 200:
            st.session_state.error = None
            return r.json()
        elif r.status_code == 401:
            st.session_state.token = None  # Token geçersiz, yenile
            return None
        else:
            st.session_state.error = f"Strava API hatası: {r.status_code}"
            return None
    except Exception as e:
        st.session_state.error = f"Veri çekme hatası: {str(e)}"
        return None

# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.markdown('<div class="title" style="font-size: 1.5rem;">Argus Pro</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="stat-label">WATER</div>', unsafe_allow_html=True)
    
    if st.button("+ 250ml", use_container_width=True):
        st.session_state.water = min(st.session_state.water + 250, 3000)
        st.rerun()
    
    water_pct = (st.session_state.water / 3000) * 100
    st.markdown(f"""
        <div style="display: flex; justify-content: space-between;">
            <span class="stat-label">{st.session_state.water}ml</span>
            <span class="stat-label">3000ml</span>
        </div>
        <div class="progress-container">
            <div class="progress-bar" style="width: {water_pct}%;"></div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.button("🔄 Sync Data", use_container_width=True):
        st.session_state.activities = None
        st.session_state.token = None
        st.rerun()

# -------------------- MAIN --------------------
st.markdown('<div class="title">Dashboard</div>', unsafe_allow_html=True)

# Hata varsa göster
if st.session_state.error:
    st.markdown(f'<div class="error-box">❌ {st.session_state.error}</div>', unsafe_allow_html=True)

# Verileri çek
if not st.session_state.activities:
    with st.spinner("Strava'ya bağlanılıyor..."):
        st.session_state.activities = get_activities()

# Veri varsa göster
if st.session_state.activities:
    acts = st.session_state.activities
    
    if len(acts) == 0:
        st.info("📊 Strava hesabında henüz aktivite yok")
    else:
        # Metrikleri hesapla
        total_dist = sum(a.get('distance', 0) for a in acts) / 1000
        total_cal = sum(a.get('calories', 0) for a in acts)
        
        hrs = [a.get('average_heartrate') for a in acts if a.get('average_heartrate')]
        avg_hr = sum(hrs) / len(hrs) if hrs else 0
        
        # Kartlar
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-label">Total Distance</div>
                    <div class="stat-value">{total_dist:.1f} km</div>
                    <div class="stat-label">{len(acts)} activities</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-label">Avg Heart Rate</div>
                    <div class="stat-value">{avg_hr:.0f} bpm</div>
                    <div class="stat-label">{len(hrs)} with HR data</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-label">Total Calories</div>
                    <div class="stat-value">{total_cal:.0f} kcal</div>
                    <div class="stat-label">burned</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Chart
        st.markdown("---")
        st.markdown('<div class="stat-label">RECENT ACTIVITIES</div>', unsafe_allow_html=True)
        
        chart_data = []
        for act in acts[:10]:
            try:
                date = datetime.strptime(act['start_date'][:10], '%Y-%m-%d')
                chart_data.append({
                    'date': date.strftime('%d %b'),
                    'distance': act.get('distance', 0) / 1000,
                    'name': act.get('name', 'Activity')[:20]
                })
            except:
                continue
        
        if chart_data:
            df = pd.DataFrame(chart_data)
            df = df[::-1]  # Ters çevir (eski -> yeni)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['date'],
                y=df['distance'],
                mode='lines+markers',
                line=dict(color='#8A2BE2', width=3),
                fill='tozeroy',
                fillcolor='rgba(138, 43, 226, 0.1)',
                marker=dict(size=8)
            ))
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#6B6B7B', size=12),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(107,107,123,0.1)', title='km'),
                height=350,
                margin=dict(l=40, r=40, t=20, b=40),
                showlegend=False,
                hovermode='x'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Tablo
            with st.expander("📋 Activity List"):
                table_data = []
                for act in acts[:15]:
                    table_data.append({
                        'Date': act['start_date'][:10],
                        'Name': act.get('name', '')[:30],
                        'Distance': f"{act.get('distance', 0)/1000:.2f} km",
                        'Time': f"{act.get('moving_time', 0)//60} min",
                        'HR': f"{act.get('average_heartrate', 0):.0f}" if act.get('average_heartrate') else '-'
                    })
                st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)
else:
    if not st.session_state.error:
        st.info("👈 Sol menüden Strava bilgilerini kontrol et")

# Footer
st.markdown("---")
st.caption("Argus Pro v3 · Strava Integration")
