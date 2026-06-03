import streamlit as st
import urllib.request
import json

st.set_page_config(page_title="Bajeti AI — Fuatilia Bajeti ya Kaunti", page_icon="📊", layout="centered")

st.markdown("""<style>
.stApp { background: #0a0f14; color: #e8f0fe; }
.budget-card {
    background: #0d1829; border: 1px solid #1a3a6e;
    border-radius: 10px; padding: 14px 18px; margin: 8px 0;
}
.stButton > button {
    background: #0d47a1; color: white; border: none;
    border-radius: 8px; padding: 10px 24px; font-weight: 700; width: 100%;
}
.good { color: #69f0ae; } .bad { color: #ff5252; } .warn { color: #ffd740; }
</style>""", unsafe_allow_html=True)

API_KEY = st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("GEMINI_API_KEY", "")

# Demo county budget data (DEMO — synthetic, for illustration only)
DEMO_BUDGET = {
    "Nairobi": {
        "year": "2023/24", "allocation_total": 42_500_000_000,
        "sectors": [
            {"name": "Afya (Health)", "allocated": 8_500_000_000, "spent": 7_200_000_000},
            {"name": "Elimu (Education)", "allocated": 6_200_000_000, "spent": 5_800_000_000},
            {"name": "Maji (Water)", "allocated": 4_100_000_000, "spent": 2_900_000_000},
            {"name": "Barabara (Roads)", "allocated": 7_800_000_000, "spent": 6_500_000_000},
            {"name": "Kilimo (Agriculture)", "allocated": 2_200_000_000, "spent": 1_100_000_000},
            {"name": "Utawala (Administration)", "allocated": 13_700_000_000, "spent": 13_200_000_000},
        ]
    },
    "Kiambu": {
        "year": "2023/24", "allocation_total": 11_200_000_000,
        "sectors": [
            {"name": "Afya (Health)", "allocated": 2_800_000_000, "spent": 2_600_000_000},
            {"name": "Elimu (Education)", "allocated": 1_900_000_000, "spent": 1_750_000_000},
            {"name": "Maji (Water)", "allocated": 1_500_000_000, "spent": 800_000_000},
            {"name": "Barabara (Roads)", "allocated": 2_100_000_000, "spent": 1_900_000_000},
            {"name": "Kilimo (Agriculture)", "allocated": 900_000_000, "spent": 550_000_000},
            {"name": "Utawala (Administration)", "allocated": 2_000_000_000, "spent": 1_950_000_000},
        ]
    },
}

def fmt_ksh(n): return f"KSh {n/1e9:.2f}B" if n >= 1e9 else f"KSh {n/1e6:.1f}M"

def ask_budget_ai(county, sectors, api_key):
    if not api_key: return "❌ API key not configured."
    summary = "\n".join([
        f"- {s['name']}: Ilipangwa {fmt_ksh(s['allocated'])}, Ilitumika {fmt_ksh(s['spent'])} ({s['spent']/s['allocated']*100:.0f}%)"
        for s in sectors
    ])
    prompt = f"""Bajeti ya Kaunti ya {county} 2023/24:
{summary}

Eleza kwa Kiswahili:
1. Je, kaunti ilitumia pesa zake vizuri?
2. Sekta gani ilipewa pesa nyingi na sekta gani kidogo?
3. Wapi pesa haikutumika? Kwa nini hii inaweza kuwa tatizo?
4. Kama mwananchi, unapaswa kuuliza maswali gani kwa serikali yako ya kaunti?"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    body = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "systemInstruction": {"parts": [{"text": "Wewe ni mchambuzi wa bajeti wa Kenya. Eleza data ya bajeti kwa wananchi kwa Kiswahili rahisi. Kuwa mkweli na wa haki."}]},
        "generationConfig": {"temperature": 0.3, "maxOutputTokens": 600}
    }
    try:
        req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.loads(r.read())
            return d["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"❌ Hitilafu: {e}"

st.markdown("# 📊 Bajeti AI")
st.markdown("**Fuatilia Bajeti ya Kaunti yako**")
st.caption("Angalia nini kilipangwa, nini kilitekelezwa, na wapi pesa haikutumika.")

st.info("⚠️ **DEMO — Data ya Mfano tu** | Hii ni data ya synthetic kwa maonyesho. Data halisi inapatikana kwenye opendata.go.ke", icon="⚠️")

county = st.selectbox("Chagua Kaunti", list(DEMO_BUDGET.keys()))
data = DEMO_BUDGET[county]

st.markdown(f"### Bajeti ya Kaunti ya {county} — {data['year']}")
st.markdown(f"**Jumla ya Mgao:** {fmt_ksh(data['allocation_total'])}")

for s in data["sectors"]:
    pct = s["spent"] / s["allocated"] * 100
    pct_class = "good" if pct >= 85 else "warn" if pct >= 60 else "bad"
    bar_w = int(pct)
    st.markdown(
        f"""<div class="budget-card">
        <b>{s['name']}</b><br>
        Ilipangwa: {fmt_ksh(s['allocated'])} | Ilitumika: {fmt_ksh(s['spent'])}
        <span class="{pct_class}"> ({pct:.0f}%)</span><br>
        <div style="background:#1a3a6e;border-radius:4px;height:8px;margin-top:6px">
        <div style="background:{'#69f0ae' if pct>=85 else '#ffd740' if pct>=60 else '#ff5252'};width:{bar_w}%;height:8px;border-radius:4px"></div></div>
        </div>""", unsafe_allow_html=True)

if st.button("🤖 Eleza Bajeti Hii kwa AI", key="ai_btn"):
    with st.spinner("Ninachambua bajeti..."):
        analysis = ask_budget_ai(county, data["sectors"], API_KEY)
    st.markdown("### Uchambuzi wa AI")
    st.markdown(f"""<div class="budget-card">{analysis.replace(chr(10), "<br>")}</div>""", unsafe_allow_html=True)

st.markdown("---")
st.caption("📊 Bajeti AI v1.0 | Data: DEMO — synthetic | Kwa data halisi: opendata.go.ke | CC BY-NC-ND 4.0")
