import streamlit as st
import random
import time
import urllib.parse

# --- 1. KONFIGURACJA I WASZE IMIONA ---
IMIE_ONA = "Ona"   
IMIE_ON = "On"     

st.set_page_config(page_title="Wieczór we Dwoje", layout="wide", page_icon="🥂")

# Obsługa Meta-tagów dla trybu pełnoekranowego (PWA) na telefonie
st.markdown("""
<head>
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Pilot Gry</title>
</head>
""", unsafe_allow_html=True)

# Pobranie parametrów URL
query_params = st.query_params
view_type = query_params.get("view", "tv")

# --- 2. ELEGANCKI CSS (TV i PILOT) ---
st.markdown("""
<style>
    .stApp {
        background-color: #0a0810;
        background-image: radial-gradient(circle at 50% 0%, #1a1225 0%, #0a0810 70%);
        color: #e0d8d3;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    #MainMenu, footer, header {visibility: hidden;}
    div[data-testid="stStaleWidget"], div[data-testid="stStatusWidget"] { display: none !important; }

    .premium-box {
        background: linear-gradient(145deg, #15101c, #0d0a13);
        border: 1px solid #2a2035;
        border-radius: 25px;
        padding: 40px;
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.8);
        text-align: center;
        margin: 20px auto;
        max-width: 800px;
    }
    
    .gold-text {
        font-size: 45px;
        font-weight: 300;
        color: #d4af37; 
        text-shadow: 0 4px 20px rgba(212, 175, 55, 0.3);
        line-height: 1.4;
    }
    
    .elegant-header {
        color: #8c7a96;
        font-size: 18px;
        text-transform: uppercase;
        letter-spacing: 6px;
        text-align: center;
        margin-top: 20px;
    }

    /* Stylizacja Pilotów */
    div.stButton > button {
        height: 35vh !important;
        width: 100% !important;
        border-radius: 30px !important;
        margin-top: 2vh;
        box-shadow: 0 15px 30px rgba(0,0,0,0.8) !important;
    }
    div.stButton > button p {
        font-size: 70px !important;
        font-weight: bold !important;
        letter-spacing: 5px !important;
    }
    button[kind="primary"] { background-color: #123524 !important; border: 3px solid #4bd67b !important; }
    button[kind="primary"] p { color: #4bd67b !important; }
    button[kind="secondary"] { background-color: #351216 !important; border: 3px solid #ff4b4b !important; }
    button[kind="secondary"] p { color: #ff4b4b !important; }

    /* Ukryty Reset */
    div.stButton:last-of-type > button {
        height: 40px !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    div.stButton:last-of-type > button p { font-size: 14px !important; color: #2a2035 !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. BAZA DANYCH (PYTANIA I KARY) ---
pytania = [
    {"kto": "ONA", "tekst": "Jakie jest moje ulubione wspomnienie z naszej pierwszej randki?"},
    {"kto": "ON", "tekst": "W czym, według Ciebie, wyglądam najatrakcyjniej na co dzień?"},
    {"kto": "ONA", "tekst": "W jakiej pozycji najszybciej osiągam orgazm?"},
    {"kto": "ON", "tekst": "Jaka jest moja najbardziej skryta fantazja erotyczna?"}
    # Tutaj wklej resztę swoich 50 pytań!
]

kary_p1 = ["Zdejmij skarpetki.", "Masaż karku."]
kary_p4 = ["Zdejmijcie wszystko.", "Nagroda główna 😈"]
def wylosuj_kare(n): return random.choice(kary_p1 if n < 12 else kary_p4)

# --- 4. SYNCHRONIZACJA STANU ---
@st.cache_resource
def get_global_state():
    return {"current_q": 0, "status": "lobby", "penalty": ""}

state = get_global_state()

# --- 5. WIDOK TELEWIZORA ---
if view_type == "tv":
    
    # EKRAN LOBBY
    if state["status"] == "lobby":
        st.markdown("<div class='elegant-header'>Lobby Wieczoru</div>", unsafe_allow_html=True)
        st.markdown("<div class='premium-box'>", unsafe_allow_html=True)
        st.markdown("<h1 class='gold-text'>Połącz Pilota</h1>", unsafe_allow_html=True)
        
        # Kluczowe: Musisz tu wkleić link do swojej aplikacji, by QR działał!
        current_url = st.text_input("🔗 Wklej tutaj link do tej strony (z paska adresu):", 
                                   placeholder="https://twoja-apka.streamlit.app")
        
        if current_url:
            pilot_link = current_url.rstrip("/") + "/?view=pilot"
            qr_api = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={urllib.parse.quote(pilot_link)}&margin=10&color=d4af37&bgcolor=0a0810"
            
            st.markdown(f"""
                <div style='text-align: center; margin: 20px;'>
                    <img src='{qr_api}' style='border: 2px solid #2a2035; border-radius: 15px;' />
                </div>
            """, unsafe_allow_html=True)
            st.write("1. Zeskanuj kod. 2. Dodaj do ekranu głównego. 3. Kliknij Start.")
        
        if st.button("▶️ ROZPOCZNIJ GRĘ"):
            state["status"] = "question"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # EKRAN GRY
    else:
        q_idx = state["current_q"]
        if q_idx < len(pytania):
            obecne = pytania[q_idx]
            if state["status"] == "question":
                kto = str(obecne.get("kto", "")).upper()
                badge, imie = ("turn-ona", IMIE_ONA) if kto == "ONA" else ("turn-on", IMIE_ON)
                st.markdown(f"<div class='elegant-header'>Runda {q_idx + 1}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='premium-box'><div class='turn-badge {badge}'>Odpowiada: {imie}</div><div class='gold-text'>{obecne['tekst']}</div></div>", unsafe_allow_html=True)
                time.sleep(1)
                st.rerun()
            elif state["status"] == "result":
                if state["penalty"] == "":
                    st.markdown("<div class='premium-box' style='background: rgba(75,214,123,0.1);'><h1 style='color: #4bd67b; font-size: 60px;'>PRAWDA</h1></div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='premium-box' style='background: rgba(255,75,75,0.1);'><h1 style='color: #ff4b4b;'>ZADANIE:</h1><h1 style='color: white;'>{state['penalty']}</h1></div>", unsafe_allow_html=True)
                time.sleep(5)
                state["current_q"] += 1
                state["status"] = "question"
                st.rerun()
        else:
            st.markdown("<div class='premium-box'><h1 class='gold-text'>KONIEC GRY</h1></div>", unsafe_allow_html=True)

# --- 6. WIDOK PILOTA ---
elif view_type == "pilot":
    # Przycisk TAK (primary)
    if st.button("TAK", use_container_width=True, type="primary"):
        if state["status"] == "question":
            state["status"] = "result"
            state["penalty"] = ""
    
    # Przycisk NIE (secondary)
    if st.button("NIE", use_container_width=True, type="secondary"):
        if state["status"] == "question":
            state["status"] = "result"
            state["penalty"] = wylosuj_kare(state["current_q"])

    # Ukryty reset
    if st.button("reset", use_container_width=True):
        state["current_q"] = 0
        state["status"] = "lobby"
        st.rerun()
