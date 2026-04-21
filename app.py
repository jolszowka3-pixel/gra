import streamlit as st
import random

# --- 1. Konfiguracja ---
st.set_page_config(page_title="Gorący Test Zgodności", layout="wide", page_icon="🥂")
query_params = st.query_params
view_type = query_params.get("view", "selection")

# --- 2. Wstrzykiwanie Eleganckiego CSS ---
st.markdown("""
<style>
    /* Główne tło - głęboka, nocna purpura/czerń */
    .stApp {
        background-color: #0a0810;
        background-image: radial-gradient(circle at 50% 0%, #1a1225 0%, #0a0810 70%);
        color: #e0d8d3;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* Ukrycie standardowych elementów interfejsu Streamlita */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Elegancki kontener na pytania z miękkim cieniem */
    .premium-box {
        background: linear-gradient(145deg, #15101c, #0d0a13);
        border: 1px solid #2a2035;
        border-radius: 20px;
        padding: 50px 30px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6), inset 0 2px 2px rgba(255, 255, 255, 0.03);
        text-align: center;
        margin: 20px auto;
        max-width: 900px;
    }
    
    /* Złoty tekst pytania */
    .gold-text {
        font-size: 48px;
        font-weight: 300;
        color: #d4af37; /* Klasyczne złoto */
        text-shadow: 0 4px 15px rgba(212, 175, 55, 0.2);
        line-height: 1.3;
        margin-bottom: 20px;
        letter-spacing: 1px;
    }
    
    /* Stylowe nagłówki */
    .elegant-header {
        color: #8c7a96;
        font-size: 20px;
        text-transform: uppercase;
        letter-spacing: 4px;
        margin-bottom: 10px;
        text-align: center;
    }

    /* Karta Kary - głęboka czerwień */
    .penalty-box {
        background: linear-gradient(145deg, #2b0f12, #1a080a);
        border: 1px solid #4a1a20;
        border-radius: 15px;
        padding: 40px;
        box-shadow: 0 15px 40px rgba(255, 0, 0, 0.15);
        text-align: center;
        animation: fadeIn 0.8s ease-in-out;
    }
    
    /* Karta Sukcesu - butelkowa zieleń */
    .success-box {
        background: linear-gradient(145deg, #0f2b1c, #081a11);
        border: 1px solid #1a4a30;
        border-radius: 15px;
        padding: 40px;
        box-shadow: 0 15px 40px rgba(0, 255, 100, 0.1);
        text-align: center;
        animation: fadeIn 0.8s ease-in-out;
    }
    
    .status-title {
        font-size: 24px;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 15px;
    }
    
    .penalty-title { color: #ff4b4b; }
    .success-title { color: #4bd67b; }
    
    .task-text {
        font-size: 32px;
        color: #ffffff;
        font-weight: 400;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# --- 3. Baza Pytań (Skrócona do kilku dla czytelności kodu - wklej tu swoje 50 z poprzedniej wersji!) ---
pytania = [
    "Jakie jest moje ulubione wspomnienie z naszej pierwszej randki?",
    "W czym, według Ciebie, wyglądam najatrakcyjniej na co dzień?",
    "Jaka cecha mojego charakteru najbardziej Cię pociąga?",
    "Gdzie najczęściej ucieka mój wzrok, gdy się przebierasz?",
    "W jakiej pozycji najszybciej osiągam orgazm?",
    "Jaka jest moja najbardziej skryta fantazja erotyczna?"
    # Uzupełnij resztę pytań z poprzedniej wiadomości
]

# --- 4. Baza Kar (Podzielona na 4 poziomy) ---
kary_poziom_1 = ["Zdejmij skarpetki i/lub buty.", "Zrób mi 2-minutowy masaż karku.", "Patrz mi głęboko w oczy przez 60 sekund."]
kary_poziom_2 = ["Zdejmij koszulkę / bluzkę.", "Pocałuj mnie w szyję z użyciem języka.", "Zawiąż mi oczy na czas kolejnego pytania."]
kary_poziom_3 = ["Zdejmij z siebie bieliznę z górnej partii ciała.", "Zrób mi 5-minutowy zmysłowy masaż.", "Całuj wewnętrzną stronę moich ud przez minutę."]
kary_poziom_4 = ["Zdejmijcie z siebie wszystko. Gra toczy się nago.", "Odłóżcie telefony. Czas na nagrodę główną. 😈"]
# (Tutaj również podmień na pełną listę z poprzedniej odpowiedzi)

def wylosuj_kare(numer_pytania):
    if numer_pytania < 12: return random.choice(kary_poziom_1)
    elif numer_pytania < 25: return random.choice(kary_poziom_2)
    elif numer_pytania < 38: return random.choice(kary_poziom_3)
    else: return random.choice(kary_poziom_4)

# --- 5. Synchronizacja stanu ---
@st.cache_resource
def get_global_state():
    return {"current_q": 0, "status": "pending", "penalty": ""}

state = get_global_state()

# --- WIDOK 1: WYBÓR ROLI ---
if view_type == "selection":
    st.markdown("<div class='elegant-header'>Wieczór we Dwoje</div>", unsafe_allow_html=True)
    st.markdown("<div class='premium-box'><h1 class='gold-text'>Wybierz tryb</h1></div>", unsafe_allow_html=True)
    st.link_button("📺 Ekran Główny (Telewizor)", "/?view=tv", use_container_width=True)
    st.link_button("📱 Pilot (Smartfon)", "/?view=pilot", use_container_width=True)

# --- WIDOK 2: TELEWIZOR ---
elif view_type == "tv":
    q_idx = state["current_q"]
    
    if q_idx < len(pytania):
        st.markdown(f"<div class='elegant-header'>Runda {q_idx + 1} z {len(pytania)}</div>", unsafe_allow_html=True)
        
        # Pytanie w eleganckim pudełku
        st.markdown(f"""
        <div class='premium-box'>
            <div class='gold-text'>{pytania[q_idx]}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Sekcja statusu (pojawia się po ocenie)
        if state["status"] == "wrong":
            st.markdown(f"""
            <div class='penalty-box'>
                <div class='status-title penalty-title'>KARA DO WYKONANIA</div>
                <div class='task-text'>{state['penalty']}</div>
            </div>
            """, unsafe_allow_html=True)
        elif state["status"] == "correct":
            st.markdown("""
            <div class='success-box'>
                <div class='status-title success-title'>IDEALNIE</div>
                <div class='task-text'>Szczera prawda. Obyło się bez kary.</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='premium-box' style='margin-top: 10vh;'>
            <div class='gold-text' style='font-size: 60px;'>Finał.</div>
            <div class='task-text' style='margin-top: 20px;'>Odłóżcie sprzęt, reszta zależy od Was...</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Automatyczne odświeżanie
    import time
    time.sleep(1.5)
    st.rerun()

# --- WIDOK 3: PILOT ---
elif view_type == "pilot":
    st.markdown("<div class='elegant-header'>Twój Pilot Sędziego</div>", unsafe_allow_html=True)
    q_idx = state["current_q"]
    
    if q_idx < len(pytania):
        st.info(f"Oceniasz: **{pytania[q_idx]}**")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ ZALICZONE", use_container_width=True, type="primary"):
                state["status"] = "correct"
                st.rerun()
        with col2:
            if st.button("🟥 KARA", use_container_width=True):
                state["status"] = "wrong"
                state["penalty"] = wylosuj_kare(q_idx)
                st.rerun()
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("➡️ Następne pytanie", use_container_width=True):
            state["status"] = "pending"
            state["current_q"] += 1
            st.rerun()
    else:
        st.success("Koniec pytań. Cieszcie się wieczorem!")
