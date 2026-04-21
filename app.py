import streamlit as st
import random
import time

# ==========================================
# 1. KONFIGURACJA I WASZE IMIONA
# ==========================================
IMIE_ONA = "Ona"   # <-- Wpisz jej imię!
IMIE_ON = "On"     # <-- Wpisz swoje imię!
LICZBA_RUND = 40   

st.set_page_config(page_title="Wieczór we Dwoje", layout="wide", page_icon="🥂")
query_params = st.query_params
view_type = query_params.get("view", "selection")

# ==========================================
# 2. GŁÓWNY CSS (PREMIUM GOLD)
# ==========================================
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
        border: 1px solid #2a2035; border-radius: 25px;
        padding: 60px 40px; box-shadow: 0 30px 60px rgba(0, 0, 0, 0.8);
        text-align: center; margin: 40px auto; max-width: 1000px;
    }
    .gold-text {
        font-size: 54px; font-weight: 300; color: #d4af37; 
        text-shadow: 0 4px 20px rgba(212, 175, 55, 0.3); line-height: 1.4;
    }
    .elegant-header {
        color: #8c7a96; font-size: 18px; text-transform: uppercase;
        letter-spacing: 6px; text-align: center; margin-top: 20px;
    }
    .turn-badge {
        display: inline-block; padding: 8px 24px; border-radius: 30px;
        font-size: 20px; font-weight: 400; letter-spacing: 4px;
        margin-bottom: 30px; text-transform: uppercase; box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    .turn-ona { background-color: rgba(212, 175, 55, 0.1); border: 1px solid #d4af37; color: #d4af37; }
    .turn-on { background-color: rgba(140, 122, 150, 0.1); border: 1px solid #8c7a96; color: #8c7a96; }
    .turn-toast { background-color: rgba(255, 75, 75, 0.1); border: 1px solid #ff4b4b; color: #ff4b4b; }

    /* PRZYCISKI PILOTA */
    div.stButton > button {
        height: 30vh !important; width: 100% !important;
        border-radius: 30px !important; margin-top: 2vh;
        box-shadow: 0 15px 30px rgba(0,0,0,0.8) !important;
        background: linear-gradient(145deg, #1a1323, #0d0a13) !important;
        border: 2px solid #d4af37 !important;
    }
    div.stButton > button p { 
        font-size: 60px !important; font-weight: bold !important; 
        color: #d4af37 !important; text-shadow: 0 4px 15px rgba(212, 175, 55, 0.3) !important;
    }

    div.stButton:last-of-type > button {
        height: 50px !important; background-color: transparent !important;
        border: 1px solid #2a2035 !important; box-shadow: none !important;
        margin-top: 10vh !important;
    }
    div.stButton:last-of-type > button p { font-size: 16px !important; color: #8c7a96 !important; text-shadow: none !important;}

    div[data-testid="stLinkButton"] > a {
        background: linear-gradient(145deg, #1a1323, #0d0a13) !important;
        border: 1px solid #d4af37 !important; color: #d4af37 !important;
        border-radius: 20px !important; padding: 25px !important;
        font-size: 24px !important; text-align: center !important;
        display: block !important; text-decoration: none !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. BAZA DANYCH (CZYTA O SOBIE)
# ==========================================

toasty = [
    "Wypijcie zdrowy łyk za Waszą namiętność! 🥂",
    "Toast za najseksowniejszą osobę w tym pokoju! 🔥",
    "Pijemy za wszystkie grzechy, które dzisiaj popełnicie! 😈",
    "Czas na toast bez użycia rąk! Podajcie sobie kieliszek do ust. 🍷"
]

p1 = [
    {"kto": "ONA", "tekst": "Jaka była Twoja pierwsza myśl, kiedy mnie zobaczyłeś?"},
    {"kto": "ON", "tekst": "Co uważam za Twoją najbardziej uroczą cechę charakteru?"},
    {"kto": "ONA", "tekst": "W jakim Twoim stroju lubię Cię najbardziej?"},
    {"kto": "ON", "tekst": "Jaka jest moja ulubiona część Twojego ciała?"}
]

p2 = [
    {"kto": "ONA", "tekst": "Gdzie na moim ciele dotyk Twoich ust sprawia mi największą przyjemność?"},
    {"kto": "ON", "tekst": "Jaka pieszczota z Twojej strony najszybciej mnie pobudza?"},
    {"kto": "ONA", "tekst": "Jakie słowa szeptane przez Ciebie do ucha kręcą mnie najbardziej?"}
]

p3 = [
    {"kto": "ONA", "tekst": "Jaka jest moja ulubiona pozycja, w której czuję się najbardziej spełniona?"},
    {"kto": "ON", "tekst": "Jakie miejsce poza sypialnią najbardziej mnie kręci, by to zrobić?"},
    {"kto": "ONA", "tekst": "Jaka jest moja najskrytsza fantazja, której jeszcze nie zrealizowaliśmy?"}
]

kary_l1 = ["Całuj moją szyję przez minutę.", "Zrób mi masaż dłoni."]
kary_l2 = ["Zdejmij jedną rzecz.", "Weź łyk alkoholu i przekaż mi go ustami."]
kary_l3 = ["Zliż kroplę alkoholu z moich obojczyków.", "Zostań tylko w bieliźnie."]
kary_l4 = ["Zaspokajaj mnie ustami przez minutę.", "Zdejmij wszystko."]

def generuj_gre():
    talia = random.sample(p1, min(len(p1), 5)) + random.sample(p2, min(len(p2), 5)) + random.sample(p3, min(len(p3), 5))
    finalna = []
    for i, q in enumerate(talia):
        if i > 0 and i % 5 == 0:
            finalna.append({"kto": "TOAST", "tekst": random.choice(toasty)})
        finalna.append(q)
    return finalna

def wylosuj_kare(idx, total):
    progres = idx / total
    if progres < 0.25: return random.choice(kary_l1)
    if progres < 0.50: return random.choice(kary_l2)
    if progres < 0.75: return random.choice(kary_l3)
    return random.choice(kary_l4)

# ==========================================
# 4. SYNCHRONIZACJA STANU
# ==========================================
@st.cache_resource
def get_global_state():
    return {"current_q": 0, "status": "question", "penalty": "", "gra": generuj_gre()}

state = get_global_state()

# ==========================================
# 5. WIDOKI
# ==========================================

if view_type == "selection":
    st.markdown("<div class='elegant-header'>System Wieczoru</div><br>", unsafe_allow_html=True)
    st.link_button("📺 AKTYWUJ EKRAN TV", "/?view=tv", use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.link_button("📱 AKTYWUJ PILOTA", "/?view=pilot", use_container_width=True)

elif view_type == "tv":
    q_idx = state["current_q"]
    if q_idx < len(state["gra"]):
        q = state["gra"][q_idx]
        if state["status"] == "question":
            who_val = str(q["kto"]).upper().strip()
            if who_val == "TOAST":
                badge_class, imie_info = "turn-toast", "CZAS NA TOAST!"
            else:
                badge_class = "turn-ona" if who_val == "ONA" else "turn-on"
                imie_info = f"CZYTA: {IMIE_ONA if who_val == 'ONA' else IMIE_ON}"

            st.markdown(f"<div class='elegant-header'>Runda {q_idx + 1}</div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class='premium-box'>
                <div class='turn-badge {badge_class}'>{imie_info}</div>
                <div class='gold-text'>{q['tekst']}</div>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(1); st.rerun()
        else:
            txt = "PRAWDA" if state["penalty"] == "" else f"ZADANIE: {state['penalty']}"
            bg = "rgba(75,214,123,0.1)" if state["penalty"] == "" else "rgba(255,75,75,0.1)"
            st.markdown(f"""
            <div class='premium-box' style='background:{bg};'>
                <h1 class='gold-text'>{txt}</h1>
                <p style='color: #8c7a96;'>Złota Zasada: Możesz wykupić się shotem! 🥃</p>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(6); state["current_q"] += 1; state["status"] = "question"; st.rerun()
    else:
        st.markdown("<div class='premium-box'><h1 class='gold-text'>KONIEC GRY.😈</h1></div>", unsafe_allow_html=True)

elif view_type == "pilot":
    q_idx = state["current_q"]
    if q_idx < len(state["gra"]):
        q = state["gra"][q_idx]
        who_val = str(q["kto"]).upper().strip()
        
        if who_val == "TOAST":
            if st.button("WYPITE! 🥂", use_container_width=True):
                state["status"] = "result"; state["penalty"] = ""; st.rerun()
        else:
            # FIX: Pilot teraz precyzyjnie sprawdza, kto czyta i sędziuje
            sedzia = IMIE_ONA if who_val == "ONA" else IMIE_ON
            st.markdown(f"<p style='text-align:center; color:#d4af37; font-size:20px; letter-spacing:2px;'>Sędziuje teraz: <b>{sedzia}</b></p>", unsafe_allow_html=True)
            
            if st.button("TAK", use_container_width=True, type="primary"):
                if state["status"] == "question":
                    state["status"] = "result"
                    state["penalty"] = ""
                    st.rerun()
            
            if st.button("NIE", use_container_width=True, type="secondary"):
                if state["status"] == "question":
                    state["status"] = "result"
                    state["penalty"] = wylosuj_kare(q_idx, len(state["gra"]))
                    st.rerun()
    
    if st.button("WYLOSUJ NOWĄ GRĘ (RESET)"):
        state["gra"] = generuj_gre(); state["current_q"] = 0; state["status"] = "question"; st.rerun()
