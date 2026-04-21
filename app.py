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

    /* --- STYL PRZYCISKÓW --- */
    div[data-testid="stLinkButton"] > a {
        background: linear-gradient(145deg, #1a1323, #0d0a13) !important;
        border: 1px solid #d4af37 !important; color: #d4af37 !important;
        border-radius: 20px !important; text-decoration: none !important;
        font-size: 24px !important; font-weight: 300 !important;
        letter-spacing: 4px !important; padding: 25px !important;
        display: flex !important; justify-content: center !important;
        box-shadow: 0 15px 30px rgba(0,0,0,0.6) !important;
    }

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
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. ROZBUDOWANA BAZA DANYCH (150+ ELEMENTÓW)
# ==========================================

toasty = [
    "Wypijcie za Waszą namiętność! 🥂",
    "Toast za najseksowniejszą osobę w tym pokoju! 🔥",
    "Pijemy za wszystkie grzechy, które dzisiaj popełnicie! 😈",
    "Czas na toast bez użycia rąk! Podajcie sobie kieliszek do ust. 🍷",
    "Toast za ten moment, w którym po raz pierwszy poczuliście do siebie pożądanie.",
    "Wypijcie za Wasze ulubione miejsce na wspólne randki.",
    "Toast za każdą minutę dzisiejszej nocy, która jest jeszcze przed Wami!"
]

# Poziom 1: Flirt i wiedza o sobie (Rozgrzewka)
p1 = [
    {"kto": "ONA", "tekst": "Jaka była Jego pierwsza myśl, kiedy zobaczył Cię po raz pierwszy?"},
    {"kto": "ON", "tekst": "Co Ona uważa za Twój najbardziej uroczy, mały nawyk?"},
    {"kto": "ONA", "tekst": "W jakim Twoim stroju On najchętniej widziałby Cię na romantycznej kolacji?"},
    {"kto": "ON", "tekst": "Jaki kolor ubrań najbardziej pociąga Ją u Ciebie?"},
    {"kto": "ONA", "tekst": "Która część Twojej twarzy jest Jego ulubioną do całowania?"},
    {"kto": "ON", "tekst": "Jakie jest Jej ulubione wspomnienie z Waszych pierwszych wakacji lub wyjazdu?"},
    {"kto": "ONA", "tekst": "Jaki Twój cecha charakteru sprawia, że On czuje się przy Tobie wyjątkowo?"},
    {"kto": "ON", "tekst": "Jaki komplement z Twoich ust sprawia Jej najwięcej frajdy?"},
    {"kto": "ONA", "tekst": "Gdyby On mógł zmienić jedną rzecz w Twojej szafie, co by to było?"},
    {"kto": "ON", "tekst": "Co Ona uważa za Twój największy męski atut?"}
]

# Poziom 2: Zmysły i dotyk (Temperatura rośnie)
p2 = [
    {"kto": "ONA", "tekst": "Gdzie na ciele dotyk Jego dłoni wywołuje u Ciebie najszybsze dreszcze?"},
    {"kto": "ON", "tekst": "Jaka pieszczota z Twojej strony jest dla Niej najbardziej relaksująca?"},
    {"kto": "ONA", "tekst": "Jaki zapach Twojego ciała lub perfum On uwielbia najbardziej?"},
    {"kto": "ON", "tekst": "Woli Cię w bieliźnie sportowej czy koronkowej (według Jej gustu)?"},
    {"kto": "ONA", "tekst": "Jakie tempo pocałunków On preferuje: powolne i zmysłowe, czy dzikie?"},
    {"kto": "ON", "tekst": "Gdybyś miał Ją pocałować w jedno miejsce poza ustami – co Ona by wybrała?"},
    {"kto": "ONA", "tekst": "Co On najbardziej lubi robić z Twoimi włosami?"},
    {"kto": "ON", "tekst": "Który moment w ciągu dnia Ona uważa za najbardziej seksowny u Ciebie?"},
    {"kto": "ONA", "tekst": "Jakie słowa szeptane przez Niego do ucha najbardziej Cię rozpalają?"},
    {"kto": "ON", "tekst": "Co Ona uważa za najbardziej namiętny moment, jaki dotąd przeżyliście?"}
]

# Poziom 3: Fantazje i sypialnia (Pikantnie)
p3 = [
    {"kto": "ONA", "tekst": "Jaka jest Jego ulubiona pozycja, w której czuje się najbardziej męsko?"},
    {"kto": "ON", "tekst": "Co Ona myśli o seksie w miejscach publicznych – kręci Ją to czy stresuje?"},
    {"kto": "ONA", "tekst": "Jakie miejsce poza sypialnią w tym domu On uważa za najgorętsze?"},
    {"kto": "ON", "tekst": "Co Ona najbardziej lubi robić swoimi rękami podczas Waszych zbliżeń?"},
    {"kto": "ONA", "tekst": "Jaką fantazję On chciałby zrealizować z Tobą w najbliższym czasie?"},
    {"kto": "ON", "tekst": "Co Ona uważa za swój najbardziej erogenny punkt na ciele?"},
    {"kto": "ONA", "tekst": "Kto z Was, według Niego, częściej przejmuje inicjatywę w łóżku?"},
    {"kto": "ON", "tekst": "Woli seks przy pełnym świetle, czy w całkowitej ciemności (według Jej opinii)?"},
    {"kto": "ONA", "tekst": "Jakie dźwięki, które wydajesz, On uważa za najbardziej podniecające?"},
    {"kto": "ON", "tekst": "Jaką rolę w sypialni Ona chciałaby dzisiaj przyjąć: uległą czy dominującą?"}
]

# Poziom 4: Pełen ogień (Ekstremalne fantazje)
p4 = [
    {"kto": "ONA", "tekst": "Jaka jest Jego najskrytsza fantazja, o której wstydził się powiedzieć na początku?"},
    {"kto": "ON", "tekst": "Gdybyście mieli dołączyć do zabawy gadżet, co Ona by wybrała jako pierwsze?"},
    {"kto": "ONA", "tekst": "W jakiej pozycji On uważa, że wyglądasz najbardziej wyzywająco?"},
    {"kto": "ON", "tekst": "Co w Twoim zachowaniu w łóżku sprawia, że On całkowicie traci nad sobą panowanie?"},
    {"kto": "ONA", "tekst": "Gdybyś mogła Go uwiązać i robić z Nim co zechcesz – co byłoby Twoim pierwszym krokiem?"},
    {"kto": "ON", "tekst": "Jaka jest najbardziej wyuzdana rzecz, jaką kiedykolwiek o Tobie pomyślała?"},
    {"kto": "ONA", "tekst": "Którą część Twojego ciała On chciałby teraz pieścić językiem najdłużej?"},
    {"kto": "ON", "tekst": "Co według Niej sprawia, że Wasz seks jest wyjątkowy na tle innych doświadczeń?"}
]

# --- ROZBUDOWANE KARY ---
kary_l1 = [
    "Całuj moją szyję przez minutę, omijając usta.",
    "Zrób mi 2-minutowy, zmysłowy masaż dłoni i palców.",
    "Zdejmij ze mnie skarpetki, używając tylko jednej ręki.",
    "Patrz mi prosto w oczy przez 60 sekund, nie odrywając wzroku.",
    "Wypisz palcem na moich plecach 3 słowa, które do mnie czujesz.",
    "Pocałuj mnie w oba policzki, czoło i czubek nosa.",
    "Miziaj mnie po włosach aż do kolejnej rundy.",
    "Powiedz mi szeptem, co najbardziej we mnie dzisiaj lubisz."
]

kary_l2 = [
    "Weź łyk alkoholu i przekaż mi go ustami bez użycia rąk.",
    "Zdejmij z siebie jedną, wybraną przez partnera część garderoby.",
    "Pocałuj powoli moje wewnętrzne udo, ale nie idź dalej.",
    "Przygryź delikatnie płatek mojego ucha i szepnij coś niegrzecznego.",
    "Zrób mi masaż stóp, używając do tego odrobiny balsamu lub alkoholu.",
    "Przejedź kostką lodu (lub zimnym palcem) wzdłuż mojego kręgosłupa.",
    "Rozepnij mój biustonosz / koszulę, ale jeszcze ich nie zdejmuj.",
    "Usiądź na moich kolanach okrakiem przez całą kolejną rundę."
]

kary_l3 = [
    "Zliż odrobinę alkoholu z mojego brzucha lub obojczyka.",
    "Zostań tylko w bieliźnie na resztę tej fazy gry.",
    "Wymasuj moje pośladki, patrząc mi głęboko w oczy.",
    "Zawiąż mi oczy na jedną rundę i rób z moimi zmysłami co chcesz.",
    "Pocałuj mnie namiętnie, dociskając moje ciało do ściany lub łóżka.",
    "Przejedź językiem od mojego pępka aż do wgłębienia między piersiami.",
    "Wymasuj moją klatkę piersiową / piersi z użyciem olejku lub drinka.",
    "Zdejmij z partnera kolejną część ubrania za pomocą samych zębów."
]

kary_l4 = [
    "Zaspokajaj mnie ustami przez pełną minutę.",
    "Rób z moim ciałem co chcesz przez najbliższe 3 minuty.",
    "Zdejmij z siebie absolutnie wszystko. Resztę gry prowadzisz nago.",
    "Użyj na partnerze wybranego gadżetu lub dłoni w sposób ekstremalny przez 2 minuty.",
    "Zwiąż moje ręce (np. paskiem) i nie pozwól mi się ruszyć przez jedną rundę.",
    "Resztę pytań czytacie i odpowiadacie na nie, będąc w ścisłym kontakcie cielesnym.",
    "Odłóżcie telefony na 5 minut. Czas na sesję bez granic. 😈",
    "Zdejmij wszystko z partnera i złóż na jego ciele 10 pocałunków w 10 różnych miejscach."
]

def generuj_gre():
    talia = random.sample(p1, 10) + random.sample(p2, 10) + random.sample(p3, 10) + random.sample(p4, 10)
    finalna = []
    for i, q in enumerate(talia):
        if i > 0 and i % 6 == 0:
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
# 4. SILNIK SYNCHRONIZACJI I WIDOKI
# ==========================================
@st.cache_resource
def get_global_state():
    return {"current_q": 0, "status": "question", "penalty": "", "gra": generuj_gre()}

state = get_global_state()

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
    if st.button("ZRESETUJ I LOSUJ NOWĄ GRĘ"):
        state["current_q"] = 0; state["status"] = "question"; state["gra"] = generuj_gre(); st.rerun()
