import streamlit as st
import random
import pandas as pd # Do symulacji prostego zapisu stanu

# --- 1. Konfiguracja ---
st.set_page_config(page_title="Gra Erotyczna", layout="wide")

# Parametry URL określają, co widzi użytkownik
query_params = st.query_params
view_type = query_params.get("view", "selection")

# --- 2. Baza Pytań ---
pytania = [
    {"q": "Pytanie do Niego: Co najbardziej kręci mnie w Twoim dotyku?", "type": "on"},
    {"q": "Pytanie do Niej: Jaka jest moja ulubiona fantazja?", "type": "ona"},
]

kary = ["Masaż stóp", "Zdejmij coś", "Pocałunek w szyję"]

# --- WAŻNE: Synchronizacja ---
# W wersji darmowej Community Cloud, najprościej użyć st.cache_resource 
# do współdzielenia stanu między użytkownikami (uwaga: zadziała to tylko na jednym serwerze!)
@st.cache_resource
def get_global_state():
    return {"current_q": 0, "status": "pending", "penalty": ""}

state = get_global_state()

# --- WIDOK 1: WYBÓR ROLI ---
if view_type == "selection":
    st.title("Wybierz tryb urządzenia")
    st.link_button("📺 Ustaw jako TELEWIZOR", "/?view=tv")
    st.link_button("📱 Ustaw jako PILOT", "/?view=pilot")

# --- WIDOK 2: TELEWIZOR (Tylko wyświetlanie) ---
elif view_type == "tv":
    st.title("🔥 Panel Główny")
    q_idx = state["current_q"]
    
    if q_idx < len(pytania):
        st.header(f"Runda {q_idx + 1}")
        st.markdown(f"<h1 style='text-align: center; font-size: 60px;'>{pytania[q_idx]['q']}</h1>", unsafe_allow_html=True)
        
        if state["status"] == "wrong":
            st.error(f"🚨 KARA: {state['penalty']}")
        elif state["status"] == "correct":
            st.success("✅ Brawo! Punkt zdobyty.")
    else:
        st.balloons()
        st.header("Koniec gry! Czas na finał... 😈")
    
    # Automatyczne odświeżanie TV co 2 sekundy, żeby widzieć zmiany z telefonu
    st.empty()
    st.rerun()

# --- WIDOK 3: PILOT (Sterowanie) ---
elif view_type == "pilot":
    st.title("📱 Twój Pilot")
    q_idx = state["current_q"]
    
    if q_idx < len(pytania):
        st.write(f"Aktualne pytanie na TV: **{pytania[q_idx]['q']}**")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ ZALICZONE", use_container_width=True):
                state["status"] = "correct"
                state["current_q"] += 1
                st.rerun()
        with col2:
            if st.button("🟥 BŁĄD / KARA", use_container_width=True):
                state["status"] = "wrong"
                state["penalty"] = random.choice(kary)
                st.rerun()
        
        if st.button("➡️ Następne pytanie", use_container_width=True):
            state["status"] = "pending"
            state["current_q"] += 1
            st.rerun()
    else:
        st.write("Gra zakończona!")
