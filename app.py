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

    /* --- PRZYCISKI PILOTA (GOLD STYLE) --- */
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
        height: 60px !important; background: transparent !important;
        border: 1px solid #2a2035 !important; margin-top: 5vh !important;
    }
    div.stButton:last-of-type > button p { font-size: 18px !important; color: #8c7a96 !important; text-shadow: none !important;}

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
# 3. GIGANTYCZNA BAZA DANYCH
# ==========================================

toasty = [
    "Wypijcie za Waszą namiętność! 🥂",
    "Toast za najseksowniejszą osobę w tym pokoju! 🔥",
    "Pijemy za wszystkie grzechy, które dzisiaj popełnicie! 😈",
    "Czas na toast bez użycia rąk! Podajcie sobie kieliszek do ust. 🍷",
    "Toast za ten moment, w którym po raz pierwszy poczuliście do siebie pożądanie.",
    "Wypijcie za Wasze ulubione wspólne wspomnienie z tego roku.",
    "Za każdą minutę dzisiejszej nocy, która jest jeszcze przed Wami!"
]

# Poziom 1: Flirt, emocje, bliskość (Lajtowe)
p1 = [
    {"kto": "ONA", "tekst": "Jaka była Jego pierwsza myśl, kiedy zobaczył Cię dzisiaj rano?"},
    {"kto": "ON", "tekst": "Co Ona uważa za Twój najbardziej uroczy, mały nawyk?"},
    {"kto": "ONA", "tekst": "Jaki komplement z Jego ust sprawia, że najbardziej promieniejesz?"},
    {"kto": "ON", "tekst": "W jakim stroju Ona najbardziej lubi Cię oglądać na co dzień?"},
    {"kto": "ONA", "tekst": "Która część Twojej twarzy jest Jego ulubioną do całowania?"},
    {"kto": "ON", "tekst": "Jaka cecha Twojego charakteru sprawia, że Ona czuje się przy Tobie bezpiecznie?"},
    {"kto": "ONA", "tekst": "Jakie jest Jego ulubione wspomnienie z naszej pierwszej wspólnej randki?"},
    {"kto": "ON", "tekst": "Jaki Twój drobny gest sprawia Jej zawsze największą radość?"},
    {"kto": "ONA", "tekst": "Jaki jest Jego absolutnie ulubiony zapach Twoich perfum?"},
    {"kto": "ON", "tekst": "O czym Ona najczęściej marzy, kiedy ma wolną chwilę tylko dla siebie?"},
    {"kto": "ONA", "tekst": "W jakiej sytuacji On czuje się najbardziej dumny z bycia Twoim partnerem?"},
    {"kto": "ON", "tekst": "Jaka potrawa w Twoim wykonaniu jest Jej ulubioną?"},
    {"kto": "ONA", "tekst": "Które z naszych wspólnych zdjęć On uważa za najładniejsze?"},
    {"kto": "ON", "tekst": "Co Ona uważa za Twój największy życiowy sukces?"},
    {"kto": "ONA", "tekst": "Jaki film lub serial najbardziej kojarzy Mu się z początkami naszej znajomości?"}
]

# Poziom 2: Zmysły, ciało i budowanie napięcia
p2 = [
    {"kto": "ONA", "tekst": "Gdzie na moim ciele dotyk Twoich dłoni wywołuje u mnie najszybsze dreszcze?"},
    {"kto": "ON", "tekst": "Jakie jest moje ulubione tempo pocałunków (według Jej opinii)?"},
    {"kto": "ONA", "tekst": "Jaki zapach mojego ciała On lubi najbardziej, gdy nie mam na sobie perfum?"},
    {"kto": "ON", "tekst": "Wolisz mnie w bieliźnie czarnej, czerwonej czy białej (według Jej gustu)?"},
    {"kto": "ONA", "tekst": "Który z naszych dotychczasowych pocałunków On pamięta jako najbardziej namiętny?"},
    {"kto": "ON", "tekst": "Jakie słowa szeptane przez Ciebie do Jej ucha rozpalają Ją najbardziej?"},
    {"kto": "ONA", "tekst": "Co On najbardziej lubiłby robić z Twoimi włosami podczas pieszczot?"},
    {"kto": "ON", "tekst": "Gdybyś miał Ją pocałować w jedno miejsce poza ustami – co Ona by wybrała?"},
    {"kto": "ONA", "tekst": "W jakiej pozycji On najbardziej lubi mnie przytulać w nocy?"},
    {"kto": "ON", "tekst": "Jaka część Jej ciała jest według Ciebie najbardziej wrażliwa na dotyk ust?"},
    {"kto": "ONA", "tekst": "Co On myśli o moich dłoniach, gdy Go dotykam?"},
    {"kto": "ON", "tekst": "Która Jej sukienka lub komplet najbardziej pobudza Twoją wyobraźnię?"},
    {"kto": "ONA", "tekst": "Jaki rodzaj masażu On lubi otrzymywać od Ciebie najbardziej?"},
    {"kto": "ON", "tekst": "Co Ona uważa za najbardziej pociągający element Twojego wyglądu rano, tuż po przebudzeniu?"}
]

# Poziom 3: Pikantne preferencje i sypialnia
p3 = [
    {"kto": "ONA", "tekst": "Jaka jest Jego ulubiona pozycja, w której czuje się najbardziej usatysfakcjonowany?"},
    {"kto": "ON", "tekst": "Co Ona myśli o seksie w nietypowych miejscach – czy ma jakieś 'miejsce marzeń'?"},
    {"kto": "ONA", "tekst": "Jakie miejsce poza sypialnią w tym domu On uważa za najbardziej podniecające?"},
    {"kto": "ON", "tekst": "Co Ona najbardziej lubi robić swoimi dłońmi podczas Waszych zbliżeń?"},
    {"kto": "ONA", "tekst": "Jaką fantazję On chciałby zrealizować z Tobą jeszcze w tym miesiącu?"},
    {"kto": "ON", "tekst": "Jakie dźwięki, które Ty wydajesz w łóżku, doprowadzają Ją do szaleństwa?"},
    {"kto": "ONA", "tekst": "Czy On woli długą grę wstępną, czy szybki i intensywny seks (według Twojej wiedzy)?"},
    {"kto": "ON", "tekst": "Jaką rolę w łóżku Ona chciałaby dzisiaj przyjąć: uległą czy dominującą?"},
    {"kto": "ONA", "tekst": "Co On sądzi o używaniu gadżetów w sypialni – który jest Jego ulubionym?"},
    {"kto": "ON", "tekst": "Jaki Twój strój 'specjalny' Ona uważa za absolutny numer jeden?"},
    {"kto": "ONA", "tekst": "O której porze dnia On ma na Ciebie największą ochotę?"},
    {"kto": "ON", "tekst": "Jakie słowa wypowiadane przez Nią podczas seksu najbardziej Cię nakręcają?"},
    {"kto": "ONA", "tekst": "Gdyby On mógł patrzeć na Ciebie przez lustro w sypialni, byłby zachwycony czy skrępowany?"},
    {"kto": "ON", "tekst": "Która część Waszej wspólnej intymności jest dla Niej najważniejsza?"}
]

# Poziom 4: Ekstremalne fantazje i Hardcore
p4 = [
    {"kto": "ONA", "tekst": "Jaka jest Jego najskrytsza fantazja, o której bał się Ci powiedzieć na początku?"},
    {"kto": "ON", "tekst": "W jakiej pozycji Ona dochodzi najszybciej i najbardziej intensywnie?"},
    {"kto": "ONA", "tekst": "Czy On woli, gdy jesteś całkowicie uległa, czy gdy to Ty przejmujesz kontrolę?"},
    {"kto": "ON", "tekst": "Jaka jest najbardziej wyzywająca rzecz, jaką Ona kiedykolwiek o Tobie pomyślała?"},
    {"kto": "ONA", "tekst": "Którą część Twojego ciała On chciałby teraz pieścić językiem najdłużej?"},
    {"kto": "ON", "tekst": "Co według Niej sprawia, że Wasza chemia w sypialni jest tak silna?"},
    {"kto": "ONA", "tekst": "Gdybyś mogła Go uwiązać i robić z Nim co zechcesz – od czego byś zaczęła?"},
    {"kto": "ON", "tekst": "Gdybyście mieli nagrać wspólne wideo, na co Ona położyłaby największy nacisk?"},
    {"kto": "ONA", "tekst": "Jakie miejsce publiczne kręci Go najbardziej jako potencjalna scena seksu?"},
    {"kto": "ON", "tekst": "Co w Twoim zachowaniu sprawia, że Ona całkowicie traci nad sobą panowanie w łóżku?"},
    {"kto": "ONA", "tekst": "Jaki rodzaj 'brudnego mówienia' (dirty talk) On lubi u Ciebie najbardziej?"},
    {"kto": "ON", "tekst": "Gdybyś miał użyć na Niej dzisiaj kostki lodu lub ciepłego wosku – co by wybrała?"}
]

# --- KARY (ZADANIA) ---
kary_l1 = [
    "Całuj moją szyję przez minutę, omijając usta.",
    "Zrób mi 2-minutowy masaż karku i ramion.",
    "Powiedz mi 3 rzeczy, które najbardziej Cię we mnie pociągają.",
    "Zdejmij ze mnie skarpetki, używając tylko jednej ręki.",
    "Patrz mi głęboko w oczy przez 60 sekund bez mrugania.",
    "Napisz palcem na moich plecach zdanie, a ja muszę zgadnąć co to.",
    "Miziaj mnie po włosach aż do zakończenia kolejnej rundy.",
    "Wyszepcz mi do ucha komplement, którego nigdy mi nie mówiłeś/aś."
]

kary_l2 = [
    "Weź łyk alkoholu i przekaż mi go prosto do ust podczas pocałunku.",
    "Zdejmij z siebie jedną, wybraną przeze mnie część garderoby.",
    "Pocałuj powoli moją klatkę piersiową/dekolt, omijając usta.",
    "Przygryź delikatnie płatek mojego ucha i powiedz coś niegrzecznego.",
    "Zdejmij ze mnie jeden element ubrania (zegarek, pasek, biżuteria) zębami.",
    "Wymasuj moje stopy, używając do tego odrobiny balsamu lub olejku.",
    "Usiądź na moich kolanach okrakiem i spędź tak całą rundę.",
    "Przejedź kostką lodu wzdłuż mojego kręgosłupa, od karku aż po lędźwia."
]

kary_l3 = [
    "Zliż odrobinę alkoholu z mojego brzucha lub szyi.",
    "Zostań tylko w bieliźnie na resztę tej części gry.",
    "Pieść moje ucho i szyję językiem przez pełną minutę.",
    "Wymasuj moje pośladki dłońmi, patrząc mi głęboko w oczy.",
    "Zdejmij moją koszulkę lub bluzkę, używając tylko zębów.",
    "Pocałuj moje wewnętrzne uda, centymetr po centymetrze, coraz wyżej.",
    "Pozwól mi zawiązać Ci oczy na kolejne dwie rundy.",
    "Zanurz palec w drinku, a potem pozwól mi go powoli ssać."
]

kary_l4 = [
    "Zaspokajaj mnie ustami przez pełne 60 sekund (stoper!).",
    "Rób z moim ciałem co tylko chcesz przez najbliższe 3 minuty.",
    "Zdejmij z siebie absolutnie wszystko. Resztę gry prowadzisz nago.",
    "Użyj na mnie wybranego gadżetu lub dłoni w sposób, który uwielbiam, przez 2 minuty.",
    "Zwiąż moje ręce (np. krawatem lub paskiem) na najbliższe dwie rundy.",
    "Zliż kroplę alkoholu z moich najbardziej wrażliwych miejsc.",
    "Wykonaj dla mnie 2-minutowy, namiętny taniec (striptease).",
    "Kary się skończyły. Resztę wieczoru spędzamy bez telefonów w sypialni. 😈"
]

# ==========================================
# 4. SILNIK GRY (LOGIKA)
# ==========================================
def generuj_gre():
    # Wybieramy losowe zestawy z każdego poziomu
    # Suma: 8 (L1) + 10 (L2) + 10 (L3) + 12 (L4) = 40 rund
    talia = random.sample(p1, 8) + random.sample(p2, 10) + \
            random.sample(p3, 10) + random.sample(p4, 12)
    
    finalna = []
    for i, q in enumerate(talia):
        # Toast co 8 rund
        if i > 0 and i % 8 == 0:
            finalna.append({"kto": "TOAST", "tekst": random.choice(toasty)})
        finalna.append(q)
    return finalna

def wylosuj_kare(idx, total):
    progres = idx / total
    if progres < 0.25: return random.choice(kary_l1)
    if progres < 0.50: return random.choice(kary_l2)
    if progres < 0.75: return random.choice(kary_l3)
    return random.choice(kary_l4)

@st.cache_resource
def get_global_state():
    return {"current_q": 0, "status": "question", "penalty": "", "gra": generuj_gre()}

state = get_global_state()

# ==========================================
# 5. WIDOKI
# ==========================================

if view_type == "selection":
    st.markdown("<div class='elegant-header'>System Wieczoru</div><br>", unsafe_allow_html=True)
    st.link_button("📺 AKTYWUJ EKRAN TV", "/?view=tv")
    st.markdown("<br>", unsafe_allow_html=True)
    st.link_button("📱 AKTYWUJ PILOTA", "/?view=pilot")

elif view_type == "tv":
    q_idx = state["current_q"]
    if q_idx < len(state["gra"]):
        q = state["gra"][q_idx]
        if state["status"] == "question":
            badge = "turn-toast" if q["kto"] == "TOAST" else ("turn-ona" if q["kto"] == "ONA" else "turn-on")
            info = "CZAS NA TOAST!" if q["kto"] == "TOAST" else f"CZYTA: {IMIE_ONA if q['kto'] == 'ONA' else IMIE_ON}"
            st.markdown(f"<div class='elegant-header'>Runda {q_idx + 1} z {len(state['gra'])}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='premium-box'><div class='turn-badge {badge}'>{info}</div><div class='gold-text'>{q['tekst']}</div></div>", unsafe_allow_html=True)
            time.sleep(1); st.rerun()
        else:
            txt = "PRAWDA" if state["penalty"] == "" else f"ZADANIE: {state['penalty']}"
            bg = "rgba(75,214,123,0.1)" if state["penalty"] == "" else "rgba(255,75,75,0.1)"
            st.markdown(f"<div class='premium-box' style='background:{bg};'><h1 class='gold-text'>{txt}</h1><p style='color: #8c7a96; font-size: 20px;'>Zasada Wykupnego: Shot i pomijasz karę! 🥃</p></div>", unsafe_allow_html=True)
            time.sleep(6); state["current_q"] += 1; state["status"] = "question"; st.rerun()
    else:
        st.markdown("<div class='premium-box'><h1 class='gold-text'>KONIEC GRY.<br>Czas na nagrodę główną... 😈</h1></div>", unsafe_allow_html=True)

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
    
    if st.button("WYLOSUJ NOWĄ GRĘ (RESET)"):
        state["gra"] = generuj_gre()
        state["current_q"] = 0
        state["status"] = "question"
        state["penalty"] = ""
        st.rerun()
