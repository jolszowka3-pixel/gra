import streamlit as st
import random
import time

# --- 1. Konfiguracja ---
IMIE_ONA = "Ona"   
IMIE_ON = "On"     

st.set_page_config(page_title="Wieczór we Dwoje", layout="wide", page_icon="🥂")
query_params = st.query_params
view_type = query_params.get("view", "selection")

# --- 2. CSS ---
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

    /* PILOT */
    div.stButton > button {
        height: 30vh !important; width: 100% !important;
        border-radius: 30px !important; margin-top: 2vh;
        box-shadow: 0 15px 30px rgba(0,0,0,0.8) !important;
    }
    div.stButton > button p { font-size: 60px !important; font-weight: bold !important; }
    button[kind="primary"], button[kind="secondary"] {
        background: linear-gradient(145deg, #1a1323, #0d0a13) !important;
        border: 2px solid #d4af37 !important;
    }
    button[kind="primary"] p, button[kind="secondary"] p { color: #d4af37 !important; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. BAZA DANYCH (PYTANIA O "MNIE")
# ==========================================

toasty = ["Wypijcie za Waszą namiętność! 🥂", "Toast za najodważniejszą osobę w tym pokoju! 🔥"]

# Pytania poziomu 1 (Delikatne)
p1 = [
    {"kto": "ONA", "tekst": "Jaka jest moja ulubiona część Twojego ciała?"},
    {"kto": "ON", "tekst": "W którym z Twoich ubrań podobasz mi się najbardziej?"},
    {"kto": "ONA", "tekst": "Jaki komplement z Twoich ust sprawia, że najbardziej promieniuję?"},
    {"kto": "ON", "tekst": "Co jest moją największą pasją, o której mógłbym opowiadać godzinami?"}
]

# Pytania poziomu 2 (Zmysłowe)
p2 = [
    {"kto": "ONA", "tekst": "Gdzie na moim ciele dotyk Twoich ust sprawia mi największą przyjemność?"},
    {"kto": "ON", "tekst": "Jaka pieszczota z Twojej strony najszybciej mnie pobudza?"},
    {"kto": "ONA", "tekst": "Wolisz mnie w pełnym makijażu i bieliźnie, czy rano, naturalną w Twojej za dużej koszulce?"},
    {"kto": "ON", "tekst": "Gdybyś miała wybrać jeden zapach, który kojarzy Ci się ze mną, co by to było?"}
]

# Pytania poziomu 3 (Pikantne)
p3 = [
    {"kto": "ONA", "tekst": "Jaka jest moja ulubiona pozycja, w której czuję się najbardziej usatysfakcjonowana?"},
    {"kto": "ON", "tekst": "Gdybym miał wybrać jedno miejsce poza sypialnią na szybki numerek, co bym wybrał?"},
    {"kto": "ONA", "tekst": "Jakie słowa wyszeptane mi do ucha podczas seksu działają na mnie najmocniej?"},
    {"kto": "ON", "tekst": "Co kręci mnie bardziej: kiedy dominujesz, czy kiedy ja przejmuję stery?"}
]

# Pytania poziomu 4 (Ekstremalne)
p4 = [
    {"kto": "ONA", "tekst": "Jaka jest moja najskrytsza fantazja, której jeszcze nie zrealizowaliśmy?"},
    {"kto": "ON", "tekst": "Który gadżet lub dodatek najbardziej chciałbym wypróbować na Tobie dzisiaj?"},
    {"kto": "ONA", "tekst": "Gdybym mogła Cię uwiązać i robić z Tobą co zechcę przez 5 minut, co byłoby pierwsze?"},
    {"kto": "ON", "tekst": "Co w Twoim zachowaniu w łóżku sprawia, że tracę nad sobą panowanie?"}
]

kary_l1 = ["Całuj moją szyję przez minutę.", "Zrób mi masaż dłoni."]
kary_l2 = ["Zdejmij z siebie jedną rzecz.", "Pocałuj moje wewnętrzne udo."]
kary_l3 = ["Zliż kroplę alkoholu z mojego brzucha.", "Zostań tylko w bieliźnie."]
kary_l4 = ["Zaspokajaj mnie ustami przez minutę.", "Rób ze mną co chcesz przez 2 minuty."]

def generuj_gre():
    # Losujemy po 5 pytań z każdego poziomu, żeby zachować progresję
    talia = random.sample(p1, 2) + random.sample(p2, 2) + random.sample(p3, 2) + random.sample(p4, 2)
    finalna = []
    for i, q in enumerate(talia):
        if i > 0 and i % 4 == 0: finalna.append({"kto": "TOAST", "tekst": random.choice(toasty)})
        finalna.append(q)
    return finalna

def wylosuj_kare(idx, total):
    progres = idx / total
    if progres < 0.25: return random.choice(kary_l1)
    if progres < 0.50: return random.choice(kary_l2)
    if progres < 0.75: return random.choice(kary_l3)
    return random.choice(kary_l4)

# --- Stan gry ---
if "state" not in st.session_state:
    st.session_state.state = {"current_q": 0, "status": "question", "penalty": "", "gra": generuj_gre()}

s = st.session_state.state

# --- WIDOKI ---
if view_type == "selection":
    st.link_button("📺 EKRAN TV", "/?view=tv")
    st.link_button("📱 PILOT", "/?view=pilot")

elif view_type == "tv":
    if s["current_q"] < len(s["gra"]):
        q = s["gra"][s["current_q"]]
        if s["status"] == "question":
            color = "turn-ona" if q["kto"] == "ONA" else "turn-on"
            if q["kto"] == "TOAST": color = "turn-toast"
            st.markdown(f"<div class='elegant-header'>Runda {s['current_q']+1}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='premium-box'><div class='turn-badge {color}'>CZYTA: {IMIE_ONA if q['kto'] == 'ONA' else IMIE_ON if q['kto'] == 'ON' else 'WSZYSCY'}</div><div class='gold-text'>{q['tekst']}</div></div>", unsafe_allow_html=True)
            time.sleep(1); st.rerun()
        else:
            txt = "PRAWDA" if s["penalty"] == "" else f"ZADANIE: {s['penalty']}"
            bg = "rgba(75,214,123,0.1)" if s["penalty"] == "" else "rgba(255,75,75,0.1)"
            st.markdown(f"<div class='premium-box' style='background:{bg};'><h1 class='gold-text'>{txt}</h1></div>", unsafe_allow_html=True)
            time.sleep(5); s["current_q"] += 1; s["status"] = "question"; st.rerun()
    else:
        st.markdown("<div class='premium-box'><h1 class='gold-text'>KONIEC</h1></div>", unsafe_allow_html=True)

elif view_type == "pilot":
    if s["current_q"] < len(s["gra"]):
        q = s["gra"][s["current_q"]]
        if q["kto"] == "TOAST":
            if st.button("WYPITE 🥂", type="primary"): s["status"] = "result"; s["penalty"] = ""; st.rerun()
        else:
            st.markdown(f"<p style='text-align:center;'>Sędziuje: {IMIE_ONA if q['kto'] == 'ONA' else IMIE_ON}</p>", unsafe_allow_html=True)
            if st.button("TAK", type="primary"): s["status"] = "result"; s["penalty"] = ""; st.rerun()
            if st.button("NIE", type="secondary"): s["status"] = "result"; s["penalty"] = wylosuj_kare(s["current_q"], len(s["gra"])); st.rerun()
    if st.button("Reset"): s["current_q"] = 0; s["gra"] = generuj_gre(); st.rerun()
