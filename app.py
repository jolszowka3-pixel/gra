import streamlit as st
import random
import time

# --- 1. Konfiguracja ---
IMIE_ONA = "Ona"   # <-- Wpisz jej imię!
IMIE_ON = "On"     # <-- Wpisz swoje imię!

st.set_page_config(page_title="Wieczór we Dwoje", layout="wide", page_icon="🥂")
query_params = st.query_params
view_type = query_params.get("view", "selection")

# --- 2. GŁÓWNY CSS (Pancerna stylizacja + nowe przyciski) ---
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
    }
    
    div.stButton > button p {
        font-size: 60px !important;
        font-weight: bold !important;
        letter-spacing: 5px !important;
    }

    /* Przycisk TAK (ciemna butelkowa zieleń) */
    button[kind="primary"] {
        background: linear-gradient(145deg, #1b3d28, #0e2416) !important;
        border: 2px solid #2e6343 !important;
    }
    button[kind="primary"] p {
        color: #4bd67b !important;
    }

    /* Przycisk NIE (ciemny, zgaszony burgund) */
    button[kind="secondary"] {
        background: linear-gradient(145deg, #451a1f, #260c0f) !important;
        border: 2px solid #73262f !important;
    }
    button[kind="secondary"] p {
        color: #ff4b4b !important;
    }

    /* Przycisk RESET (Ostatni przycisk na stronie) */
    div.stButton:last-of-type > button {
        height: 50px !important;
        background-color: transparent !important;
        border: 1px solid #2a2035 !important;
        box-shadow: none !important;
        margin-top: 10vh !important;
    }
    div.stButton:last-of-type > button p {
        font-size: 16px !important;
        font-weight: normal !important;
        color: #8c7a96 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. BAZA DANYCH (PYTANIA I KARY - GORĄCA EDYCJA)
# ==========================================

pytania = [
    # --- POZIOM 1: Intymność i flirt (Rozgrzewka) ---
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

    # --- POZIOM 2: Zmysły i pragnienia (Budowanie napięcia) ---
    {"kto": "ONA", "tekst": "Gdzie na ciele masz moje absolutnie ulubione miejsce do pieszczot?"},
    {"kto": "ON", "tekst": "Jakie jest moje ulubione tempo, gdy zaczynamy się całować – powolne i zmysłowe, czy drapieżne?"},
    {"kto": "ONA", "tekst": "Jaki rodzaj Twojego dotyku sprawia, że natychmiast przechodzą mnie dreszcze?"},
    {"kto": "ON", "tekst": "Gdybym miał Cię teraz pocałować w jedno miejsce – poza ustami – co bym wybrał?"},
    {"kto": "ONA", "tekst": "W jakiej mojej bieliźnie (lub bez niej) lubisz mnie najbardziej?"},
    {"kto": "ON", "tekst": "Jaki jest mój ulubiony sposób na to, by dać Ci znać, że mam na Ciebie ochotę?"},
    {"kto": "ONA", "tekst": "Jaki był mój najśmielszy sen z Twoim udziałem, o którym Ci opowiedziałam?"},
    {"kto": "ON", "tekst": "Który z naszych dotychczasowych pocałunków w miejscu publicznym najbardziej zapadł mi w pamięć?"},
    {"kto": "ONA", "tekst": "Jakie słowa wyszeptane przez Ciebie do mojego ucha kręcą mnie najbardziej?"},
    {"kto": "ON", "tekst": "Co najbardziej lubię z Tobą robić pod prysznicem lub w wannie?"},

    # --- POZIOM 3: Temperatura rośnie (Pikantne preferencje) ---
    {"kto": "ONA", "tekst": "Jaka jest moja ulubiona pozycja, gdy chcę mieć nad Tobą pełną kontrolę?"},
    {"kto": "ON", "tekst": "Jakie miejsce w naszym domu – poza sypialnią – najbardziej mnie kręci, by to zrobić?"},
    {"kto": "ONA", "tekst": "Co lubię najbardziej w Twojej twarzy lub oddechu, gdy oboje zbliżamy się do szczytu?"},
    {"kto": "ON", "tekst": "Gdybyś zgodziła się dzisiaj spełnić jedną moją fantazję, co poprosiłbym jako pierwsze?"},
    {"kto": "ONA", "tekst": "Jakie jest moje ulubione tempo w łóżku? Długie budowanie napięcia czy szybki, ostry seks?"},
    {"kto": "ON", "tekst": "Jaka jest najgorętsza rzecz, jaką kiedykolwiek mi zrobiłaś w łóżku?"},
    {"kto": "ONA", "tekst": "Czego chciałabym dzisiaj spróbować, co robimy rzadko lub wcale?"},
    {"kto": "ON", "tekst": "Jakie dźwięki, które wydajesz podczas seksu, doprowadzają mnie do szaleństwa?"},
    {"kto": "ONA", "tekst": "Gdybyś na 5 minut mógł zostać moim posłusznym niewolnikiem, o co bym Cię poprosiła?"},
    {"kto": "ON", "tekst": "Co myślę o porannym, 'leniwym' seksie w porównaniu do nocnych, dzikich maratonów?"},

    # --- POZIOM 4: Pełen ogień (Fantazje i granice) ---
    {"kto": "ONA", "tekst": "Gdybyśmy mieli nagrać domowe wideo, od jakiej sceny bym chciała zacząć?"},
    {"kto": "ON", "tekst": "Jakie jest jedno miejsce publiczne, w którym bardzo chciałbym, żebyśmy to zrobili (nawet jeśli to ryzykowne)?"},
    {"kto": "ONA", "tekst": "Czy bardziej kręci mnie, gdy to Ty jesteś dominujący, czy kiedy ja przejmuję inicjatywę?"},
    {"kto": "ON", "tekst": "Jaką część Twojego ciała chciałbym teraz powoli i dokładnie pieścić ustami?"},
    {"kto": "ONA", "tekst": "Jaka jest najostrzejsza i najbardziej 'brudna' fantazja, jaka kiedykolwiek przeszła mi przez myśl?"},
    {"kto": "ON", "tekst": "Gdybym mógł użyć na Tobie dzisiaj tylko jednego gadżetu, co bym wybrał?"},
    {"kto": "ONA", "tekst": "Jakie słowa chciałabym usłyszeć od Ciebie dokładnie w momencie, gdy dochodzę?"},
    {"kto": "ON", "tekst": "Gdybyśmy mieli dzisiaj dołączyć do nas kogoś trzeciego... czy zgodziłbym się, a jeśli tak, to w jakiej roli?"},
    {"kto": "ONA", "tekst": "Co sprawia, że po seksie czuję się absolutnie, stuprocentowo spełniona i wyczerpana?"},
    {"kto": "ON", "tekst": "Jak wyglądałby mój idealny, godzinny scenariusz gry wstępnej z Twoim udziałem?"}
]

# --- KARY: PODZIELONE NA 4 POZIOMY PIKANTERII ---

kary_poziom_1 = [ # Zmysłowy kontakt (Rozgrzewka)
    "Całuj szyję partnera przez pełną minutę, bardzo powoli schodząc w stronę obojczyków.",
    "Zdejmij jedną część garderoby z partnera, ale użyj do tego wyłącznie jednej dłoni.",
    "Splećcie dłonie, patrzcie sobie w oczy i zróbcie sobie nawzajem zmysłowy masaż dłoni przez 2 minuty.",
    "Pocałuj partnera w wybrane przez Niego miejsce na ciele, ale omijaj usta.",
    "Przejedź delikatnie opuszkiem palca po ustach, szyi i klatce piersiowej partnera. Musisz to robić przez 60 sekund.",
    "Wymasuj kark i ramiona partnera, przytulając się do jego pleców.",
    "Złap partnera za włosy (delikatnie!) i złóż na jego ustach głęboki, 10-sekundowy pocałunek.",
    "Wyznaj partnerowi, o czym pomyślałeś/aś, kiedy zobaczyłeś/aś go dzisiaj nago (lub w bieliźnie)."
]

kary_poziom_2 = [ # Temperatura rośnie
    "Zdejmij z siebie koszulkę lub bluzkę, patrząc partnerowi głęboko w oczy.",
    "Rozepnij powoli spodnie/spódnicę partnera, używając do tego tylko zębów i jednej ręki.",
    "Pocałuj wewnętrzną stronę ud partnera. Masz na to 60 sekund.",
    "Zawiąż partnerowi oczy. Masz 2 minuty, by całować i muskać oddechem jego/jej strefy erogenne.",
    "Usiądź na kolanach partnera okrakiem na czas trwania kolejnych dwóch pytań.",
    "Przejedź językiem wzdłuż kręgosłupa partnera, od karku aż po sam dół pleców.",
    "Wyszeptaj do ucha partnera najbardziej zbuntowaną/pikantną rzecz, jaką chcesz z nim dziś zrobić.",
    "Zdejmij z partnera kolejną część ubrania w najbardziej zmysłowy i powolny sposób, jaki potrafisz."
]

kary_poziom_3 = [ # Gorące napięcie
    "Weź kostkę lodu (lub użyj zimnych palców/ust) i powoli przesuwaj ją po brzuchu i wewnętrznej stronie ud partnera.",
    "Zdejmijcie z siebie to, co zostało, zostając jedynie w bieliźnie (lub całkiem nago, jeśli macie ochotę).",
    "Pieść szyję i uszy partnera swoimi wargami i językiem, podczas gdy jego/jej ręce są trzymane w górze przez Ciebie.",
    "Będziesz uległy/uległa przez najbliższe 3 minuty. Partner decyduje, jakiej pieszczoty mu udzielisz.",
    "Wymasuj pośladki partnera, używając do tego odrobiny olejku, balsamu lub własnej śliny.",
    "Pocałuj partnera namiętnie, jednocześnie przyciskając go całym swoim ciałem do łóżka/ściany na 60 sekund.",
    "Zamknij oczy. Partner będzie Cię teraz dotykał w wybrane przez siebie miejsca – masz głośno mówić, jak bardzo Ci się to podoba.",
    "Poprowadź dłonie partnera po swoim ciele, pokazując mu dokładnie to, jak i gdzie chcesz być teraz dotykany/a."
]

kary_poziom_4 = [ # Pełen ogień i preludium
    "Odłóżcie telefony na 5 minut. Rozpocznijcie grę wstępną z użyciem ust i rąk we wszystkich miejscach, na jakie macie ochotę.",
    "Zdejmijcie z siebie absolutnie wszystko. Resztę gry prowadzicie całkowicie nago.",
    "Pozwól partnerowi użyć na Tobie (lub wokół Ciebie) ulubionego gadżetu przez 2 minuty.",
    "Zaspokajaj partnera oralnie przez minutę, utrzymując z nim intensywny kontakt wzrokowy.",
    "Zacznijcie uprawiać seks na 3 minuty... po czym przerwijcie i musicie odpowiedzieć na kolejne pytanie.",
    "Pokaż partnerowi (dotykając siebie), jak chcesz, aby Cię dzisiaj pieścił.",
    "Zwiąż lub przytrzymaj ręce partnera i przez 3 minuty rób z jego/jej ciałem dosłownie to, na co masz ochotę.",
    "Kary się skończyły. Telewizor idzie w odstawkę, czas przenieść tę grę do sypialni. 😈"
]

def wylosuj_kare(numer_pytania):
    progres = numer_pytania / len(pytania)
    if progres < 0.25: return random.choice(kary_poziom_1)
    elif progres < 0.50: return random.choice(kary_poziom_2)
    elif progres < 0.75: return random.choice(kary_poziom_3)
    else: return random.choice(kary_poziom_4)

# ==========================================

# Inteligentna funkcja dozująca napięcie
def wylosuj_kare(numer_pytania):
    # Aplikacja sprawdza na jakim jesteście etapie w procentach
    progres = numer_pytania / len(pytania)
    
    if progres < 0.25:
        return random.choice(kary_poziom_1)
    elif progres < 0.50:
        return random.choice(kary_poziom_2)
    elif progres < 0.75:
        return random.choice(kary_poziom_3)
    else:
        return random.choice(kary_poziom_4)

# --- KONIEC SEKCJI 3 ---

# --- 4. Synchronizacja stanu ---
@st.cache_resource
def get_global_state():
    return {"current_q": 0, "status": "question", "penalty": ""}

state = get_global_state()

# --- WIDOK 1: WYBÓR ROLI ---
if view_type == "selection":
    st.markdown("<div class='elegant-header'>Wybierz Urządzenie</div><br>", unsafe_allow_html=True)
    st.link_button("📺 AKTYWUJ EKRAN TV", "/?view=tv", use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.link_button("📱 AKTYWUJ PILOTA", "/?view=pilot", use_container_width=True)

# --- WIDOK 2: TELEWIZOR (Mózg operacji) ---
elif view_type == "tv":
    q_idx = state["current_q"]
    
    if q_idx < len(pytania):
        obecne_pytanie = pytania[q_idx]
        kto_odpowiada = str(obecne_pytanie.get("kto", "")).upper().strip()
        badge_class, kolej_imie = ("turn-ona", IMIE_ONA) if kto_odpowiada == "ONA" else ("turn-on", IMIE_ON)

        if state["status"] == "question":
            st.markdown(f"<div class='elegant-header'>Runda {q_idx + 1}</div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class='premium-box'>
                <div class='turn-badge {badge_class}'>TERAZ ODPOWIADA: {kolej_imie}</div>
                <div class='gold-text'>{obecne_pytanie['tekst']}</div>
            </div>
            """, unsafe_allow_html=True)
            # TV nasłuchuje werdyktu
            time.sleep(1)
            st.rerun()
            
        elif state["status"] == "result":
            if state["penalty"] == "":
                st.markdown("<div class='premium-box' style='background: rgba(75, 214, 123, 0.1); border: 1px solid #1a4a30;'><h1 style='color: #4bd67b; font-size: 60px;'>PRAWDA</h1><p style='font-size: 24px; color: white;'>Zaliczone bez kary!</p></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='premium-box' style='background: rgba(255, 75, 75, 0.1); border: 1px solid #4a1a20;'><h1 style='color: #ff4b4b; font-size: 40px;'>CZAS NA ZADANIE:</h1><h1 style='color: white; font-size: 50px;'>{state['penalty']}</h1></div>", unsafe_allow_html=True)
            
            # Odliczanie kary i auto-przejście
            time.sleep(5)
            state["current_q"] += 1
            state["status"] = "question"
            st.rerun()
    else:
        st.markdown("<div class='premium-box'><div class='gold-text'>KONIEC GRY.<br>Czas na Was.</div></div>", unsafe_allow_html=True)
        time.sleep(5)
        st.rerun()

# --- WIDOK 3: PILOT ---
elif view_type == "pilot":
    
    # Przycisk TAK (primary)
    if st.button("TAK", use_container_width=True, type="primary"):
        if state["status"] == "question":
            state["status"] = "result"
            state["penalty"] = ""
    
    # Przycisk NIE (secondary)
    if st.button("NIE", use_container_width=True, type="secondary"):
        if state["status"] == "question":
            state["status"] = "result"
            state["penalty"] = wylosuj_kare(state["current_q"])

    # Przycisk RESETU
    if st.button("Zresetuj grę", use_container_width=True):
        state["current_q"] = 0
        state["status"] = "question"
