import streamlit as st
import random
import time

# --- 1. Konfiguracja i Wasze Imiona ---
# Wpiszcie tutaj swoje imiona! Będą się wyświetlać na TV.
IMIE_ONA = "BASIA" 
IMIE_ON = "KUBA"

st.set_page_config(page_title="Wieczór we Dwoje", layout="wide", page_icon="🥂")
query_params = st.query_params
view_type = query_params.get("view", "selection")

# --- 2. Elegancki CSS ---
st.markdown("""
<style>
    .stApp {
        background-color: #0a0810;
        background-image: radial-gradient(circle at 50% 0%, #1a1225 0%, #0a0810 70%);
        color: #e0d8d3;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    #MainMenu, footer, header {visibility: hidden;}

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

    /* Plakietki wskazujące czyja to kolej */
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
    
    .turn-ona {
        background-color: rgba(212, 175, 55, 0.1);
        border: 1px solid #d4af37;
        color: #d4af37;
    }
    
    .turn-on {
        background-color: rgba(140, 122, 150, 0.1);
        border: 1px solid #8c7a96;
        color: #8c7a96;
    }

    /* Przyciski Pilota */
    .stButton > button {
        height: 180px !important;
        border-radius: 30px !important;
        font-size: 48px !important;
        font-weight: 200 !important;
        letter-spacing: 10px !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6) !important;
        border: none !important;
    }

    button[data-testid="baseButton-primary"] {
        background: linear-gradient(145deg, #123524, #0a1a11) !important;
        color: #4bd67b !important;
        box-shadow: inset 0 0 20px rgba(75, 214, 123, 0.1) !important;
    }
    
    button[data-testid="baseButton-secondary"] {
        background: linear-gradient(145deg, #351216, #1a0a0b) !important;
        color: #ff4b4b !important;
        box-shadow: inset 0 0 20px rgba(255, 75, 75, 0.1) !important;
    }

    .result-screen {
        animation: fadeIn 1s ease-out;
        padding: 50px;
        border-radius: 20px;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: scale(0.95); }
        to { opacity: 1; transform: scale(1); }
    }
</style>
""", unsafe_allow_html=True)

# --- 3. Baza Danych (Teraz z podziałem na role) ---
# Format: {"kto": "ONA", "tekst": "Treść pytania..."} lub {"kto": "ON", "tekst": "..."}
pytania = [
    {"kto": "ONA", "tekst": "Jakie jest moje ulubione wspomnienie z naszej pierwszej randki?"},
    {"kto": "ON", "tekst": "W czym, według Ciebie, wyglądam najatrakcyjniej na co dzień?"},
    {"kto": "ONA", "tekst": "W jakiej pozycji najszybciej osiągam orgazm?"},
    {"kto": "ON", "tekst": "Jaka jest moja najbardziej skryta fantazja erotyczna?"}
    # Uzupełnij resztę w ten sam sposób!
]

kary_p1 = ["Zdejmij skarpetki.", "Masaż karku."]
kary_p4 = ["Zdejmijcie wszystko.", "Nagroda główna 😈"]
# Uzupełnij swoje listy kar

def wylosuj_kare(n):
    return random.choice(kary_p1 if n < 12 else kary_p4)

# --- 4. Synchronizacja stanu ---
@st.cache_resource
def get_global_state():
    return {"current_q": 0, "status": "pending", "penalty": ""}

state = get_global_state()

# --- WIDOK 1: WYBÓR ROLI ---
if view_type == "selection":
    st.markdown("<div class='elegant-header'>System Zarządzania Atmosferą</div>", unsafe_allow_html=True)
    st.link_button("📺 AKTYWUJ EKRAN TV", "/?view=tv", use_container_width=True)
    st.link_button("📱 AKTYWUJ PILOTA", "/?view=pilot", use_container_width=True)

# --- WIDOK 2: TELEWIZOR ---
elif view_type == "tv":
    q_idx = state["current_q"]
    
    if q_idx < len(pytania):
        obecne_pytanie = pytania[q_idx]
        
        if state["status"] == "pending":
            # Ustalenie stylistyki i imienia na podstawie tego, do kogo jest pytanie
            if obecne_pytanie["kto"] == "ONA":
                badge_class = "turn-ona"
                kolej_imie = IMIE_ONA
            else:
                badge_class = "turn-on"
                kolej_imie = IMIE_ON

            st.markdown(f"<div class='elegant-header'>Runda {q_idx + 1}</div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class='premium-box'>
                <div class='turn-badge {badge_class}'>TERAZ ODPOWIADA: {kolej_imie}</div>
                <div class='gold-text'>{obecne_pytanie['tekst']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        else:
            if state["status"] == "correct":
                st.markdown("<div class='result-screen' style='background: rgba(75, 214, 123, 0.1); border: 1px solid #1a4a30; text-align: center;'><h1 style='color: #4bd67b; font-size: 60px;'>PRAWDA</h1><p style='font-size: 24px;'>Idealnie. Zaraz kolejne pytanie...</p></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='result-screen' style='background: rgba(255, 75, 75, 0.1); border: 1px solid #4a1a20; text-align: center;'><h1 style='color: #ff4b4b; font-size: 40px;'>CZAS NA ZADANIE:</h1><h1 style='color: white; font-size: 50px;'>{state['penalty']}</h1></div>", unsafe_allow_html=True)
            
            time.sleep(5)
            state["current_q"] += 1
            state["status"] = "pending"
            st.rerun()
    else:
        st.markdown("<div class='premium-box'><div class='gold-text'>KONIEC GRY.<br>Czas na Was.</div></div>", unsafe_allow_html=True)
    
    time.sleep(1)
    st.rerun()

# --- WIDOK 3: PILOT ---
elif view_type == "pilot":
    q_idx = state["current_q"]
    
    if q_idx < len(pytania):
        obecne_pytanie = pytania[q_idx]
        osoba_oceniana = IMIE_ONA if obecne_pytanie["kto"] == "ONA" else IMIE_ON
        
        st.markdown("<div class='elegant-header'>Werdykt</div>", unsafe_allow_html=True)
        # Mała informacja dla Sędziego, kogo aktualnie ocenia
        st.markdown(f"<p style='text-align: center; color: #8c7a96;'>Oceniasz odpowiedź osoby: <b>{osoba_oceniana}</b></p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("TAK", use_container_width=True, type="primary"):
            state["status"] = "correct"
            st.rerun()
            
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        if st.button("NIE", use_container_width=True):
            state["status"] = "wrong"
            state["penalty"] = wylosuj_kare(q_idx)
            st.rerun()
    else:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<div class='elegant-header' style='text-align: center; font-size: 24px; color: #d4af37;'>Koniec pytań!<br>Bawcie się dobrze! 😈</div>", unsafe_allow_html=True)

    st.markdown("<br><br><br><br><hr>", unsafe_allow_html=True)
    if st.button("🔄 ZRESETUJ GRĘ", use_container_width=True):
        state["current_q"] = 0
        state["status"] = "pending"
        st.rerun()
