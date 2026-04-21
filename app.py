import streamlit as st
import random
import time

# --- 1. Konfiguracja ---
IMIE_ONA = "Ona"   # <-- Wpisz jej imię!
IMIE_ON = "On"     # <-- Wpisz swoje imię!
LICZBA_RUND = 40   # Ile łącznie pytań ma mieć jedna pełna gra (domyślnie 40)

st.set_page_config(page_title="Wieczór we Dwoje", layout="wide", page_icon="🥂")
query_params = st.query_params
view_type = query_params.get("view", "selection")

# --- 2. GŁÓWNY CSS (Pancerna stylizacja + złote przyciski) ---
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
    .turn-toast { background-color: rgba(255, 75, 75, 0.1); border: 1px solid #ff4b4b; color: #ff4b4b; }

    /* --- Luksusowe przyciski w menu startowym --- */
    div[data-testid="stLinkButton"] > a {
        background: linear-gradient(145deg, #1a1323, #0d0a13) !important;
        border: 1px solid #d4af37 !important;
        color: #d4af37 !important;
        border-radius: 20px !important;
        text-decoration: none !important;
        font-size: 24px !important;
        font-weight: 300 !important;
        letter-spacing: 4px !important;
        padding: 25px !important;
        text-align: center !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        box-shadow: 0 15px 30px rgba(0,0,0,0.6) !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="stLinkButton"] > a:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 20px 40px rgba(212, 175, 55, 0.2) !important;
        background: linear-gradient(145deg, #261b33, #15101c) !important;
    }

    /* --- PANCERNA STYLIZACJA PRZYCISKÓW PILOTA --- */
    div.stButton > button {
        height: 30vh !important;
        width: 100% !important;
        border-radius: 30px !important;
        margin-top: 2vh;
        box-shadow: 0 15px 30px rgba(0,0,0,0.8) !important;
        transition: all 0.2s ease !important;
    }
    
    div.stButton > button p {
        font-size: 60px !important;
        font-weight: bold !important;
        letter-spacing: 5px !important;
    }

    button[kind="primary"], button[kind="secondary"] {
        background: linear-gradient(145deg, #1a1323, #0d0a13) !important;
        border: 2px solid #d4af37 !important;
    }
    button[kind="primary"] p, button[kind="secondary"] p {
        color: #d4af37 !important;
        text-shadow: 0 4px 15px rgba(212, 175, 55, 0.3) !important;
    }
    
    button[kind="primary"]:active, button[kind="secondary"]:active {
        background: linear-gradient(145deg, #261b33, #15101c) !important;
        box-shadow: 0 10px 30px rgba(212, 175, 55, 0.4) !important;
        transform: scale(0.98) !important;
    }

    /* Przycisk RESET */
    div.stButton:last-of-type > button {
        height: 50px !important;
        background-color: transparent !important;
        border: 1px solid #2a2035 !important;
        box-shadow: none !important;
        margin-top: 10vh !important;
        transform: none !important;
    }
    div.stButton:last-of-type > button p {
        font-size: 16px !important;
        font-weight: normal !important;
        color: #8c7a96 !important;
        text-shadow: none !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. POTĘŻNA BAZA DANYCH (TEST ZGODNOŚCI)
# ==========================================

# --- TOASTY ---
toasty = [
    "Wypijcie zdrowy łyk za Waszą pierwszą randkę! Niech ten wieczór będzie jeszcze lepszy. 🥂",
    "Oboje pijecie potężnego łyka za to, jak dzisiaj rewelacyjnie wyglądacie! 🔥",
    "Czas na toast bez użycia rąk! Podajcie sobie nawzajem kieliszek do ust. 🍷",
    "Pijemy za wszystkie grzechy, które dzisiaj popełnicie! 😈",
    "Pocałujcie się z alkoholem w ustach, dzieląc się nim jak podczas pocałunku. 💋",
    "Wypijcie za najgorętszy moment, który dopiero nadejdzie... 🍾"
]

# --- PYTANIA POZIOM 1 (Intymność, flirt, uśmiech) ---
pytania_l1 = [
    {"kto": "ONA", "tekst": "Jaka jest pierwsza rzecz, na którą On zwrócił uwagę, gdy się poznaliście?"},
    {"kto": "ON", "tekst": "Co Ona uważa za Twoją najbardziej atrakcyjną cechę charakteru?"},
    {"kto": "ONA", "tekst": "W jakim Twoim ubraniu (z tych codziennych) On lubi Cię najbardziej?"},
    {"kto": "ON", "tekst": "Jaka jest Jej ulubiona część Twojego ciała?"},
    {"kto": "ONA", "tekst": "Który Twój nawyk On uważa za najbardziej uroczy?"},
    {"kto": "ON", "tekst": "O czym Ona najczęściej myśli tuż przed zaśnięciem?"},
    {"kto": "ONA", "tekst": "Jakie jest Jego ulubione wspomnienie z Waszej pierwszej randki?"},
    {"kto": "ON", "tekst": "Jaki Twój drobny gest sprawia Jej zawsze największą radość?"},
    {"kto": "ONA", "tekst": "Jaki jest Jego ulubiony zapach Twoich perfum?"},
    {"kto": "ON", "tekst": "Jaka piosenka lub jaki film najbardziej kojarzy Jej się z Wami?"}
]

# --- PYTANIA POZIOM 2 (Zmysły, ciało i pragnienia) ---
pytania_l2 = [
    {"kto": "ONA", "tekst": "Gdzie On najbardziej lubi być całowany, gdy jest zmęczony po całym dniu?"},
    {"kto": "ON", "tekst": "Jaki rodzaj Twojego dotyku od razu wywołuje u Niej dreszcze?"},
    {"kto": "ONA", "tekst": "Jakie jest Jego ulubione tempo, gdy zaczynacie się całować (powoli czy drapieżnie)?"},
    {"kto": "ON", "tekst": "W jakiej swojej bieliźnie Ona czuje się najbardziej pociągająca?"},
    {"kto": "ONA", "tekst": "Który z Waszych pocałunków w miejscu publicznym On pamięta najlepiej?"},
    {"kto": "ON", "tekst": "Jakie słowa szeptane przez Ciebie do ucha kręcą Ją najbardziej?"},
    {"kto": "ONA", "tekst": "Co On najbardziej lubiłby z Tobą robić podczas wspólnego prysznica?"},
    {"kto": "ON", "tekst": "Jaki jest Jej ulubiony sposób na dyskretne pokazanie Ci, że ma na Ciebie ochotę?"},
    {"kto": "ONA", "tekst": "Gdyby On miał Cię teraz pocałować w jedno miejsce poza ustami, co by wybrał?"},
    {"kto": "ON", "tekst": "Które miejsce na Jej ciele uważa za najwrażliwsze na pieszczoty?"}
]

# --- PYTANIA POZIOM 3 (Napięcie, sypialnia, fetysze) ---
pytania_l3 = [
    {"kto": "ONA", "tekst": "Jaka jest Jego ulubiona pozycja w sypialni, gdy chce mieć nad Tobą pełną kontrolę?"},
    {"kto": "ON", "tekst": "Jakie tempo w łóżku Ona woli: długie budowanie napięcia czy szybki, ostry seks?"},
    {"kto": "ONA", "tekst": "Jakie nietypowe miejsce w Waszym domu najbardziej kręci Go na 'szybki numerek'?"},
    {"kto": "ON", "tekst": "Co najbardziej kręci Ją w wyrazie Twojej twarzy, gdy zbliżacie się do szczytu?"},
    {"kto": "ONA", "tekst": "Jaka jest Jego najbardziej skryta fantazja, o której Ci kiedykolwiek wspomniał?"},
    {"kto": "ON", "tekst": "Jaka jest najgorętsza rzecz, jaką Ona uważa, że Jej kiedykolwiek zrobiłeś?"},
    {"kto": "ONA", "tekst": "Czego On chciałby spróbować w sypialni z Tobą, a co robicie bardzo rzadko?"},
    {"kto": "ON", "tekst": "Jakie dźwięki wydawane przez Ciebie doprowadzają Ją w sypialni do szaleństwa?"},
    {"kto": "ONA", "tekst": "Co kręci Go bardziej: poranny 'leniwy' seks, czy nocne, dzikie maratony?"},
    {"kto": "ON", "tekst": "Kto z Waszej dwójki uważa, że jest głośniejszy w łóżku, patrząc z Jej perspektywy?"}
]

# --- PYTANIA POZIOM 4 (Pełen ogień, ekstremalne) ---
pytania_l4 = [
    {"kto": "ONA", "tekst": "Gdybyście mieli nagrać domowe wideo, od jakiej sceny On chciałby zacząć?"},
    {"kto": "ON", "tekst": "W jakiej pozycji Ona dochodzi najszybciej i najintensywniej?"},
    {"kto": "ONA", "tekst": "Czy On woli, gdy jesteś uległa, czy gdy to Ty przejmujesz inicjatywę i dominujesz?"},
    {"kto": "ON", "tekst": "Jakiego gadżetu Ona użyłaby w sypialni najchętniej podczas dzisiejszej nocy?"},
    {"kto": "ONA", "tekst": "Jakie miejsce publiczne kręci Go najbardziej, mimo że jest to bardzo ryzykowne?"},
    {"kto": "ON", "tekst": "Jaka jest najostrzejsza i najbardziej wyuzdana fantazja, jaka przeszła Jej kiedykolwiek przez myśl?"},
    {"kto": "ONA", "tekst": "Którą część Twojego ciała On chciałby, abyś dzisiaj pieściła ustami najdłużej?"},
    {"kto": "ON", "tekst": "Co sprawia, że po seksie Ona czuje się absolutnie, w 100% zaspokojona?"},
    {"kto": "ONA", "tekst": "[TWÓJ TEKST] Dodaj tu swoje pytanie o Go!"},
    {"kto": "ON", "tekst": "[TWÓJ TEKST] Dodaj tu swoje pytanie o Nią!"}
]

# --- KARY L1 ---
kary_poziom_1 = [ 
    "Całuj szyję partnera przez pełną minutę, bardzo powoli schodząc w stronę obojczyków.",
    "Zdejmij jedną część garderoby z partnera, ale użyj do tego wyłącznie jednej dłoni.",
    "Splećcie dłonie, patrzcie sobie w oczy i zróbcie sobie nawzajem zmysłowy masaż dłoni przez 2 minuty.",
    "Pocałuj partnera w wybrane przez Niego miejsce na ciele, ale omijaj usta.",
    "Przejedź delikatnie opuszkiem palca po ustach, szyi i klatce piersiowej partnera. Musisz to robić przez 60 sekund.",
    "Delikatnie pociągnij partnera za włosy i złóż na ustach powolny pocałunek.",
    "Połóż głowę na kolanach partnera, podczas gdy on/ona będzie gładzić Cię po włosach przez minutę.",
    "Powiedz partnerowi o czymś, co robi w łóżku, a co doprowadza Cię do szaleństwa."
]

# --- KARY L2 ---
kary_poziom_2 = [ 
    "Weź łyka swojego drinka/wina i przekaż mi go prosto do moich ust (bez użycia rąk).",
    "Zdejmij z siebie koszulkę lub bluzkę, patrząc partnerowi głęboko w oczy.",
    "Rozepnij powoli spodnie/spódnicę partnera, używając do tego tylko zębów i jednej ręki.",
    "Pocałuj wewnętrzną stronę ud partnera. Masz na to 60 sekund.",
    "Wypijmy 'bruderszafta' ze splecionymi ramionami, po czym pocałuj mnie powoli w szyję.",
    "Przejedź językiem wzdłuż kręgosłupa partnera, od karku aż po sam dół pleców.",
    "Usiądź na kolanach partnera okrakiem i spędźcie tak resztę rundy.",
    "Rozepnij swój biustonosz / koszulę, ale jeszcze ich nie zdejmuj."
]

# --- KARY L3 ---
kary_poziom_3 = [ 
    "Zanurz palec w swoim alkoholu i pozwól partnerowi go ssać przez 15 sekund.",
    "Przejedź chłodnym kieliszkiem/szklanką powoli po dekolcie lub brzuchu partnera, a potem zliż krople.",
    "Zdejmijcie z siebie to, co zostało, zostając jedynie w bieliźnie (lub całkowicie nago).",
    "Będziesz uległy/uległa przez najbliższe 3 minuty. Partner decyduje, jakiej pieszczoty mu udzielisz.",
    "Pocałuj partnera namiętnie, jednocześnie przyciskając go całym swoim ciałem do łóżka/ściany na 60 sekund.",
    "Zamknij oczy. Partner będzie Cię teraz dotykał w wybrane przez siebie miejsca – musisz głośno mówić, jak bardzo Ci się to podoba.",
    "Poprowadź dłonie partnera po swoim ciele, pokazując mu dokładnie to, jak i gdzie chcesz być teraz dotykany/a.",
    "Zliż powoli odrobinę alkoholu z szyi lub obojczyka partnera."
]

# --- KARY L4 ---
kary_poziom_4 = [ 
    "Odłóżcie telefony na 5 minut. Rozpocznijcie grę wstępną z użyciem ust i rąk we wszystkich miejscach.",
    "Zdejmijcie z siebie absolutnie wszystko. Resztę gry prowadzicie całkowicie nago.",
    "Pozwól partnerowi użyć na Tobie (lub wokół Ciebie) ulubionego gadżetu przez 2 minuty.",
    "Zwiąż lub przytrzymaj ręce partnera i przez 2 minuty rób z jego/jej ciałem dosłownie to, na co masz ochotę.",
    "Zaspokajaj partnera oralnie przez minutę, utrzymując z nim intensywny kontakt wzrokowy.",
    "[DODAJ SWOJĄ WŁASNĄ BARDZO PIKANTNĄ KARĘ]",
    "[DODAJ SWOJĄ WŁASNĄ BARDZO PIKANTNĄ KARĘ]",
    "Kary się skończyły. Czas przenieść tę grę do sypialni. 😈"
]


# ==========================================
# 4. SILNIK GENERUJĄCY GRĘ (LOSOWANIE)
# ==========================================
def generuj_gre():
    # Pobieramy losowe próbki z każdego poziomu, żeby się nie powtarzały
    q1 = random.sample(pytania_l1, min(10, len(pytania_l1)))
    q2 = random.sample(pytania_l2, min(10, len(pytania_l2)))
    q3 = random.sample(pytania_l3, min(10, len(pytania_l3)))
    q4 = random.sample(pytania_l4, min(10, len(pytania_l4)))
    
    pelna_lista = q1 + q2 + q3 + q4
    
    # Dodajemy losowe Toasty (np. co 8 pytań)
    kolejka_z_toastami = []
    for i, pytanie in enumerate(pelna_lista):
        if i > 0 and i % 8 == 0:
            kolejka_z_toastami.append({"kto": "TOAST", "tekst": random.choice(toasty)})
        kolejka_z_toastami.append(pytanie)
        
    return kolejka_z_toastami

def wylosuj_kare(numer_pytania, max_pytan):
    progres = numer_pytania / max_pytan
    if progres < 0.25: return random.choice(kary_poziom_1)
    elif progres < 0.50: return random.choice(kary_poziom_2)
    elif progres < 0.75: return random.choice(kary_poziom_3)
    else: return random.choice(kary_poziom_4)

# --- Synchronizacja stanu ---
@st.cache_resource
def get_global_state():
    return {
        "current_q": 0, 
        "status": "question", 
        "penalty": "",
        "kolejka_pytan": generuj_gre() # Od razu losuje układ gry!
    }

state = get_global_state()
aktualna_gra = state["kolejka_pytan"]


# ==========================================
# 5. WIDOK 1: WYBÓR ROLI
# ==========================================
if view_type == "selection":
    st.markdown("<div class='elegant-header'>Wybierz Urządzenie</div><br>", unsafe_allow_html=True)
    st.link_button("📺 AKTYWUJ EKRAN TV", "/?view=tv", use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.link_button("📱 AKTYWUJ PILOTA", "/?view=pilot", use_container_width=True)


# ==========================================
# 6. WIDOK 2: TELEWIZOR (Mózg operacji)
# ==========================================
elif view_type == "tv":
    q_idx = state["current_q"]
    
    if q_idx < len(aktualna_gra):
        obecne_pytanie = aktualna_gra[q_idx]
        kto_odpowiada = str(obecne_pytanie.get("kto", "")).upper().strip()
        
        is_toast = (kto_odpowiada == "TOAST")
        
        if is_toast:
            badge_class, kolej_imie = ("turn-toast", "CZAS NA TOAST!")
        else:
            badge_class, kolej_imie = ("turn-ona", IMIE_ONA) if kto_odpowiada == "ONA" else ("turn-on", IMIE_ON)

        if state["status"] == "question":
            if is_toast:
                st.markdown("<div class='elegant-header'>Przerwa Specjalna</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='elegant-header'>Runda {q_idx + 1} z {len(aktualna_gra)}</div>", unsafe_allow_html=True)
                
            st.markdown(f"""
            <div class='premium-box'>
                <div class='turn-badge {badge_class}'>{kolej_imie}</div>
                <div class='gold-text'>{obecne_pytanie['tekst']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            time.sleep(1)
            st.rerun()
            
        elif state["status"] == "result":
            if state["penalty"] == "":
                st.markdown("<div class='premium-box' style='background: rgba(75, 214, 123, 0.1); border: 1px solid #1a4a30;'><h1 style='color: #4bd67b; font-size: 60px;'>PRAWDA</h1><p style='font-size: 24px; color: white;'>Zaliczone bez kary!</p></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='premium-box' style='background: rgba(255, 75, 75, 0.1); border: 1px solid #4a1a20;'><h1 style='color: #ff4b4b; font-size: 40px;'>CZAS NA ZADANIE:</h1><h1 style='color: white; font-size: 50px;'>{state['penalty']}</h1></div>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: center; color: #8c7a96; font-size: 20px; margin-top: 20px;'>Złota Zasada: Nie masz odwagi? Wypijasz solidnego shota/łyka alkoholu i tracisz kolejkę! 🥃</p>", unsafe_allow_html=True)
            
            time.sleep(6)
            state["current_q"] += 1
            state["status"] = "question"
            st.rerun()
    else:
        st.markdown("<div class='premium-box'><div class='gold-text'>KONIEC GRY.<br>Czas na Was. 😈</div></div>", unsafe_allow_html=True)
        time.sleep(5)
        st.rerun()


# ==========================================
# 7. WIDOK 3: PILOT
# ==========================================
elif view_type == "pilot":
    q_idx = state["current_q"]
    
    if q_idx < len(aktualna_gra):
        obecne_pytanie = aktualna_gra[q_idx]
        is_toast = (str(obecne_pytanie.get("kto", "")).upper().strip() == "TOAST")
        
        if is_toast:
            if st.button("WYPITE! 🥂 (Dalej)", use_container_width=True, type="primary"):
                if state["status"] == "question":
                    state["status"] = "result"
                    state["penalty"] = ""
        else:
            if st.button("TAK", use_container_width=True, type="primary"):
                if state["status"] == "question":
                    state["status"] = "result"
                    state["penalty"] = ""
            
            if st.button("NIE", use_container_width=True, type="secondary"):
                if state["status"] == "question":
                    state["status"] = "result"
                    state["penalty"] = wylosuj_kare(state["current_q"], len(aktualna_gra))

    if st.button("Zresetuj i losuj nową grę", use_container_width=True):
        state["kolejka_pytan"] = generuj_gre() # Silnik tworzy całkowicie nową rozgrywkę!
        state["current_q"] = 0
        state["status"] = "question"
