import streamlit as st
import random

# --- 1. Konfiguracja strony ---
st.set_page_config(page_title="Gorący Test Zgodności", page_icon="🌶️", layout="centered")

# --- 2. Baza danych (Pytania i Kary) ---
# Tutaj możesz wpisać własne, najbardziej pasujące do Was pytania!
pytania = [
    "Pytanie do Niego: Jakie jest moje ulubione miejsce na Twoim ciele?",
    "Pytanie do Niej: W co byłem ubrany na naszej pierwszej randce?",
    "Pytanie do Niego: Jaka jest moja absolutnie ulubiona pozycja w sypialni?",
    "Pytanie do Niej: Gdybyś przez 5 minut mogła robić ze mną wszystko, od czego byś zaczęła?",
    "Pytanie do Niego: Jaką moją bieliznę uważam za najseksowniejszą?"
]

kary = [
    "Zdejmij jedną część garderoby (skarpetki się nie liczą!).",
    "Zrób mi 3-minutowy, zmysłowy masaż wybranego przeze mnie miejsca.",
    "Zamknij oczy. Będę Cię dotykać przez minutę, a Ty musisz zgadnąć czym to robię.",
    "Zatańcz dla mnie przez 30 sekund.",
    "Pocałuj mnie w wybrane przeze mnie miejsce (ale nie w usta)."
]

# --- 3. Pamięć aplikacji (Session State) ---
if 'index_pytania' not in st.session_state:
    st.session_state.index_pytania = 0
if 'pokaz_kare' not in st.session_state:
    st.session_state.pokaz_kare = False
if 'obecna_kara' not in st.session_state:
    st.session_state.obecna_kara = ""

# Funkcja do przełączania pytań
def nastepne_pytanie():
    st.session_state.index_pytania += 1
    st.session_state.pokaz_kare = False

# --- 4. Interfejs Użytkownika (UI) ---
st.title("🔥 Gorący Test Zgodności")
st.markdown("---")

# Jeśli są jeszcze jakieś pytania
if st.session_state.index_pytania < len(pytania):
    
    # Wyświetl aktualne pytanie
    aktualne_pytanie = pytania[st.session_state.index_pytania]
    st.subheader(f"Pytanie {st.session_state.index_pytania + 1} z {len(pytania)}")
    st.info(aktualne_pytanie)

    st.write("*(Odpowiedz na głos. Osoba trzymająca telefon ocenia!)*")

    # Jeśli uaktywniono karę, pokaż ją i przycisk przejścia dalej
    if st.session_state.pokaz_kare:
        st.error(f"🚨 **CZAS NA ZADANIE!** 🚨\n\n**{st.session_state.obecna_kara}**")
        st.button("➡️ Kliknij, gdy zadanie zostanie wykonane", on_click=nastepne_pytanie, use_container_width=True)
    
    # Jeśli nie ma kary, pokaż przyciski do oceny
    else:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🟩 ZALICZONE (Prawda)", use_container_width=True):
                st.success("Punkt! Obyło się bez kary.")
                nastepne_pytanie()
                st.rerun()
        with col2:
            if st.button("🟥 KARA! (Fałsz)", use_container_width=True):
                st.session_state.pokaz_kare = True
                st.session_state.obecna_kara = random.choice(kary)
                st.rerun()

# Ekran końcowy
else:
    st.success("Dotarliście do końca! Teraz ogranicza Was tylko wyobraźnia... 😈")
    if st.button("🔄 Zagraj od nowa", use_container_width=True):
        st.session_state.index_pytania = 0
        st.session_state.pokaz_kare = False
        st.rerun()
