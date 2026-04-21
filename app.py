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
# 3. POTĘŻNA BAZA DANYCH
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
    {"kto": "ONA", "tekst": "Jaka jest pierwsza rzecz, o której myślisz, gdy rano budzisz się obok mnie?"},
    {"kto": "ON", "tekst": "Jaki drobny, codzienny gest z Twojej strony sprawia, że od razu mam ochotę Cię pocałować?"},
    {"kto": "ONA", "tekst": "W którym z moich codziennych ubrań wyglądam według Ciebie najbardziej pociągająco?"},
    {"kto": "ON", "tekst": "Jaka jest moja ulubiona część Twojego ciała, na którą najczęściej ukradkiem spoglądam?"},
    {"kto": "ONA", "tekst": "Jaki mój nawyk w sypialni (nawet podczas zasypiania) lubisz najbardziej?"},
    {"kto": "ON", "tekst": "Gdzie najbardziej lubię być całowany, gdy wracam zmęczony po całym dniu?"},
    {"kto": "ONA", "tekst": "Jaki rodzaj komplementów od Ciebie działa na mnie najszybciej?"},
    {"kto": "ON", "tekst": "Kiedy ostatnio pomyślałem sobie: 'Cholera, jaka ona jest seksowna'?"},
    {"kto": "ONA", "tekst": "Jaki jest mój ulubiony zapach Twoich perfum lub Twojego ciała?"},
    {"kto": "ON", "tekst": "W jakiej sytuacji czuję się przy Tobie najbardziej męski?"},
    {"kto": "ONA", "tekst": "Gdybym mogła spędzić z Tobą cały dzień w łóżku, co byśmy robili oprócz seksu?"},
    {"kto": "ON", "tekst": "Co we mnie sprawia, że czujesz się przy mnie bezpieczna i kochana?"},
    {"kto": "ONA", "tekst": "Które z naszych wspólnych zdjęć lubisz najbardziej i dlaczego?"},
    {"kto": "ON", "tekst": "Z jakim aktorem lub postacią najbardziej Ci się kojarzę?"},
    {"kto": "ONA", "tekst": "Jaka moja drobna wada wcale Ci nie przeszkadza, a wręcz Cię bawi?"}
]

# --- PYTANIA POZIOM 2 (Zmysły, ciało i pragnienia) ---
pytania_l2 = [
    {"kto": "ONA", "tekst": "Gdzie na ciele masz moje absolutnie ulubione miejsce do pieszczot?"},
    {"kto": "ON", "tekst": "Jakie jest moje ulubione tempo, gdy zaczynamy się całować – powolne i zmysłowe, czy drapieżne?"},
    {"kto": "ONA", "tekst": "Jaki rodzaj Twojego dotyku sprawia, że natychmiast przechodzą mnie dreszcze?"},
    {"kto": "ON", "tekst": "Gdybym miał Cię teraz pocałować w jedno miejsce – poza ustami – co bym wybrał?"},
    {"kto": "ONA", "tekst": "W jakiej mojej bieliźnie (lub bez niej) lubisz mnie najbardziej?"},
    {"kto": "ON", "tekst": "Jaki jest mój ulubiony sposób na to, by dać Ci znać, że mam na Ciebie ochotę?"},
    {"kto": "ONA", "tekst": "Jaki był mój najśmielszy sen z Twoim udziałem, o którym Ci opowiedziałam?"},
    {"kto": "ON", "tekst": "Który z naszych dotychczasowych pocałunków najbardziej zapadł mi w pamięć?"},
    {"kto": "ONA", "tekst": "Jakie słowa wyszeptane przez Ciebie do mojego ucha kręcą mnie najbardziej?"},
    {"kto": "ON", "tekst": "Co najbardziej lubię z Tobą robić pod prysznicem lub w wannie?"},
    {"kto": "ONA", "tekst": "Gdybyś miał opisać mój styl całowania w trzech słowach, jakie by to były słowa?"},
    {"kto": "ON", "tekst": "Kiedy ostatnio podczas jakiegoś wyjścia miałem ochotę zerwać z Ciebie ubranie?"},
    {"kto": "ONA", "tekst": "Jaka jest pierwsza rzecz, na którą zwracam uwagę, gdy stoisz przede mną nago?"},
    {"kto": "ON", "tekst": "Jaki kolor bielizny najbardziej mnie na Tobie kręci?"},
    {"kto": "ONA", "tekst": "Gdybyśmy mieli jutro zostać w domu, w co chciałbyś, żebym była ubrana?"}
]

# --- PYTANIA POZIOM 3 (Napięcie, sypialnia, fetysze) ---
pytania_l3 = [
    {"kto": "ONA", "tekst": "Jaka jest moja ulubiona pozycja, gdy chcę mieć nad Tobą pełną kontrolę?"},
    {"kto": "ON", "tekst": "Jakie miejsce w naszym domu – poza sypialnią – najbardziej mnie kręci, by to zrobić?"},
    {"kto": "ONA", "tekst": "Co lubię najbardziej w Twojej twarzy, gdy oboje zbliżamy się do szczytu?"},
    {"kto": "ON", "tekst": "Gdybyś zgodziła się dzisiaj spełnić jedną moją fantazję, co poprosiłbym jako pierwsze?"},
    {"kto": "ONA", "tekst": "Jakie jest moje ulubione tempo w łóżku? Długie budowanie napięcia czy szybki, ostry seks?"},
    {"kto": "ON", "tekst": "Jaka jest najgorętsza rzecz, jaką kiedykolwiek mi zrobiłaś w łóżku?"},
    {"kto": "ONA", "tekst": "Czego chciałabym dzisiaj spróbować, co robimy rzadko lub wcale?"},
    {"kto": "ON", "tekst": "Jakie dźwięki, które wydajesz podczas seksu, doprowadzają mnie do szaleństwa?"},
    {"kto": "ONA", "tekst": "Kto z nas w sypialni jest zazwyczaj głośniejszy?"},
    {"kto": "ON", "tekst": "Co lubię, kiedy robisz swoimi rękami podczas gdy my to robimy?"},
    {"kto": "ONA", "tekst": "Czy bardziej kręci mnie delikatne podduszanie/przytrzymywanie rąk, czy pełna czułość?"},
    {"kto": "ON", "tekst": "W jaki sposób najbardziej lubię być przez Ciebie obudzony?"},
    {"kto": "ONA", "tekst": "Co kręci mnie bardziej: robienie tego rano po przebudzeniu, czy w środku nocy?"},
    {"kto": "ON", "tekst": "Jak bardzo lubię, kiedy zostawiasz mi ślady na ciele (zadrapania, malinki)?"},
    {"kto": "ONA", "tekst": "Gdybym na 5 minut miała przejąć nad Tobą absolutną kontrolę, co kazałabym Ci zrobić?"}
]

# --- PYTANIA POZIOM 4 (Pełen ogień, ekstremalne) ---
pytania_l4 = [
    {"kto": "ONA", "tekst": "Gdybyśmy mieli nagrać domowe wideo, od jakiej sceny bym chciała zacząć?"},
    {"kto": "ON", "tekst": "Jakie jest jedno miejsce publiczne, w którym bardzo chciałbym to zrobić?"},
    {"kto": "ONA", "tekst": "Czy bardziej kręci mnie, gdy to Ty jesteś dominujący, czy kiedy ja przejmuję inicjatywę?"},
    {"kto": "ON", "tekst": "Gdybym mógł użyć na Tobie dzisiaj tylko jednego gadżetu, co bym wybrał?"},
    {"kto": "ONA", "tekst": "W jakiej pozycji najszybciej i najmocniej dochodzę?"},
    {"kto": "ON", "tekst": "Gdybyśmy dzisiaj wcielili się w role nieznajomych w barze, jaki tekst na podryw bym rzucił?"},
    {"kto": "ONA", "tekst": "Jaka jest najbardziej wyuzdana fantazja, z której kiedykolwiek Ci się zwierzyłam?"},
    {"kto": "ON", "tekst": "Którą część mojego ciała chciałbym, abyś teraz całowała i lizała najdłużej?"},
    {"kto": "ONA", "tekst": "[TWÓJ TEKST] Dodaj tutaj własne mega gorące pytanie!"},
    {"kto": "ON", "tekst": "[TWÓJ TEKST] Dodaj tutaj własne mega gorące pytanie!"},
    {"kto": "ONA", "tekst": "[TWÓJ TEKST] Dodaj tutaj własne mega gorące pytanie!"},
    {"kto": "ON", "tekst": "[TWÓJ TEKST] Dodaj tutaj własne mega gorące pytanie!"}
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
