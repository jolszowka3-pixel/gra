import streamlit as st
import random
import time

# --- 1. Konfiguracja i Wasze Imiona ---
IMIE_ONA = "BASIA"   # <-- Wpisz tu jej imię!
IMIE_ON = "KUBA"     # <-- Wpisz tu swoje imię!

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

    /* Przyciski Pilota (Większe i głębsze kolory) */
    .stButton > button {
        height: 160px !important;
        border-radius: 30px !important;
        font-size: 40px !important;
        font-weight: 300 !important;
        letter-spacing: 8px !important;
        transition: all 0.4s ease !important;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6) !important;
        border: none !important;
    }

    button[data-testid="baseButton-primary"] {
        background: linear-gradient(145deg, #123524, #0a1a11) !important;
        color: #4bd67b !important;
    }
    
    button[data-testid="baseButton-secondary"] {
        background: linear-gradient(145deg, #351216, #1a0a0b) !important;
        color: #ff4b4b !important;
    }

    /* Animacja dla osoby odpowiadającej */
    @keyframes pulse-gold {
        0% { transform: scale(0.98); box-shadow: 0 0 0 0 rgba(212, 175, 55, 0.4); }
        70% { transform: scale(1); box-shadow: 0 0 20px 15px rgba(212, 175, 55, 0); }
        100% { transform: scale(0.98); box-shadow: 0 0 0 0 rgba(212, 175, 55, 0); }
    }
    .answering-box {
        animation: pulse-gold 2.5s infinite;
        padding: 40px;
        border-radius: 20px;
        border: 1px solid #d4af37;
        background: rgba(212, 175, 55, 0.05);
        text-align: center;
        margin-top: 50px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. Baza Danych ---
pytania = [
    {"kto": "ONA", "tekst": "Jakie jest moje ulubione wspomnienie z naszej pierwszej randki?"},
    {"kto": "ON", "tekst": "W czym, według Ciebie, wyglądam najatrakcyjniej na co dzień?"},
    {"kto": "ONA", "tekst": "W jakiej pozycji najszybciej osiągam orgazm?"},
    {"kto": "ON", "tekst": "Jaka jest moja najbardziej skryta fantazja erotyczna?"}
    # Pamiętaj wkleić tu resztę pytań!
]

kary_p1 = ["Zdejmij skarpetki.", "Masaż karku."]
kary_p4 = ["Zdejmijcie wszystko.", "Nagroda główna 😈"]

def wylosuj_kare(n):
    return random.choice(kary_p1 if n < 12 else kary_p4)

# --- 4. Synchronizacja stanu ---
@st.cache_resource
def get_global_state():
    return {"current_q": 0, "status": "pending", "penalty": ""}

state = get_global_state()

# --- WIDOK 1: WYBÓR ROLI ---
if view_type == "selection":
    st.markdown("<div class='elegant-header'>Wybierz Urządzenie</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.link_button("📺 AKTYWUJ EKRAN TV", "/?view=tv", use_container_width=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.link_button(f"📱 Telefon: {IMIE_ONA}", "/?view=pilot_ona", use_container_width=True)
    st.link_button(f"📱 Telefon: {IMIE_ON}", "/?view=pilot_on", use_container_width=True)

# --- WIDOK 2: TELEWIZOR ---
elif view_type == "tv":
    q_idx = state["current_q"]
    
    if q_idx < len(pytania):
        obecne_pytanie = pytania[q_idx]
        
        if state["status"] == "pending":
            if obecne_pytanie["kto"] == "ONA":
                badge_class, kolej_imie = "turn-ona", IMIE_ONA
            else:
                badge_class, kolej_imie = "turn-on", IMIE_ON

            st.markdown(f"<div class='elegant-header'>Runda {q_idx + 1}</div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class='premium-box'>
                <div class='turn-badge {badge_class}'>TERAZ ODPOWIADA: {kolej_imie}</div>
                <div class='gold-text'>{obecne_pytanie['tekst']}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            if state["status"] == "correct":
                st.markdown("<div class='premium-box' style='background: rgba(75, 214, 123, 0.1); border: 1px solid #1a4a30;'><h1 style='color: #4bd67b; font-size: 60px;'>PRAWDA</h1><p style='font-size: 24px; color: white;'>Idealnie. Zaraz kolejne pytanie...</p></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='premium-box' style='background: rgba(255, 75, 75, 0.1); border: 1px solid #4a1a20;'><h1 style='color: #ff4b4b; font-size: 40px;'>CZAS NA ZADANIE:</h1><h1 style='color: white; font-size: 50px;'>{state['penalty']}</h1></div>", unsafe_allow_html=True)
            
            time.sleep(5)
            state["current_q"] += 1
            state["status"] = "pending"
            st.rerun()
    else:
        st.markdown("<div class='premium-box'><div class='gold-text'>KONIEC GRY.<br>Czas na Was.</div></div>", unsafe_allow_html=True)
    
    time.sleep(1)
    st.rerun()

# --- WIDOK 3: PILOTY (ON i ONA) ---
elif view_type in ["pilot_ona", "pilot_on"]:
    # 1. Sprawdzamy kim jesteś na podstawie linku
    kto_ja = "ONA" if view_type == "pilot_ona" else "ON"
    moje_imie = IMIE_ONA if kto_ja == "ONA" else IMIE_ON
    
    q_idx = state["current_q"]
    
    if q_idx < len(pytania):
        # Jeśli wynik jest właśnie wyświetlany na TV (5 sekund pauzy)
        if state["status"] != "pending":
            st.markdown("<br><br><br><br>", unsafe_allow_html=True)
            st.markdown("<div class='elegant-header' style='font-size: 24px;'>Spójrz na telewizor... 👀</div>", unsafe_allow_html=True)
            time.sleep(1) # Odświeżamy by wykryć kiedy TV wróci do pytań
            st.rerun()
            
        # Jeśli gra czeka na werdykt
        else:
            obecne_pytanie = pytania[q_idx]
            kto_odpowiada = obecne_pytanie["kto"]
            
            if kto_ja != kto_odpowiada:
                # --- JESTEŚ SĘDZIĄ W TEJ RUNDZIE ---
                osoba_oceniana = IMIE_ON if kto_odpowiada == "ON" else IMIE_ONA
                st.markdown("<div class='elegant-header'>Jesteś Sędzią</div>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center; color: #8c7a96; margin-bottom: 30px;'>Oceniasz odpowiedź osoby: <b>{osoba_oceniana}</b></p>", unsafe_allow_html=True)
                
                if st.button("TAK", use_container_width=True, type="primary"):
                    state["status"] = "correct"
                    st.rerun()
                    
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("NIE", use_container_width=True):
                    state["status"] = "wrong"
                    state["penalty"] = wylosuj_kare(q_idx)
                    st.rerun()
            else:
                # --- JESTEŚ ODPOWIADAJĄCYM W TEJ RUNDZIE ---
                st.markdown("<div class='elegant-header'>Uwaga!</div>", unsafe_allow_html=True)
                st.markdown("""
                <div class='answering-box'>
                    <h1 style='color: #d4af37; font-size: 40px; margin-bottom: 10px;'>Twoja Kolej</h1>
                    <p style='color: #e0d8d3; font-size: 20px;'>Odpowiedz na głos. Twój partner używa swojego telefonu, aby ocenić czy mówisz prawdę...</p>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(1) # Pilot musi się sam odświeżać, żeby wyłapać kliknięcie od partnera
                st.rerun()
    else:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<div class='elegant-header' style='text-align: center; font-size: 24px; color: #d4af37;'>Koniec pytań!<br>Odłóżcie telefony 😈</div>", unsafe_allow_html=True)

    # Przycisk Reset ZAWSZE na dole
    st.markdown("<br><br><br><br><hr>", unsafe_allow_html=True)
    if st.button("🔄 ZRESETUJ GRĘ", use_container_width=True):
        state["current_q"] = 0
        state["status"] = "pending"
        st.rerun()
