import streamlit as st
import random
import time
import urllib.parse

# --- 1. Konfiguracja ---
IMIE_ONA = "Ona"   # <-- Wpisz jej imię!
IMIE_ON = "On"     # <-- Wpisz swoje imię!

st.set_page_config(page_title="Wieczór we Dwoje", layout="wide", page_icon="🥂")
query_params = st.query_params
# Domyślnie ładujemy widok TV (Lobby)
view_type = query_params.get("view", "tv")

# --- 2. GŁÓWNY CSS (Telewizor i ogólny styl) ---
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
        padding: 60px 40px;
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.8);
        text-align: center;
        margin: 40px auto;
        max-width: 1000px;
    }
    
    .gold-text {
        font-size: 54px;
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

    .turn-badge {
        display: inline-block;
        padding: 8px 24px;
        border-radius: 30px;
        font-size: 20px;
        font-weight: 400;
        letter-spacing: 4px;
        margin-bottom: 30px;
        text-transform: uppercase;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    
    .turn-ona { background-color: rgba(212, 175, 55, 0.1); border: 1px solid #d4af37; color: #d4af37; }
    .turn-on { background-color: rgba(140, 122, 150, 0.1); border: 1px solid #8c7a96; color: #8c7a96; }

    /* Stylowanie przycisku START na TV */
    button[kind="primary"] {
        background: linear-gradient(145deg, #d4af37, #b5952f) !important;
        color: #0a0810 !important;
        border: none !important;
        font-weight: bold !important;
        font-size: 24px !important;
        border-radius: 15px !important;
        box-shadow: 0 10px 20px rgba(212, 175, 55, 0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. SPECJALNY CSS TYLKO DLA PILOTA ---
if view_type == "pilot":
    st.markdown("""
    <style>
        /* Nadpisywanie stylów, by pilot był ekstremalnie czysty */
        .premium-box, .elegant-header { display: none !important; }
        
        div.stButton > button {
            height: 40vh !important;
            width: 100% !important;
            border-radius: 40px !important;
            margin-top: 2vh;
            box-shadow: 0 15px 30px rgba(0,0,0,0.8) !important;
        }
        
        div.stButton > button p {
            font-size: 80px !important;
            font-weight: bold !important;
            letter-spacing: 10px !important;
        }

        /* 1. Przycisk TAK (primary nadpisany z TV) */
        button[kind="primary"] {
            background: linear-gradient(145deg, #123524, #0a1a11) !important;
            border: 3px solid #4bd67b !important;
            box-shadow: 0 20px 40px rgba(0,0,0,0.8) !important;
        }
        button[kind="primary"] p { color: #4bd67b !important; }

        /* 2. Przycisk NIE (secondary) */
        button[kind="secondary"] {
            background: linear-gradient(145deg, #351216, #1a0a0b) !important;
            border: 3px solid #ff4b4b !important;
        }
        button[kind="secondary"] p { color: #ff4b4b !important; }

        /* 3. Przycisk RESET (Niewidzialny ninja) */
        div.stButton:last-of-type > button {
            height: 50px !important;
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            margin-top: 10vh !important;
        }
        div.stButton:last-of-type > button p {
            font-size: 14px !important;
            color: #2a2035 !important; /* Bardzo ciemny, zlewa się z tłem */
        }
    </style>
    """, unsafe_allow_html=True)

# --- 4. Baza Danych ---
pytania = [
    {"kto": "ONA", "tekst": "Jakie jest moje ulubione wspomnienie z naszej pierwszej randki?"},
    {"kto": "ON", "tekst": "W czym, według Ciebie, wyglądam najatrakcyjniej na co dzień?"},
    {"kto": "ONA", "tekst": "W jakiej pozycji najszybciej osiągam orgazm?"},
    {"kto": "ON", "tekst": "Jaka jest moja najbardziej skryta fantazja erotyczna?"}
    # Tutaj wklej wszystkie 50 pytań!
]

kary_p1 = ["Zdejmij skarpetki.", "Masaż karku."]
kary_p4 = ["Zdejmijcie wszystko.", "Nagroda główna 😈"]
def wylosuj_kare(n): return random.choice(kary_p1 if n < 12 else kary_p4)

# --- 5. Synchronizacja stanu ---
@st.cache_resource
def get_global_state():
    # Zaczynamy w statusie "lobby"
    return {"current_q": 0, "status": "lobby", "penalty": ""}

state = get_global_state()

# --- WIDOK 1: TELEWIZOR (Mózg operacji) ---
if view_type == "tv":
    
    # === TRYB LOBBY (Ekran powitalny z kodem QR) ===
    if state["status"] == "lobby":
        st.markdown("<div class='elegant-header'>Lobby Gry</div>", unsafe_allow_html=True)
        st.markdown("<div class='premium-box'>", unsafe_allow_html=True)
        st.markdown("<h1 class='gold-text' style='font-size: 40px; margin-bottom: 10px;'>Podłącz Pilota</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #8c7a96; font-size: 18px;'>Zeskanuj kod telefonem, zapisz do ekranu głównego jako aplikację, a następnie kliknij Start.</p>", unsafe_allow_html=True)
        
        # Pole do wklejenia linku (potrzebne, by wygenerować prawidłowy kod QR)
        app_url = st.text_input("🔗 Adres Twojej aplikacji (skopiuj z paska przeglądarki na tym TV):", value="https://twoja-aplikacja.streamlit.app")
        
        if app_url:
            pilot_link = app_url.rstrip("/") + "/?view=pilot"
            # Generowanie kodu QR przez darmowe, niezawodne API
            qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={urllib.parse.quote(pilot_link)}&margin=10"
            
            st.markdown(f"""
                <div style='background-color: white; padding: 15px; display: inline-block; border-radius: 20px; margin: 30px;'>
                    <img src='{qr_url}' width='250' style='display: block;'/>
                </div>
            """, unsafe_allow_html=True)
        
        # Przycisk startu uruchamia grę
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("▶️ ROZPOCZNIJ GRĘ", use_container_width=True, type="primary"):
            state["status"] = "question"
            st.rerun()
            
        st.markdown("</div>", unsafe_allow_html=True)

    # === TRYB GRY ===
    else:
        q_idx = state["current_q"]
        
        if q_idx < len(pytania):
            obecne_pytanie = pytania[q_idx]
            kto_odpowiada = str(obecne_pytanie.get("kto", "")).upper().strip()
            badge_class, kolej_imie = ("turn-ona", IMIE_ONA) if kto_odpowiada == "ONA" else ("turn-on", IMIE_ON)

            if state["status"] == "question":
                st.markdown(f"<div class='elegant-header'>Runda {q_idx + 1}</div>", unsafe_allow_html=True)
                st.markdown(f"""
                <div class='premium-box'>
                    <div class='turn-badge {badge_class}'>TERAZ ODPOWIADA: {kolej_imie}</div>
                    <div class='gold-text'>{obecne_pytanie['tekst']}</div>
                </div>
                """, unsafe_allow_html=True)
                # TV nasłuchuje werdyktu (odświeża się co sekundę)
                time.sleep(1)
                st.rerun()
                
            elif state["status"] == "result":
                if state["penalty"] == "":
                    st.markdown("<div class='premium-box' style='background: rgba(75, 214, 123, 0.1); border: 1px solid #1a4a30;'><h1 style='color: #4bd67b; font-size: 60px;'>PRAWDA</h1><p style='font-size: 24px; color: white;'>Zaliczone bez kary!</p></div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='premium-box' style='background: rgba(255, 75, 75, 0.1); border: 1px solid #4a1a20;'><h1 style='color: #ff4b4b; font-size: 40px;'>CZAS NA ZADANIE:</h1><h1 style='color: white; font-size: 50px;'>{state['penalty']}</h1></div>", unsafe_allow_html=True)
                
                # Odliczanie kary i auto-przejście
                time.sleep(5)
                state["current_q"] += 1
                state["status"] = "question"
                st.rerun()
        else:
            st.markdown("<div class='premium-box'><div class='gold-text'>KONIEC GRY.<br>Czas na Was.</div></div>", unsafe_allow_html=True)
            time.sleep(5)
            st.rerun()

# --- WIDOK 2: PILOT (Dumb Terminal) ---
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

    # Przycisk RESETU (Cofamy do Lobby na wszelki wypadek)
    if st.button("reset", use_container_width=True):
        state["current_q"] = 0
        state["status"] = "lobby"
