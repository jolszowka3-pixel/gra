import streamlit as st
import random
import time

# ==========================================
# 1. KONFIGURACJA I WASZE IMIONA
# ==========================================
IMIE_ONA = "Ona"   
IMIE_ON = "On"     

st.set_page_config(page_title="Wieczór we Dwoje", layout="wide", page_icon="🥂")
query_params = st.query_params
view_type = query_params.get("view", "selection")

# ==========================================
# 2. GŁÓWNY CSS (LUKSUSOWY PREMIUM GOLD)
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
        margin-bottom: 30px; text-transform: uppercase;
    }
    .turn-ona { background-color: rgba(212, 175, 55, 0.1); border: 1px solid #d4af37; color: #d4af37; }
    .turn-on { background-color: rgba(140, 122, 150, 0.1); border: 1px solid #8c7a96; color: #8c7a96; }
    .turn-toast { background-color: rgba(255, 75, 75, 0.1); border: 1px solid #ff4b4b; color: #ff4b4b; }

    /* PILOT PRZYCISKI */
    div.stButton > button {
        height: 30vh !important; width: 100% !important;
        border-radius: 30px !important; margin-top: 2vh;
        box-shadow: 0 15px 30px rgba(0,0,0,0.8) !important;
        background: linear-gradient(145deg, #1a1323, #0d0a13) !important;
        border: 2px solid #d4af37 !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button p { 
        font-size: 60px !important; font-weight: bold !important; 
        color: #d4af37 !important; text-shadow: 0 4px 15px rgba(212, 175, 55, 0.3) !important;
    }
    div.stButton > button:active { transform: scale(0.98) !important; }

    /* Reset */
    div.stButton:last-of-type > button {
        height: 50px !important; background-color: transparent !important;
        border: 1px solid #2a2035 !important; box-shadow: none !important;
    }
    div.stButton:last-of-type > button p { font-size: 16px !important; color: #8c7a96 !important; text-shadow: none !important;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. PIKANTNA BAZA DANYCH (TEST ZGODNOŚCI)
# ==========================================

toasty = [
    "Wypijcie za Waszą namiętność! 🥂",
    "Toast za najodważniejszą osobę w tym pokoju! 🔥",
    "Czas na toast bez użycia rąk! Podajcie sobie kieliszek do ust. 🍷",
    "Pijemy za wszystkie grzechy, które dzisiaj popełnicie! 😈"
]

# Poziom 1: Intymność
p1 = [
    {"kto": "ONA", "tekst": "Jaka jest moja ulubiona część Twojego ciała, na którą najczęściej ukradkiem spoglądam?"},
    {"kto": "ON", "tekst": "W którym z Twoich ubrań według Niej wyglądasz najbardziej pociągająco?"},
    {"kto": "ONA", "tekst": "Jaki drobny gest z Twojej strony sprawia, że Ona od razu ma ochotę Cię pocałować?"},
    {"kto": "ON", "tekst": "Jaka jest moja ulubiona cecha Twojej twarzy, gdy się uśmiechasz?"}
]

# Poziom 2: Budowanie napięcia
p2 = [
    {"kto": "ONA", "tekst": "Gdzie na moim ciele dotyk Twoich ust sprawia mi największą przyjemność?"},
    {"kto": "ON", "tekst": "Jakie jest moje ulubione tempo, gdy zaczynamy się całować – powolne czy drapieżne?"},
    {"kto": "ONA", "tekst": "Jaki rodzaj Twojego dotyku sprawia, że natychmiast przechodzą mnie dreszcze?"},
    {"kto": "ON", "tekst": "Który z naszych dotychczasowych pocałunków w miejscu publicznym najbardziej zapadł Jej w pamięć?"}
]

# Poziom 3: Pikantne fantazje
p3 = [
    {"kto": "ONA", "tekst": "Jaka jest moja ulubiona pozycja, w której czuję się najbardziej spełniona?"},
    {"kto": "ON", "tekst": "Jakie miejsce w naszym domu – poza sypialnią – najbardziej mnie kręci, by to zrobić?"},
    {"kto": "ONA", "tekst": "Jakie słowa wyszeptane mi do ucha podczas seksu działają na mnie najmocniej?"},
    {"kto": "ON", "tekst": "Gdybym miał wybrać dzisiaj jedną fantazję do spełnienia, co by to było?"}
]

# Poziom 4: Pełen ogień
p4 = [
    {"kto": "ONA", "tekst": "Gdybyśmy mieli nagrać domowe wideo, od jakiej sceny bym chciała zacząć?"},
    {"kto": "ON", "tekst": "Jaka jest najostrzejsza i najbardziej wyuzdana fantazja, jaka kiedykolwiek przeszła Jej przez myśl?"},
    {"kto": "ONA", "tekst": "Czy bardziej kręci mnie, gdy to Ty dominujesz, czy kiedy ja przejmuję inicjatywę?"},
    {"kto": "ON", "tekst": "Którą część mojego ciała chciałbym, abyś teraz pieściła ustami najdłużej?"}
]

# KARY
kary_l1 = ["Całuj moją szyję przez minutę, powoli schodząc niżej.", "Zdejmij ze mnie skarpetki i/lub buty."]
kary_l2 = ["Zdejmij z siebie jedną część ubrania.", "Weź łyk alkoholu i przekaż mi go ustami bez użycia rąk."]
kary_l3 = ["Zliż odrobinę alkoholu z moich obojczyków lub brzucha.", "Zostań tylko w bieliźnie na resztę gry."]
kary_l4 = ["Zaspokajaj mnie ustami przez 60 sekund.", "Rób z moim ciałem co chcesz przez 3 minuty.", "Zdejmij wszystko."]

def generuj_gre():
    talia = random.sample(p1, 2) + random.sample(p2, 2) + random.sample(p3, 2) + random.sample(p4, 2)
    finalna = []
    for i, q in enumerate(talia):
        if i > 0 and i % 4 == 0:
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
    st.link_button("📺 EKRAN TV", "/?view=tv", use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.link_button("📱 PILOT", "/?view=pilot", use_container_width=True)

elif view_type == "tv":
    q_idx = state["current_q"]
    if q_idx < len(state["gra"]):
        q = state["gra"][q_idx]
        if state["status"] == "question":
            badge = "turn-toast" if q["kto"] == "TOAST" else ("turn-ona" if q["kto"] == "ONA" else "turn-on")
            info = "CZAS NA TOAST!" if q["kto"] == "TOAST" else f"CZYTA: {IMIE_ONA if q['kto'] == 'ONA' else IMIE_ON}"
            st.markdown(f"<div class='elegant-header'>Runda {q_idx + 1}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='premium-box'><div class='turn-badge {badge}'>{info}</div><div class='gold-text'>{q['tekst']}</div></div>", unsafe_allow_html=True)
            time.sleep(1); st.rerun()
        else:
            txt = "PRAWDA" if state["penalty"] == "" else f"ZADANIE: {state['penalty']}"
            bg = "rgba(75,214,123,0.1)" if state["penalty"] == "" else "rgba(255,75,75,0.1)"
            st.markdown(f"<div class='premium-box' style='background:{bg};'><h1 class='gold-text'>{txt}</h1><p style='color: #8c7a96;'>Zasada Wykupnego: Shot alkoholu i pomijasz karę! 🥃</p></div>", unsafe_allow_html=True)
            time.sleep(6); state["current_q"] += 1; state["status"] = "question"; st.rerun()
    else:
        st.markdown("<div class='premium-box'><h1 class='gold-text'>KONIEC GRY.😈</h1></div>", unsafe_allow_html=True)

elif view_type == "pilot":
    q_idx = state["current_q"]
    if q_idx < len(state["gra"]):
        q = state["gra"][q_idx]
        if q["kto"] == "TOAST":
            if st.button("WYPITE! 🥂", use_container_width=True):
                state["status"] = "result"; state["penalty"] = ""; st.rerun()
        else:
            st.markdown(f"<p style='text-align:center; color:#8c7a96;'>Sędziuje: <b>{IMIE_ONA if q['kto'] == 'ONA' else IMIE_ON}</b></p>", unsafe_allow_html=True)
            if st.button("TAK", use_container_width=True, type="primary"):
                state["status"] = "result"; state["penalty"] = ""; st.rerun()
            if st.button("NIE", use_container_width=True, type="secondary"):
                state["status"] = "result"; state["penalty"] = wylosuj_kare(q_idx, len(state["gra"])); st.rerun()
    if st.button("ZRESETUJ GRĘ"):
        state["current_q"] = 0; state["status"] = "question"; state["gra"] = generuj_gre(); st.rerun()
