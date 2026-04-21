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

# --- 3. Baza Danych (Inteligentna struktura na 200+ elementów) ---

# PYTANIA
# Poziom 1 i 2 (Romantyczne, budujące napięcie i wiedza o sobie)
pytania = [
    {"kto": "ONA", "tekst": "Jakie jest moje ulubione wspomnienie z naszej pierwszej randki?"},
    {"kto": "ON", "tekst": "Co najbardziej urzekło mnie w Tobie, gdy się poznaliśmy?"},
    {"kto": "ONA", "tekst": "Który z moich ciuchów lubisz na mnie najbardziej?"},
    {"kto": "ON", "tekst": "Gdzie najchętniej zabrałbym Cię na romantyczny weekend bez telefonów?"},
    {"kto": "ONA", "tekst": "Jaki mój nawyk uważasz za najbardziej uroczy?"},
    {"kto": "ON", "tekst": "Jaki drobny gest z Twojej strony sprawia, że od razu mam lepszy dzień?"},
    {"kto": "ONA", "tekst": "Która część Twojego ciała podoba mi się najbardziej?"},
    {"kto": "ON", "tekst": "Jakie jest moje ulubione jedzenie, gdy mam gorszy dzień?"},
    {"kto": "ONA", "tekst": "Jaka jest pierwsza rzecz, na którą zwracam uwagę u innych ludzi?"},
    {"kto": "ON", "tekst": "Wymień jedną rzecz, której w sobie nie lubię, a Ty ją we mnie uwielbiasz."},
    {"kto": "ONA", "tekst": "Jaki rodzaj dotyku najbardziej mnie relaksuje?"},
    {"kto": "ON", "tekst": "Co najbardziej lubię robić z Tobą w leniwy niedzielny poranek?"},
    {"kto": "ONA", "tekst": "Gdybym mogła zmienić w naszym mieszkaniu jedną rzecz, co by to było?"},
    {"kto": "ON", "tekst": "Jaki komplement od Ciebie zapadł mi najbardziej w pamięć?"},
    {"kto": "ONA", "tekst": "W jakiej sytuacji czuję się przy Tobie najbardziej bezpieczna?"},
    {"kto": "ON", "tekst": "Kiedy ostatnio poczułem, że jestem absolutnym szczęściarzem, mając Cię obok?"},
    # Możesz kontynuować dodawanie pytań z tego poziomu...
]

# Poziom 3 i 4 (Pikantne i gorące - DOPISZCIE SWOJE!)
pytania_pikantne = [
    {"kto": "ONA", "tekst": "[TUTAJ WPISZ SWOJE PIKANTNE PYTANIE]"},
    {"kto": "ON", "tekst": "[TUTAJ WPISZ SWOJE PIKANTNE PYTANIE]"},
    {"kto": "ONA", "tekst": "[TUTAJ WPISZ SWOJE PIKANTNE PYTANIE]"},
    {"kto": "ON", "tekst": "[TUTAJ WPISZ SWOJE PIKANTNE PYTANIE]"}
    # Dodajcie ich tyle, by łącznie z poprzednimi było ich około 200
]

# Połączenie wszystkich pytań w jedną wielką listę
pytania.extend(pytania_pikantne)


# KARY (ZADANIA) PODZIELONE NA 4 POZIOMY
kary_poziom_1 = [ # Niewinne, romantyczne, rozgrzewka
    "Zdejmij skarpetki i/lub buty.",
    "Zrób mi 2-minutowy masaż karku.",
    "Patrz mi głęboko w oczy przez 60 sekund w całkowitej ciszy.",
    "Pocałuj mnie w oba policzki i w czoło.",
    "Powiedz mi 3 rzeczy, które najbardziej we mnie cenisz.",
    "Miziaj mnie po włosach przez 2 minuty.",
    "Obejmij mnie mocno i przytulaj przez pełną minutę.",
    "Zdejmij ze mnie jeden wybrany dodatek (zegarek, biżuteria)."
]

kary_poziom_2 = [ # Zmysłowe, budujące napięcie
    "Pocałuj mnie namiętnie, używając tylko warg (bez języka) przez 30 sekund.",
    "Zrób mi 3-minutowy masaż stóp.",
    "Pocałuj mnie powoli w szyję tuż za uchem.",
    "Zdejmij koszulkę / bluzkę.",
    "Zamknij oczy. Będę Cię dotykać przez 30 sekund, a Ty musisz zgadnąć czym.",
    "Wyszeptaj mi do ucha coś bardzo niegrzecznego, co chciałbyś/chciałabyś dzisiaj zrobić.",
    "Pocałuj moje ramię, schodząc powoli w stronę dekoltu/klatki piersiowej.",
    "Przejedź opuszkiem palca powoli wzdłuż mojego kręgosłupa."
]

kary_poziom_3 = [ # Gorące (DO WYPEŁNIENIA PRZEZ WAS)
    "[TUTAJ WPISZ GORĄCE ZADANIE, np. związane ze zdejmowaniem reszty ubrań]",
    "[TUTAJ WPISZ GORĄCE ZADANIE]",
    "[TUTAJ WPISZ GORĄCE ZADANIE]",
    "[TUTAJ WPISZ GORĄCE ZADANIE]"
]

kary_poziom_4 = [ # Mega erotyczne i finałowe (DO WYPEŁNIENIA PRZEZ WAS)
    "[TUTAJ WPISZ BARDZO PIKANTNE ZADANIE]",
    "[TUTAJ WPISZ BARDZO PIKANTNE ZADANIE]",
    "[TUTAJ WPISZ BARDZO PIKANTNE ZADANIE]",
    "Odłóżcie telefony. Czas na nagrodę główną. 😈"
]

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
