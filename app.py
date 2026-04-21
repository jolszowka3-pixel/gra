import streamlit as st
import random
import time

# ==========================================
# 1. KONFIGURACJA I WASZE IMIONA
# ==========================================
IMIE_ONA = "Ona"   
IMIE_ON = "On"     
LICZBA_RUND = 40   # Optymalna długość jednej sesji

st.set_page_config(page_title="Wieczór we Dwoje", layout="wide", page_icon="🥂")
query_params = st.query_params
view_type = query_params.get("view", "selection")

# ==========================================
# 2. GŁÓWNY CSS (PREMIUM GOLD - ELEGANCKI)
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
# 3. GIGANTYCZNA BAZA DANYCH (160+ ELEMENTÓW)
# ==========================================

toasty = [
    "Wypijcie zdrowy łyk za Waszą namiętność! 🥂",
    "Toast za najseksowniejszą osobę w tym pokoju! 🔥",
    "Pijemy za wszystkie grzechy, które dzisiaj popełnicie! 😈",
    "Czas na toast bez użycia rąk! Podajcie sobie kieliszek do ust. 🍷",
    "Za Wasz pierwszy wspólny wyjazd i wszystkie kolejne! ✈️",
    "Pijemy za szczerość, która zaraz rozgrzeje ten pokój! 🥃",
    "Toast za to, że macie siebie na wyłączność. 🥂"
]

# --- PYTANIA: POZIOM 1 (Urocze, Romantyczne) ---
p1 = [
    {"kto": "ONA", "tekst": "Jaka była Twoja pierwsza myśl, kiedy mnie zobaczyłeś po raz pierwszy w życiu?"},
    {"kto": "ON", "tekst": "Co uważam za Twoją najbardziej atrakcyjną cechę charakteru?"},
    {"kto": "ONA", "tekst": "W jakim stroju (z moich codziennych ubrań) lubię Cię najbardziej?"},
    {"kto": "ON", "tekst": "Jaki drobny gest z Twojej strony sprawia mi zawsze największą radość?"},
    {"kto": "ONA", "tekst": "Który Twój nawyk uważam za najbardziej uroczy i zabawny?"},
    {"kto": "ON", "tekst": "Jaka jest moja ulubiona część Twojego ciała, gdy po prostu siedzimy obok siebie?"},
    {"kto": "ONA", "tekst": "Jakie jest moje ulubione wspomnienie z naszej pierwszej randki?"},
    {"kto": "ON", "tekst": "Co we mnie sprawia, że czujesz się przy mnie najbardziej bezpieczna?"},
    {"kto": "ONA", "tekst": "Gdybym mogła zabrać Cię teraz w dowolne miejsce na świecie, gdzie by to było?"},
    {"kto": "ON", "tekst": "Który komplement z Twoich ust zapadł mi najbardziej w pamięć?"},
    {"kto": "ONA", "tekst": "Jaki zapach moich perfum jest Twoim absolutnie ulubionym?"},
    {"kto": "ON", "tekst": "Jaką cechę mojego wyglądu zauważyłaś u mnie jako pierwszą?"},
    {"kto": "ONA", "tekst": "W jakiej sytuacji czuję się przy Tobie najbardziej kochana?"},
    {"kto": "ON", "tekst": "O czym najczęściej marzę, kiedy mamy leniwą, wspólną niedzielę?"},
    {"kto": "ONA", "tekst": "Który film lub piosenka najbardziej kojarzy mi się z naszymi początkami?"}
]

# --- PYTANIA: POZIOM 2 (Zmysłowe, Budowanie napięcia) ---
p2 = [
    {"kto": "ONA", "tekst": "Gdzie na moim ciele dotyk Twoich ust sprawia mi największą przyjemność?"},
    {"kto": "ON", "tekst": "Jaka pieszczota z Twojej strony najszybciej wywołuje u mnie dreszcze?"},
    {"kto": "ONA", "tekst": "Jakie słowa szeptane przez Ciebie do mojego ucha kręcą mnie najbardziej?"},
    {"kto": "ON", "tekst": "W jakiej swojej bieliźnie według mnie wyglądasz najbardziej pociągająco?"},
    {"kto": "ONA", "tekst": "Który z naszych dotychczasowych pocałunków w miejscu publicznym pamiętam najlepiej?"},
    {"kto": "ON", "tekst": "Co najbardziej lubię robić z Twoimi włosami, kiedy się do siebie zbliżamy?"},
    {"kto": "ONA", "tekst": "Gdybym miała wybrać jeden zapach, który kojarzy mi się z Tobą, co by to było?"},
    {"kto": "ON", "tekst": "Jaka jest moja ulubiona pora dnia na wspólne pieszczoty?"},
    {"kto": "ONA", "tekst": "Wolisz mnie w pełnym makijażu, czy rano, naturalną w Twojej za dużej koszulce?"},
    {"kto": "ON", "tekst": "Które miejsce na Twoim ciele uważam za najbardziej wrażliwe na mój dotyk?"},
    {"kto": "ONA", "tekst": "Jaka była najbardziej szalona rzecz, jaką zrobiliśmy razem w ciągu ostatniego roku?"},
    {"kto": "ON", "tekst": "Co myślę o Twoim stylu całowania w skali od 1 do 10?"},
    {"kto": "ONA", "tekst": "Jakie ubranie z mojej szafy chętnie byś ze mnie teraz zdjął?"},
    {"kto": "ON", "tekst": "Co we mnie budzi w Tobie największy pożądanie, gdy na mnie patrzysz?"}
]

# --- PYTANIA: POZIOM 3 (Pikantne, Sypialnia) ---
p3 = [
    {"kto": "ONA", "tekst": "Jaka jest moja ulubiona pozycja, w której czuję się najbardziej spełniona?"},
    {"kto": "ON", "tekst": "Jakie nietypowe miejsce poza sypialnią najbardziej mnie kręci na 'szybki numerek'?"},
    {"kto": "ONA", "tekst": "Co lubię najbardziej w Twoim zachowaniu w łóżku, gdy zbliżamy się do szczytu?"},
    {"kto": "ON", "tekst": "Jaki rodzaj dotyku rąk w sypialni Ona preferuje: delikatny czy zdecydowany?"},
    {"kto": "ONA", "tekst": "Jaka jest moja najbardziej skryta fantazja, o której kiedykolwiek Ci wspomniałam?"},
    {"kto": "ON", "tekst": "Co Ona sądzi o używaniu gadżetów – który z nich byłby Jej ulubionym?"},
    {"kto": "ONA", "tekst": "Jaki dźwięk wydawany przeze mnie w sypialni działa na Ciebie najbardziej?"},
    {"kto": "ON", "tekst": "Kto z nas według Niej zazwyczaj przejmuje inicjatywę w łóżku?"},
    {"kto": "ONA", "tekst": "Czego chciałabym spróbować w sypialni, co robimy bardzo rzadko lub wcale?"},
    {"kto": "ON", "tekst": "Jakie słowa wypowiadane podczas seksu kręcą Ją najbardziej?"},
    {"kto": "ONA", "tekst": "Wolisz, kiedy w sypialni dominuję, czy kiedy jestem całkowicie uległa?"},
    {"kto": "ON", "tekst": "Co sprawia, że po seksie Ona czuje się w 100% usatysfakcjonowana?"}
]

# --- PYTANIA: POZIOM 4 (Ekstremalne, Finał) ---
p4 = [
    {"kto": "ONA", "tekst": "Gdybyśmy mieli nagrać wspólne wideo, od jakiej sceny chciałabym zacząć?"},
    {"kto": "ON", "tekst": "W jakiej pozycji Ona dochodzi najszybciej i najbardziej intensywnie?"},
    {"kto": "ONA", "tekst": "Gdybym mogła Cię uwiązać i robić z Tobą co zechcę przez 5 minut, co byłoby pierwsze?"},
    {"kto": "ON", "tekst": "Co w Twoim zachowaniu sprawia, że Ona całkowicie traci nad sobą panowanie?"},
    {"kto": "ONA", "tekst": "Którą część Twojego ciała chciałabym teraz pieścić ustami najdłużej?"},
    {"kto": "ON", "tekst": "Jaka jest Jej najostrzejsza i najbardziej wyuzdana fantazja, jaka kiedykolwiek przeszła Jej przez myśl?"},
    {"kto": "ONA", "tekst": "Gdybyśmy mieli dzisiaj dołączyć kogoś trzeciego... czy Ona w ogóle by to rozważyła?"},
    {"kto": "ON", "tekst": "Jakie miejsce publiczne kręci Ją najbardziej jako potencjalna scena seksu?"},
    {"kto": "ONA", "tekst": "Co jest dla mnie ważniejsze: technika i tempo czy emocjonalne połączenie podczas seksu?"},
    {"kto": "ON", "tekst": "Który z moich fetyszy Ona akceptuje najbardziej, a który Ją zaskoczył?"}
]

# --- KARY: POZIOM 1 (Delikatne) ---
kary_l1 = [
    "Całuj moją szyję przez pełną minutę, omijając usta.",
    "Zrób mi 2-minutowy masaż dłoni i palców.",
    "Powiedz mi szeptem 3 rzeczy, które najbardziej we mnie cenisz.",
    "Zdejmij ze mnie skarpetki, używając tylko jednej dłoni.",
    "Patrz mi głęboko w oczy przez 60 sekund, nie odrywając wzroku.",
    "Przejedź delikatnie nosem po moich policzkach i szyi.",
    "Przytul mnie tak mocno, jak potrafisz, przez pełną minutę.",
    "Napisz palcem na moich plecach zdanie, a ja muszę zgadnąć co to."
]

# --- KARY: POZIOM 2 (Zmysłowe) ---
kary_l2 = [
    "Weź łyk alkoholu i przekaż mi go ustami podczas pocałunku.",
    "Zdejmij z partnera jedną, wybraną przez Ciebie część garderoby.",
    "Pocałuj moje wewnętrzne udo, centymetr po centymetrze, coraz wyżej.",
    "Przygryź delikatnie płatek mojego ucha i powiedz coś niegrzecznego.",
    "Zdejmij ze mnie jeden element ubrania (biżuteria, zegarek, pasek) samymi zębami.",
    "Usiądź na moich kolanach okrakiem i spędź tak całą kolejną rundę.",
    "Wymasuj moje stopy, używając do tego odrobiny balsamu lub drinka.",
    "Pozwól mi zawiązać Ci oczy na najbliższą rundę."
]

# --- KARY: POZIOM 3 (Pikantne) ---
kary_l3 = [
    "Zliż odrobinę alkoholu z mojego brzucha lub obojczyka.",
    "Zostań tylko w bieliźnie na resztę tej fazy gry.",
    "Wymasuj moje pośladki dłońmi, patrząc mi głęboko w oczy przez minutę.",
    "Pieść moje ucho i szyję językiem, podczas gdy moje ręce są trzymane przez Ciebie.",
    "Przejedź językiem od mojego pępka aż do wgłębienia między piersiami.",
    "Zdejmij moją koszulkę lub bluzkę, używając tylko zębów.",
    "Przejedź kostką lodu wzdłuż mojego kręgosłupa, a potem zliż wodę.",
    "Będziesz uległy/uległa przez najbliższe 3 minuty. Robię z Twoim ciałem co chcę."
]

# --- KARY: POZIOM 4 (Erotyczne) ---
kary_l4 = [
    "Zaspokajaj mnie ustami przez pełne 60 sekund (użyj stopera!).",
    "Rób z moim ciałem co tylko chcesz przez najbliższe 3 minuty.",
    "Zdejmij z siebie absolutnie wszystko. Resztę gry prowadzisz nago.",
    "Użyj na partnerze wybranego gadżetu lub dłoni w sposób ekstremalny przez 2 minuty.",
    "Zwiąż moje ręce (np. krawatem lub paskiem) na najbliższe dwie rundy.",
    "Wykonaj dla mnie namiętny, 2-minutowy taniec (striptease).",
    "Zliż kroplę alkoholu z moich najbardziej wrażliwych miejsc.",
    "Kary się skończyły. Resztę wieczoru spędzamy bez telefonów w sypialni. 😈"
]


# ==========================================
# 4. SILNIK GENERUJĄCY GRĘ
# ==========================================
def generuj_gre():
    # Wybieramy losowe zestawy z każdego poziomu
    q1 = random.sample(p1, min(len(p1), 10))
    q2 = random.sample(p2, min(len(p2), 10))
    q3 = random.sample(p3, min(len(p3), 10))
    q4 = random.sample(p4, min(len(p4), 10))
    
    talia_bazowa = q1 + q2 + q3 + q4
    
    # Dodajemy toasty co 8 rund
    finalna = []
    for i, q in enumerate(talia_bazowa):
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

# --- Synchronizacja stanu (Globalna) ---
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

            st.markdown(f"<div class='elegant-header'>Runda {q_idx + 1} z {len(state['gra'])}</div>", unsafe_allow_html=True)
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
                <p style='color: #8c7a96; font-size: 20px; margin-top: 20px;'>Zasada Wykupnego: Shot alkoholu i pomijasz karę! 🥃</p>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(6); state["current_q"] += 1; state["status"] = "question"; st.rerun()
    else:
        st.markdown("<div class='premium-box'><h1 class='gold-text'>KONIEC GRY.<br>Czas przenieść się do sypialni... 😈</h1></div>", unsafe_allow_html=True)

elif view_type == "pilot":
    q_idx = state["current_q"]
    if q_idx < len(state["gra"]):
        q = state["gra"][q_idx]
        who_val = str(q["kto"]).upper().strip()
        
        if who_val == "TOAST":
            if st.button("WYPITE! 🥂 (Dalej)", use_container_width=True):
                state["status"] = "result"; state["penalty"] = ""; st.rerun()
        else:
            # Pilot precyzyjnie wskazuje sędziego
            sedzia = IMIE_ONA if who_val == "ONA" else IMIE_ON
            st.markdown(f"<p style='text-align:center; color:#d4af37; font-size:20px; letter-spacing:2px;'>Sędziuje: <b>{sedzia}</b></p>", unsafe_allow_html=True)
            
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
