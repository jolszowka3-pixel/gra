import streamlit as st
import random

# --- 1. Konfiguracja ---
st.set_page_config(page_title="Gorący Test Zgodności", layout="wide", page_icon="🔥")
query_params = st.query_params
view_type = query_params.get("view", "selection")

# --- 2. Baza Pytań (50 sztuk) ---
pytania = [
    # Rozgrzewka
    "Jakie jest moje ulubione wspomnienie z naszej pierwszej randki?",
    "W czym, według Ciebie, wyglądam najatrakcyjniej na co dzień?",
    "Jaka cecha mojego charakteru najbardziej Cię pociąga?",
    "Co pomyślałem/am, kiedy pierwszy raz się pocałowaliśmy?",
    "Jakie jest moje ulubione miejsce na Twoim ciele, które nie jest strefą intymną?",
    "Jaki mój nawyk uważasz za najbardziej uroczy?",
    "Gdybyśmy mieli wyjechać na romantyczny weekend, jakie miejsce bym wybrał/a?",
    "Co najbardziej lubię z Tobą robić w leniwe niedzielne poranki?",
    "Jaki komplement od Ciebie sprawił mi największą radość?",
    "W jakiej sytuacji ostatnio poczułem/am się przez Ciebie bardzo kochany/a?",
    "Jaki jest mój ulubiony sposób na relaks po ciężkim dniu?",
    "Która piosenka najbardziej kojarzy mi się z naszym związkiem?",
    # Wchodzimy głębiej
    "Gdzie najczęściej ucieka mój wzrok, gdy się przebierasz?",
    "Co robię, gdy mam ochotę na seks, ale nie mówię tego wprost?",
    "Który z naszych pocałunków zapadł mi najbardziej w pamięć?",
    "W jakiej bieliźnie (mojej lub Twojej) lubię Cię/siebie najbardziej?",
    "Jaki rodzaj dotyku najbardziej mnie relaksuje?",
    "Co najbardziej lubię, gdy zasypiamy lub budzimy się obok siebie?",
    "Gdzie w miejscu publicznym najchętniej bym Cię pocałował/a?",
    "Które Twoje słowa w łóżku działają na mnie najmocniej?",
    "Jaka część mojego ciała jest najbardziej wrażliwa na pieszczoty (poza strefami intymnymi)?",
    "Gdybym miał/a wybrać jeden gadżet z naszej sypialni na bezludną wyspę, co by to było?",
    "Co uważam za naszą największą 'zaletę' jako pary w sypialni?",
    "Jaką jedną rzecz, którą robimy w łóżku rzadko, chciał(a)bym robić częściej?",
    "Jaki był mój najodważniejszy sen z Twoim udziałem?",
    # Robi się gorąco
    "W jakiej pozycji najszybciej osiągam orgazm?",
    "Co sprawia, że od razu dostaję gęsiej skórki pod Twoim dotykiem?",
    "Jaka jest moja ulubiona pora dnia na uprawianie miłości?",
    "Gdybyśmy mieli spróbować nowej lokacji w domu na seks, co bym wybrał/a?",
    "Jakie tempo w łóżku lubię najbardziej – powoli i zmysłowo, czy ostro i namiętnie?",
    "Co najbardziej kręci mnie w Twoim ciele, gdy jesteś całkowicie nago?",
    "Jakie słówko lub dźwięk wydaję, gdy jest mi najlepiej?",
    "Co myślę o porannym seksie?",
    "Jaki rodzaj gry wstępnej sprawia, że dosłownie tracę głowę?",
    "Gdybym mógł/mogła mieć na Tobie teraz tylko jedną rzecz, co by to było?",
    "Co uważam za Twój największy atut w sypialni?",
    "Gdybym miał/a zaplanować idealny erotyczny wieczór dla nas, od czego bym zaczął/zaczęła?",
    "Czego pragnę, gdy patrzę głęboko w Twoje oczy w trakcie stosunku?",
    # Hardcore i Fantazje
    "Jaka jest moja najbardziej skryta fantazja erotyczna?",
    "Gdybym dzisiaj mógł/mogła przejąć pełną kontrolę na 10 minut, co bym z Tobą zrobił/a?",
    "Co najbardziej podoba mi się w widoku Twojej twarzy, gdy dochodzisz?",
    "Które z naszych 'pikantnych' doświadczeń chciał(a)bym powtórzyć w pierwszej kolejności?",
    "Jaka nowa pozycja lub zabawa chodzi mi ostatnio po głowie?",
    "Gdybyś zgodził/a się dzisiaj absolutnie na wszystko, o co poproszę jako pierwsze?",
    "Co czuję, kiedy zdejmujesz ze mnie ostatni element ubrania?",
    "Jaki rodzaj 'brudnego gadania' (dirty talk) kręci mnie najbardziej?",
    "Czy wolał(a)bym dzisiaj dłuższą grę wstępną, czy szybki, namiętny numerek?",
    "Jakie miejsce na Twoim ciele chciał(a)bym teraz popieścić swoimi ustami?",
    "Gdybym miał/a opisać mój najlepszy orgazm z Tobą w trzech słowach, jak by brzmiały?",
    "Czego najbardziej nie mogę się doczekać, gdy wyłączymy tę grę?"
]

# --- 3. Baza Kar (Podzielona na 4 poziomy) ---
kary_poziom_1 = [ # Niewinne i zmysłowe
    "Zdejmij skarpetki i/lub buty.",
    "Zrób mi 2-minutowy masaż karku.",
    "Patrz mi głęboko w oczy przez 60 sekund bez odwracania wzroku.",
    "Pocałuj mnie w oba policzki i w czoło.",
    "Powiedz mi 3 rzeczy, które najbardziej we mnie cenisz.",
    "Miziaj mnie po włosach przez 2 minuty.",
    "Zdejmij biżuterię, zegarek lub inne dodatki.",
    "Daj mi zmysłowy pocałunek w dłoń.",
    "Obejmij mnie mocno i przytulaj przez pełną minutę.",
    "Opisz zapach moich perfum/ciała własnymi słowami.",
    "Pogłaszcz mnie po plecach (przez ubranie) przez minutę.",
    "Pocałuj moje ramię."
]

kary_poziom_2 = [ # Budowanie napięcia
    "Zdejmij koszulkę / bluzkę.",
    "Pocałuj mnie w szyję z użyciem języka.",
    "Przejedź dłonią powoli po moim udzie.",
    "Zrób mi 3-minutowy masaż stóp.",
    "Zdejmij spodnie / spódnicę.",
    "Zawiąż mi oczy na czas trwania kolejnego pytania.",
    "Przyłóż wargi do mojego ucha i oddychaj głęboko przez 30 sekund.",
    "Pocałuj mnie namiętnie w usta przez minimum 10 sekund.",
    "Przejedź opuszkiem palca wzdłuż mojego kręgosłupa.",
    "Zatańcz dla mnie seksownie przez 30 sekund.",
    "Pozwól mi zdjąć z Ciebie jedną dowolną część garderoby.",
    "Delikatnie possij mój płatek ucha."
]

kary_poziom_3 = [ # Gorące i erotyczne
    "Zdejmij z siebie bieliznę z górnej partii ciała.",
    "Pocałuj mnie w brzuch, powoli schodząc coraz niżej.",
    "Zrób mi 5-minutowy zmysłowy masaż używając olejku/balsamu.",
    "Weź moją dłoń i połóż na miejscu, w którym chcesz, bym Cię teraz dotykał(a).",
    "Wykorzystaj kostkę lodu (lub chłodny palec) i obrysuj moje strefy erogenne.",
    "Całuj wewnętrzną stronę moich ud przez minutę.",
    "Zdejmij z siebie całą bieliznę z dolnej partii ciała.",
    "Dotykaj moich stref intymnych (przez bieliznę lub bez) przez 2 minuty.",
    "Zdejmij ze mnie jedną część garderoby używając tylko zębów.",
    "Usiądź na mnie okrakiem na czas dwóch kolejnych pytań.",
    "Wymasuj moje pośladki.",
    "Wyszeptaj mi do ucha dokładnie to, co chcesz, żebym Ci za chwilę zrobił(a)."
]

kary_poziom_4 = [ # Mega erotyczne i seksualne
    "Zdejmijcie z siebie wszystko. Gra toczy się nago.",
    "Pieść mnie ustami (oralnie) przez minimum 3 minuty.",
    "Pozwól mi użyć na Tobie Twojego ulubionego gadżetu przez 2 minuty.",
    "Spraw, żebym jęknął/jęknęła z rozkoszy.",
    "Wejdź we mnie / pozwól mi wejść w Ciebie na kilka minut powolnych ruchów.",
    "Pocałuj mnie w najdelikatniejszą część moich stref intymnych.",
    "Stymuluj mnie ręką, patrząc mi głęboko w oczy.",
    "Ustaw nas w pozycji 69 i bawmy się tak przez 3 minuty.",
    "Będziesz uległy/uległa przez następne 5 minut – spełniasz każdą moją zachciankę.",
    "Odrobinę mnie 'podduś' lub delikatnie klapnij klapsa (za obopólną zgodą!).",
    "Zacznijmy stosunek, ale przerwijmy w najlepszym momencie, by kontynuować grę.",
    "Odłóżcie telefony. Kary się skończyły, czas na nagrodę główną. 😈"
]

# --- 4. Funkcja wybierająca karę ze względu na etap ---
def wylosuj_kare(numer_pytania):
    if numer_pytania < 12:
        return random.choice(kary_poziom_1)
    elif numer_pytania < 25:
        return random.choice(kary_poziom_2)
    elif numer_pytania < 38:
        return random.choice(kary_poziom_3)
    else:
        return random.choice(kary_poziom_4)

# --- 5. Synchronizacja stanu (Shared State) ---
@st.cache_resource
def get_global_state():
    return {"current_q": 0, "status": "pending", "penalty": ""}

state = get_global_state()

# --- WIDOK 1: WYBÓR ROLI ---
if view_type == "selection":
    st.title("🔥 Gorący Test Zgodności")
    st.markdown("Wybierzcie, które urządzenie pełni jaką rolę.")
    st.link_button("📺 Ustaw jako TELEWIZOR (Panel Główny)", "/?view=tv")
    st.link_button("📱 Ustaw jako PILOT (Do oceny na telefonie)", "/?view=pilot")

# --- WIDOK 2: TELEWIZOR ---
elif view_type == "tv":
    st.title("🔥 Panel Główny")
    q_idx = state["current_q"]
    
    if q_idx < len(pytania):
        # Progress bar
        progress = (q_idx) / len(pytania)
        st.progress(progress)
        
        st.header(f"Runda {q_idx + 1} / {len(pytania)}")
        st.markdown(f"<h1 style='text-align: center; font-size: 50px; color: #ff4b4b; padding: 40px;'>{pytania[q_idx]}</h1>", unsafe_allow_html=True)
        
        if state["status"] == "wrong":
            st.markdown(f"""
            <div style='background-color: #ffcccc; padding: 20px; border-radius: 10px; text-align: center; border: 2px solid red;'>
                <h2 style='color: red;'>🚨 BŁĄD! CZAS NA ZADANIE:</h2>
                <h1 style='color: black;'>{state['penalty']}</h1>
            </div>
            """, unsafe_allow_html=True)
        elif state["status"] == "correct":
            st.markdown("""
            <div style='background-color: #ccffcc; padding: 20px; border-radius: 10px; text-align: center; border: 2px solid green;'>
                <h2 style='color: green;'>✅ PRAWDA! Zaliczone bez zadania.</h2>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.balloons()
        st.markdown("<h1 style='text-align: center; font-size: 70px; color: purple;'>Mamy finał! Odłóżcie sprzęt, reszta zależy od Was... 😈</h1>", unsafe_allow_html=True)
    
    st.empty()
    st.rerun()

# --- WIDOK 3: PILOT ---
elif view_type == "pilot":
    st.title("📱 Panel Sędziego")
    q_idx = state["current_q"]
    
    if q_idx < len(pytania):
        st.info(f"Oceniasz odpowiedź na pytanie: **{pytania[q_idx]}**")
        
        st.markdown("### Jak oceniasz?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ PRAWDA (Bez kary)", use_container_width=True, type="primary"):
                state["status"] = "correct"
                st.rerun()
        with col2:
            if st.button("🟥 FAŁSZ (Nałóż karę!)", use_container_width=True):
                state["status"] = "wrong"
                state["penalty"] = wylosuj_kare(q_idx)
                st.rerun()
        
        st.markdown("---")
        if st.button("➡️ Przejdź do kolejnego pytania", use_container_width=True):
            state["status"] = "pending"
            state["current_q"] += 1
            st.rerun()
            
        if st.button("🔄 Zresetuj grę", use_container_width=True):
            state["current_q"] = 0
            state["status"] = "pending"
            st.rerun()
    else:
        st.success("Koniec pytań. Cieszcie się wieczorem!")
