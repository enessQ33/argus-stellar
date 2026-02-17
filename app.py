# main.py - Argus Pro v3 (Streamlit Secrets ile - Uyarısız)
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from datetime import datetime, timedelta
import time

# =============================================
# 🔐 STRAVA API BİLGİLERİ (Sadece Secrets'ten)
# =============================================
# Streamlit Cloud'da Settings > Secrets'a şunları ekle:
"""
STRAVA_CLIENT_ID = "135871"
STRAVA_CLIENT_SECRET = "8e9b9a2fb16f50233a1f9e5b747439d5ef996c53"
STRAVA_REFRESH_TOKEN = "f55d2575ae4f2e799f5970914fa4667170a50c6c"
"""

# Secrets'ten al - hata yönetimli ama uyarısız
CLIENT_ID = st.secrets.get("STRAVA_CLIENT_ID", "")
CLIENT_SECRET = st.secrets.get("STRAVA_CLIENT_SECRET", "")
REFRESH_TOKEN = st.secrets.get("STRAVA_REFRESH_TOKEN", "")

# Boşsa bile sessizce devam et (sonra token yenileme başarısız olur ama uyarı patlamaz)
# =============================================

# Sayfa yapılandırması
st.set_page_config(
    page_title="Argus Pro v3 - Sağlık Paneli",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# FontAwesome ikonları için CSS
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
    .stApp {
        background-color: #0e1117;
    }
    .card {
        background: linear-gradient(145deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 20px;
        padding: 1.5rem;
        border-left: 5px solid #8A2BE2;
        box-shadow: 0 10px 30px rgba(138, 43, 226, 0.2);
        transition: transform 0.3s ease;
        color: white;
        margin: 10px 0;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(138, 43, 226, 0.3);
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #8A2BE2;
        margin: 10px 0;
    }
    .metric-label {
        font-size: 1rem;
        color: #b0b0b0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .progress-bar {
        width: 100%;
        height: 20px;
        background: #1a1a2e;
        border-radius: 10px;
        margin: 10px 0;
        overflow: hidden;
    }
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #8A2BE2, #b066fe);
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    .water-text {
        font-size: 1.2rem;
        color: #8A2BE2;
        text-align: center;
    }
    .success-badge {
        background: rgba(138, 43, 226, 0.2);
        color: #8A2BE2;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        display: inline-block;
        margin: 5px 0;
        border: 1px solid #8A2BE2;
    }
    .info-box {
        background: rgba(138, 43, 226, 0.1);
        border-left: 3px solid #8A2BE2;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Session state başlatma
if 'water_intake' not in st.session_state:
    st.session_state.water_intake = 0
if 'access_token' not in st.session_state:
    st.session_state.access_token = None
if 'activities_data' not in st.session_state:
    st.session_state.activities_data = None
if 'last_fetch' not in st.session_state:
    st.session_state.last_fetch = None
if 'token_expires_at' not in st.session_state:
    st.session_state.token_expires_at = None
if 'token_status' not in st.session_state:
    st.session_state.token_status = "⏳ Bağlanıyor..."
if 'refresh_token' not in st.session_state:
    st.session_state.refresh_token = REFRESH_TOKEN

def get_new_token():
    """Strava'dan yeni access token alır (Refresh Token ile)"""
    # Secrets boşsa sessizce None dön
    if not CLIENT_ID or not CLIENT_SECRET or not st.session_state.refresh_token:
        return None
    
    try:
        token_url = "https://www.strava.com/oauth/token"
        payload = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'refresh_token': st.session_state.refresh_token,
            'grant_type': 'refresh_token'
        }
        
        response = requests.post(token_url, data=payload, timeout=10)
        
        if response.status_code == 200:
            token_data = response.json()
            return {
                'access_token': token_data['access_token'],
                'expires_at': token_data['expires_at'],
                'refresh_token': token_data.get('refresh_token', st.session_state.refresh_token)
            }
        else:
            return None
    except Exception:
        return None

def ensure_valid_token():
    """Token'ın geçerliliğini kontrol eder, gerekirse yeniler"""
    current_time = time.time()
    
    # Token yoksa veya süresi dolmuşsa yenile
    if (st.session_state.access_token is None or 
        st.session_state.token_expires_at is None or 
        current_time >= st.session_state.token_expires_at - 300):
        
        st.session_state.token_status = "🔄 Token yenileniyor..."
        token_data = get_new_token()
        
        if token_data:
            st.session_state.access_token = token_data['access_token']
            st.session_state.token_expires_at = token_data['expires_at']
            st.session_state.refresh_token = token_data['refresh_token']
            st.session_state.token_status = "✅ Bağlandı"
            return True
        else:
            st.session_state.token_status = "⏳ Beklemede..."
            return False
    return True

def fetch_strava_activities():
    """Strava'dan aktivite verilerini çeker"""
    if not ensure_valid_token():
        return None
    
    try:
        url = "https://www.strava.com/api/v3/athlete/activities"
        headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
        params = {"per_page": 15, "page": 1}
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            st.session_state.access_token = None
            return None
        else:
            return None
    except Exception:
        return None

# Başlık
st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <i class='fas fa-heartbeat' style='font-size: 4rem; color: #8A2BE2;'></i>
        <h1 style='color: white; font-size: 3rem; margin: 1rem 0;'>Argus Pro <span style='color: #8A2BE2;'>v3</span></h1>
        <p style='color: #b0b0b0;'>🔐 Gelişmiş Sağlık Takip Paneli</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("<h2 style='color: #8A2BE2; text-align: center;'>⚙️ Kontrol Paneli</h2>", unsafe_allow_html=True)
    
    # Token durumu göster - sade ama şık
    st.markdown(f"""
        <div style='text-align: center; margin: 10px 0;'>
            <span class='success-badge'>
                <i class='fas fa-key'></i> {st.session_state.token_status}
            </span>
        </div>
    """, unsafe_allow_html=True)
    
    # Su takibi butonu
    st.markdown("### 💧 Su Takibi")
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("🚰 +250 ml Su İç", use_container_width=True):
            st.session_state.water_intake = min(st.session_state.water_intake + 250, 3000)
            st.rerun()
    with col2:
        if st.button("🔄 Sıfırla", use_container_width=True):
            st.session_state.water_intake = 0
            st.rerun()
    
    # Su ilerleme çubuğu
    water_percentage = (st.session_state.water_intake / 3000) * 100
    st.markdown(f"""
        <div class='water-text'>
            <i class='fas fa-droplet'></i> {st.session_state.water_intake}ml / 3000ml
        </div>
        <div class='progress-bar'>
            <div class='progress-fill' style='width: {water_percentage}%;'></div>
        </div>
    """, unsafe_allow_html=True)
    
    # Token süresi varsa göster
    if st.session_state.token_expires_at:
        expiry_date = datetime.fromtimestamp(st.session_state.token_expires_at)
        time_left = expiry_date - datetime.now()
        minutes_left = int(time_left.total_seconds() / 60)
        
        if minutes_left > 0 and minutes_left < 60:
            st.markdown(f"""
                <div style='text-align: center; font-size: 0.8rem; color: #666;'>
                    ⏱️ {minutes_left} dk kaldı
                </div>
            """, unsafe_allow_html=True)
    
    # Butonlar
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Token Yenile", use_container_width=True):
            st.session_state.access_token = None
            st.session_state.last_fetch = None
            st.rerun()
    with col2:
        if st.button("📊 Veri Yenile", use_container_width=True):
            st.session_state.last_fetch = None
            st.rerun()

# Ana içerik
# Token kontrolü ve veri çekme
if ensure_valid_token():
    if (st.session_state.last_fetch is None or 
        (datetime.now() - st.session_state.last_fetch).seconds > 300):
        
        with st.spinner("📡 Veriler yükleniyor..."):
            activities = fetch_strava_activities()
            if activities:
                st.session_state.activities_data = activities
                st.session_state.last_fetch = datetime.now()

# Metrik kartları
if st.session_state.activities_data:
    activities = st.session_state.activities_data
    
    # Metrikleri hesapla
    total_distance = sum(act.get('distance', 0) for act in activities) / 1000
    avg_heartrate = 0
    heartrate_count = 0
    total_calories = sum(act.get('calories', 0) for act in activities)
    
    for act in activities:
        if act.get('average_heartrate'):
            avg_heartrate += act['average_heartrate']
            heartrate_count += 1
    
    avg_heartrate = avg_heartrate / heartrate_count if heartrate_count > 0 else 0
    
    # Kartlar
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class='card'>
                <i class='fas fa-route' style='font-size: 2rem; color: #8A2BE2;'></i>
                <div class='metric-label'>Toplam Mesafe</div>
                <div class='metric-value'>{total_distance:.1f} km</div>
                <div style='color: #666; font-size: 0.8rem;'>son 15 aktivite</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class='card'>
                <i class='fas fa-heart' style='font-size: 2rem; color: #8A2BE2;'></i>
                <div class='metric-label'>Ortalama Nabız</div>
                <div class='metric-value'>{avg_heartrate:.0f} bpm</div>
                <div style='color: #666; font-size: 0.8rem;'>son 15 aktivite</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class='card'>
                <i class='fas fa-fire' style='font-size: 2rem; color: #8A2BE2;'></i>
                <div class='metric-label'>Toplam Kalori</div>
                <div class='metric-value'>{total_calories:.0f} kcal</div>
                <div style='color: #666; font-size: 0.8rem;'>son 15 aktivite</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Grafik
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: white;'>📊 Aktiviteler</h3>", unsafe_allow_html=True)
    
    # Grafik verisi
    df_data = []
    for act in activities[:15]:
        try:
            date_str = act['start_date'].replace('Z', '+00:00')
            if 'T' in date_str:
                date_obj = datetime.fromisoformat(date_str.split('+')[0])
            else:
                date_obj = datetime.strptime(date_str.split('+')[0], '%Y-%m-%d')
            
            df_data.append({
                'tarih': date_obj.strftime('%d/%m'),
                'mesafe': act.get('distance', 0) / 1000,
                'isim': act.get('name', 'Aktivite')[:30],
                'tarih_obj': date_obj
            })
        except Exception:
            continue
    
    if df_data:
        df = pd.DataFrame(df_data)
        df = df.sort_values('tarih_obj')
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['tarih'],
            y=df['mesafe'],
            mode='lines+markers',
            line=dict(color='#8A2BE2', width=3),
            fill='tozeroy',
            fillcolor='rgba(138, 43, 226, 0.2)',
            marker=dict(size=8, color='#8A2BE2')
        ))
        
        fig.update_layout(
            plot_bgcolor='#0e1117',
            paper_bgcolor='#0e1117',
            font=dict(color='white'),
            xaxis=dict(gridcolor='#333', showgrid=True),
            yaxis=dict(gridcolor='#333', showgrid=True, title='km'),
            height=350,
            margin=dict(l=40, r=40, t=20, b=40),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Tablo
        with st.expander("📋 Aktivite Listesi"):
            df_display = df[['tarih', 'mesafe', 'isim']].copy()
            df_display['mesafe'] = df_display['mesafe'].round(2)
            df_display.columns = ['Tarih', 'Mesafe (km)', 'Aktivite']
            st.dataframe(df_display, use_container_width=True, hide_index=True)
else:
    # Boş durum mesajı - sade ve şık
    if st.session_state.token_status == "✅ Bağlandı":
        st.markdown("""
            <div style='text-align: center; padding: 3rem; color: #666;'>
                <i class='fas fa-bicycle' style='font-size: 3rem; color: #8A2BE2;'></i>
                <p style='margin-top: 1rem;'>Henüz aktivite bulunamadı</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style='text-align: center; padding: 3rem; color: #666;'>
                <i class='fas fa-plug' style='font-size: 3rem; color: #8A2BE2;'></i>
                <p style='margin-top: 1rem;'>Strava bağlantısı bekleniyor</p>
            </div>
        """, unsafe_allow_html=True)

# Footer - sade
st.markdown("""
    <div style='text-align: center; padding: 1rem; color: #333; font-size: 0.7rem;'>
        <hr style='border-color: #222;'>
        <p>Argus Pro v3 · Strava ile entegre</p>
    </div>
""", unsafe_allow_html=True)
