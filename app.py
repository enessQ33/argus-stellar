import os
from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

# --- AYARLAR ---
# Burayı sunucuya yüklemeden önce kendi anahtarlarınla doldur kanka!
GROQ_API_KEY = "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"
SYSTEM_PROMPT = "Sen bilge 'Astro Abla'sın. Samimi, mistik ve 'canım, güzel kardeşim' diyen bir üslubun var. Kısa, zeki ve astrolojik derinliği olan cevaplar ver."

# --- HTML & PWA DESTEĞİ ---
HTML_SABLON = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Argus Stellar</title>
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&family=Playfair+Display:ital,wght@0,600;1,600&display=swap" rel="stylesheet">
    <style>
        :root { --gold: #d4af37; --bg: #050507; --glass: rgba(255, 255, 255, 0.03); }
        body { background: var(--bg); color: #d1d1d1; font-family: 'Montserrat', sans-serif; margin: 0; padding: 0; height: 100vh; overflow: hidden; }
        .app-container { display: flex; flex-direction: column; height: 100%; padding: 20px; box-sizing: border-box; }
        .header { text-align: center; margin: 10px 0 20px; }
        .header h1 { font-family: 'Playfair Display', serif; font-size: 24px; color: var(--gold); margin: 0; letter-spacing: 2px; }
        .content { flex: 1; overflow-y: auto; padding-bottom: 90px; }
        .tab { display: none; animation: fadeIn 0.4s ease; }
        .tab.active { display: block; }
        .card { background: var(--glass); border-radius: 20px; padding: 20px; border: 1px solid rgba(212, 175, 55, 0.1); backdrop-filter: blur(15px); margin-bottom: 15px; }
        input, select { width: 100%; padding: 12px; background: transparent; border: none; border-bottom: 1px solid #222; color: #fff; font-size: 15px; outline: none; margin-bottom: 15px; box-sizing: border-box; }
        .btn-gold { background: transparent; border: 1px solid var(--gold); color: var(--gold); padding: 12px; border-radius: 30px; cursor: pointer; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; width: 100%; transition: 0.3s; }
        .btn-gold:hover { background: var(--gold); color: #000; }
        .avatar-circle { width: 70px; height: 70px; border-radius: 50%; background: linear-gradient(45deg, #111, var(--gold)); margin: 0 auto 15px; border: 2px solid var(--gold); display: flex; align-items: center; justify-content: center; font-size: 30px; }
        .energy-bar { background: #111; height: 6px; border-radius: 3px; margin-top: 10px; overflow: hidden; }
        .energy-fill { background: var(--gold); height: 100%; width: 85%; }
        .bottom-nav { position: fixed; bottom: 0; left: 0; right: 0; background: #070709; height: 75px; border-top: 1px solid #1a1a1a; display: flex; justify-content: space-around; align-items: center; z-index: 1000; }
        .nav-item { color: #444; font-size: 9px; text-transform: uppercase; letter-spacing: 1px; cursor: pointer; text-align: center; }
        .nav-item.active { color: var(--gold); }
        .nav-item svg { display: block; margin: 0 auto 5px; width: 22px; height: 22px; fill: currentColor; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    </style>
</head>
<body>
    <div class="app-container">
        <div class="header"><h1>Argus</h1></div>
        <div class="content">
            <div id="chat" class="tab active">
                <div class="card">
                    <div id="displayArea" style="min-height:120px; font-style:italic; font-size:14px; color:#aaa;">Yıldızlar bugün senin için fısıldıyor canım... Sormak istediğin bir şey mi var?</div>
                    <input type="text" id="chatInput" placeholder="Ablana anlat...">
                    <button class="btn-gold" onclick="askAbla()">Sorgula</button>
                </div>
            </div>
            <div id="magic" class="tab">
                <div class="card">
                    <h3 style="color:var(--gold); font-family:'Playfair Display'; margin-top:0;">Kozmik İşlemler</h3>
                    <button class="btn-gold" style="margin-bottom:10px;" onclick="getFortune()">Sanal Kahve Falı Bak</button>
                    <button class="btn-gold" onclick="showMapForm()">Doğum Haritası Çıkar</button>
                    <div id="magicRes" style="margin-top:20px; font-size:13px; line-height:1.6;"></div>
                </div>
            </div>
            <div id="profile" class="tab">
                <div class="card" style="text-align:center;">
                    <div class="avatar-circle">🧿</div>
                    <h2 id="profName" style="color:var(--gold); font-family:'Playfair Display'; margin:5px 0;">Kozmik Yolcu</h2>
                    <p id="profSign" style="font-size:12px; color:#666;">BURÇ SEÇİLMEDİ</p>
                    <div style="text-align:left; margin-top:20px;">
                        <span style="font-size:11px;">RUHSAL ENERJİ %88</span>
                        <div class="energy-bar"><div class="energy-fill"></div></div>
                    </div>
                </div>
            </div>
            <div id="settings" class="tab">
                <div class="card">
                    <h3 style="color:var(--gold); font-family:'Playfair Display'; margin-top:0;">Tercihler</h3>
                    <button class="btn-gold" onclick="alert('Önbellek temizlendi!')">Verileri Sıfırla</button>
                    <p style="font-size:10px; color:#333; margin-top:20px; text-align:center;">Argus v6.5 Server Edition</p>
                </div>
            </div>
        </div>
    </div>
    <div class="bottom-nav">
        <div class="nav-item active" onclick="switchTab('chat', this)"><svg viewBox="0 0 24 24"><path d="M21 6h-2v9H6v2c0 .55.45 1 1 1h11l4 4V7c0-.55-.45-1-1-1zm-4 6V3c0-.55-.45-1-1-1H3c-.55 0-1 .45-1 1v14l4-4h10c.55 0 1-.45 1-1z"/></svg>Sohbet</div>
        <div class="nav-item" onclick="switchTab('magic', this)"><svg viewBox="0 0 24 24"><path d="M12 2L4.5 20.29l.71.71L12 18l6.79 3 .71-.71L12 2z"/></svg>Mistik</div>
        <div class="nav-item" onclick="switchTab('profile', this)"><svg viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>Profil</div>
        <div class="nav-item" onclick="switchTab('settings', this)"><svg viewBox="0 0 24 24"><path d="M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58z"/></svg>Ayarlar</div>
    </div>
    <script>
        function switchTab(tabId, el) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            el.classList.add('active');
        }
        async function askAbla() {
            const inp = document.getElementById('chatInput');
            const disp = document.getElementById('displayArea');
            if(!inp.value) return;
            disp.innerText = "Bekle canım, bir bakayım gökyüzüne...";
            const res = await fetch('/sor', { method: 'POST', body: new URLSearchParams({'soru': inp.value}) });
            const data = await res.json();
            disp.innerText = data.cevap;
            inp.value = "";
        }
        async function getFortune() {
            const res = document.getElementById('magicRes');
            res.innerText = "Fincanına bakıyorum canım...";
            const resp = await fetch('/sor', { method: 'POST', body: new URLSearchParams({'soru': 'Bana sanal bir kahve falı bak ablası'}) });
            const data = await resp.json();
            res.innerText = data.cevap;
        }
        function showMapForm() {
            document.getElementById('magicRes').innerHTML = `
                <input type="text" id="mN" placeholder="Adın" onchange="document.getElementById('profName').innerText=this.value">
                <select id="mS" onchange="document.getElementById('profSign').innerText=this.value.toUpperCase()">
                    <option>Burç Seç</option><option>Koç</option><option>Boğa</option><option>İkizler</option><option>Yengeç</option>
                </select>
                <button class="btn-gold" onclick="alert('Profil güncellendi!')">Kaydet</button>
            `;
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index(): return render_template_string(HTML_SABLON)

@app.route("/sor", methods=["POST"])
def sor():
    soru = request.form.get("soru")
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
    data = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": soru}]}
    try:
        r = requests.post(url, headers=headers, json=data, timeout=15)
        return jsonify({"cevap": r.json()['choices'][0]['message']['content']})
    except: return jsonify({"cevap": "Canım yıldızlar bugün tozlu, sonra yine gel."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("PORT", 5000))
