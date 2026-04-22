import streamlit as st
import random
import time
from streamlit_autorefresh import st_autorefresh

# ==========================================
# 1. KONFIGURACJA I WASZE IMIONA
# ==========================================
IMIE_ONA = "Ona"   
IMIE_ON = "On"     

st.set_page_config(page_title="Wieczór we Dwoje", layout="wide", page_icon="🥂")
query_params = st.query_params
view_type = query_params.get("view", "selection")

# ==========================================
# 2. GŁÓWNY CSS (LUKSUSOWY PREMIUM GOLD + STATY)
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
        text-align: center; margin: 20px auto; max-width: 1000px;
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
    .turn-intro { background-color: rgba(75, 214, 123, 0.1); border: 1px solid #4bd67b; color: #4bd67b; }

    /* PANEL STATYSTYK */
    .stats-container {
        display: flex; justify-content: space-around; max-width: 1000px; margin: 0 auto;
    }
    .stat-card {
        background: rgba(21, 16, 28, 0.6); padding: 15px 30px; border-radius: 20px;
        border: 1px solid #2a2035; text-align: center; min-width: 200px;
    }
    .stat-name { color: #8c7a96; font-size: 14px; letter-spacing: 2px; margin-bottom: 5px; }
    .stat-lives { color: #d4af37; font-size: 24px; font-weight: bold; }

    /* PRZYCISKI PILOTA */
    div.stButton > button {
        height: 20vh !important; width: 100% !important;
        border-radius: 30px !important; margin-top: 1vh;
        box-shadow: 0 15px 30px rgba(0,0,0,0.8) !important;
        background: linear-gradient(145deg, #1a1323, #0d0a13) !important;
        border: 2px solid #d4af37 !important;
    }
    div.stButton > button p { 
        font-size: 30px !important; font-weight: bold !important; 
        color: #d4af37 !important;
    }

    /* PRZYCISKI RESET / NASTĘPNE */
    div.stButton:nth-last-child(1) > button, div.stButton:nth-last-child(2) > button {
        height: 60px !important; background-color: transparent !important;
        border: 1px solid #2a2035 !important; box-shadow: none !important;
    }
    div.stButton:nth-last-child(1) > button p, div.stButton:nth-last-child(2) > button p { 
        font-size: 16px !important; color: #8c7a96 !important;
    }

    div[data-testid="stLinkButton"] > a {
        background: linear-gradient(145deg, #1a1323, #0d0a13) !important;
        border: 1px solid #d4af37 !important; color: #d4af37 !important;
        border-radius: 20px !important; padding: 25px !important;
        font-size: 24px !important; text-align: center !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. BAZA DANYCH (TEST WIEDZY O PARTNERZE 🔥)
# ==========================================

pytania_intro = [
    {"kto": "ONA", "tekst": "Zgadnij, jaki gatunek filmowy według MNIE najlepiej opisuje nasz związek?"},
    {"kto": "ON", "tekst": "Co JA uważam za najważniejszą lekcję o miłości, jaką wyciągnąłem z naszej relacji?"},
    {"kto": "ONA", "tekst": "Jak myślisz, co we mnie najbardziej zmieniło się na plus od kiedy jesteśmy razem?"},
    {"kto": "ON", "tekst": "Zgadnij, w jakiej codziennej, prozaicznej sytuacji czuję z Tobą najsilniejszą więź?"},
    {"kto": "ONA", "tekst": "Gdybym to JA miała stworzyć naszą nową wspólną tradycję, jak myślisz, co by to było?"},
    {"kto": "ON", "tekst": "Jaka drobna rzecz, którą dla mnie robisz, ma dla mnie osobiście największe znaczenie?"},
    {"kto": "ONA", "tekst": "O jakim moim ukrytym talencie lub pasji chciałabym, żebyśmy rozmawiali częściej?"},
    {"kto": "ON", "tekst": "Gdybym to JA mógł cofnąć czas i zmienić jedną naszą decyzję w przeszłości, co bym wybrał?"},
    {"kto": "ONA", "tekst": "Przypomnij sobie sytuację, w której poczułam się przez Ciebie w 100% zrozumiana. Kiedy to było?"},
    {"kto": "ON", "tekst": "Zgadnij, które z Twoich słów dają mi największe poczucie spokoju i bezpieczeństwa?"},
    {"kto": "ONA", "tekst": "Gdybyśmy utknęli na bezludnej wyspie, jaką jedną, bezużyteczną rzecz zabrałabym ze sobą?"},
    {"kto": "ON", "tekst": "Jak myślę, która z moich cech charakteru będzie mnie najbardziej definiować na starość?"},
    {"kto": "ONA", "tekst": "Co JA uważam za nasz absolutnie największy, wspólny sukces do tej pory?"},
    {"kto": "ON", "tekst": "Czego najbardziej chciałbym z Tobą spróbować w nadchodzącym roku (nie w sypialni)?"},
    {"kto": "ONA", "tekst": "Jakie Twoje dziwactwo, które na początku mnie irytowało, teraz potajemnie uwielbiam?"},
    {"kto": "ON", "tekst": "Gdybym miał zaplanować dla nas mój wymarzony dzień od A do Z, co byśmy robili po południu?"}
]

toasty = [
    "Zdrowie za tego, kto dziś ma lepszą pamięć! 🧠",
    "Pijemy za nasze grzeszne myśli – niech staną się czynami! 😈",
    "Toast za sąsiadów, oby mieli dziś mocny sen! 🤫",
    "Pijemy łyk z zamkniętymi oczami, wyobrażając sobie, co stanie się za godzinę! 🍷",
    "Za każdą kroplę potu, którą dziś z siebie wyciśniemy! 💦",
    "Toast za nasze usta i to, do czego są zdolne! 🥂",
    "Pijemy za spontaniczność – łamanie zasad jest dziś dozwolone! 🥃",
    "Wypijmy za to, kto jako pierwszy oblał dzisiaj test! 🍾",
    "Zdrowie za dzikie fantazje, do których boimy się przyznać! 🔥",
    "Toast bez użycia rąk – pijemy prosto ze swoich ust! 🍷",
    "Za łóżko, podłogę, stół... i wszystkie inne miejsca, które dziś zwiedzimy! 🥂"
]

p1 = [
    {"kto": "ONA", "tekst": "Zgadnij, jaka była MOJA absolutnie pierwsza myśl, kiedy Cię poznałam?"},
    {"kto": "ON", "tekst": "Jak myślisz, co JA uważam za Twoją najbardziej atrakcyjną cechę charakteru?"},
    {"kto": "ONA", "tekst": "W jakim konkretnym ubraniu (z Twojej szafy) uważam, że wyglądasz najgoręcej?"},
    {"kto": "ON", "tekst": "Zgadnij, jaki Twój codzienny nawyk uważam za najbardziej uroczy?"},
    {"kto": "ONA", "tekst": "Jak myślę o nas, to jakie jest MOJE najpiękniejsze wspomnienie z naszych początków?"},
    {"kto": "ON", "tekst": "Co najbardziej sprawia, że JA czuję się przy Tobie stuprocentowym mężczyzną?"},
    {"kto": "ONA", "tekst": "Zgadnij, jaki komplement od Ciebie sprawia, że promienieję najmocniej?"},
    {"kto": "ON", "tekst": "Gdybym mógł zabrać nas na romantyczny weekend w jedno miejsce, gdzie bym wybrał?"},
    {"kto": "ONA", "tekst": "Jaki Twój zapach (perfumy lub naturalny) kręci MNIE najbardziej?"},
    {"kto": "ON", "tekst": "Zgadnij, które z naszych wspólnych zdjęć trzymam w pamięci jako ulubione?"},
    {"kto": "ONA", "tekst": "Jaka piosenka absolutnie zawsze, natychmiast przypomina MI o Tobie?"},
    {"kto": "ON", "tekst": "Jak myślisz, co najbardziej lubię robić, leżąc z Tobą w leniwy, niedzielny poranek?"},
    {"kto": "ONA", "tekst": "Zgadnij, czego JA bałabym się najbardziej, gdybym miała Cię stracić?"},
    {"kto": "ON", "tekst": "Co uważam za najbardziej szaloną rzecz, jaką zrobiłem na początku, by Ci zaimponować?"},
    {"kto": "ONA", "tekst": "Zgadnij, co w Twoim spojrzeniu upewnia mnie w tym, że masz na mnie wielką ochotę?"},
    {"kto": "ON", "tekst": "Kiedy wracam zmęczony z pracy, jakiego jednego Twojego gestu pragnę najbardziej?"},
    {"kto": "ONA", "tekst": "Czy według mnie lepiej całujesz, gdy jesteś wypity, czy całkowicie trzeźwy?"},
    {"kto": "ON", "tekst": "Jak myślisz, która część Twojej twarzy jest MOJĄ absolutnie ulubioną?"},
    {"kto": "ONA", "tekst": "W jakim Twoim zachowaniu w towarzystwie widzę największą klasę?"},
    {"kto": "ON", "tekst": "Gdy patrzę na Ciebie z drugiego końca pokoju, na co najczęściej zwracam uwagę?"}
]

p2 = [
    {"kto": "ONA", "tekst": "Zgadnij, gdzie na moim ciele dotyk Twoich ust sprawia MI największą przyjemność?"},
    {"kto": "ON", "tekst": "Jak myślisz, jaka pieszczota z Twojej strony najszybciej wywołuje u MNIE dreszcze?"},
    {"kto": "ONA", "tekst": "Które Twoje 'niegrzeczne' słowo szeptane do ucha działa na MNIE jak magnes?"},
    {"kto": "ON", "tekst": "Zgadnij, w jakiej swojej bieliźnie (kolor/fason) według MNIE wyglądasz najlepiej?"},
    {"kto": "ONA", "tekst": "Który z naszych pocałunków w miejscu publicznym JA zapamiętałam jako najgorętszy?"},
    {"kto": "ON", "tekst": "Co JA najbardziej lubię robić z Twoimi włosami, kiedy się namiętnie całujemy?"},
    {"kto": "ONA", "tekst": "Wybierz jedno: czy JA wolę szybki seks po przebudzeniu, czy długą grę wstępną wieczorem?"},
    {"kto": "ON", "tekst": "Jakie miejsce na Twoim ciele JA uważam za najbardziej wrażliwe na mój dotyk?"},
    {"kto": "ONA", "tekst": "Gdybym miała na sobie wszystkie ubrania, od zdjęcia czego najbardziej chciałabym, żebyś zaczął?"},
    {"kto": "ON", "tekst": "Jak myślisz, jaki rodzaj masażu lubię otrzymywać od Ciebie najbardziej?"},
    {"kto": "ONA", "tekst": "Gdybym mogła ucałować tylko jedno miejsce na Twoim ciele, by Cię podniecić, co bym wybrała?"},
    {"kto": "ON", "tekst": "Co we mnie budzi we MNIE największe pożądanie, gdy jesteśmy sami?"},
    {"kto": "ONA", "tekst": "Co kręci MNIE w Twoim głosie najbardziej: ton, głośność czy to co mówisz?"},
    {"kto": "ON", "tekst": "Wolisz wiedzieć, czy zgadnąć: w jakich sytuacjach potajemnie wyobrażam Cię sobie bez ubrań?"},
    {"kto": "ONA", "tekst": "Co czuję w środku, gdy gładzisz mnie z tyłu po karku?"},
    {"kto": "ON", "tekst": "Zgadnij: czy wolę całować się z Tobą bardzo delikatnie, czy z wyraźną, agresywną pasją?"},
    {"kto": "ONA", "tekst": "Jaka jest MOJA reakcja w głowie, gdy w miejscu publicznym dyskretnie mnie dotykasz?"},
    {"kto": "ON", "tekst": "Co w Twoim zachowaniu daje MI najbardziej bezpośredni sygnał, że to jest 'ten' moment?"},
    {"kto": "ONA", "tekst": "Co sprawia MI większą frajdę: widok, gdy zdejmujesz mi bieliznę rękami, czy zębami?"},
    {"kto": "ON", "tekst": "Jak bardzo kręci MNIE, gdy chodzisz po domu tylko w mojej koszulce?"}
]

p3 = [
    {"kto": "ONA", "tekst": "Zgadnij, jaka jest MOJA ulubiona pozycja w łóżku, w której czuję największą rozkosz?"},
    {"kto": "ON", "tekst": "Jakie nietypowe miejsce poza sypialnią w naszym domu kręci MNIE na 'szybki numerek'?"},
    {"kto": "ONA", "tekst": "Co JA lubię najbardziej w Twoim ciele, gdy zbliżamy się do szczytu?"},
    {"kto": "ON", "tekst": "Jaki rodzaj uścisku podczas seksu preferuję: gdy wbijasz we mnie paznokcie, czy mocno przytulasz?"},
    {"kto": "ONA", "tekst": "Zgadnij, jaka jest MOJA najbardziej skryta fantazja, o której kiedykolwiek rozmawialiśmy?"},
    {"kto": "ON", "tekst": "Który z naszych gadżetów jest MOIM osobistym faworytem podczas naszych zabaw?"},
    {"kto": "ONA", "tekst": "Jakie dźwięki, które z siebie wydajesz, sprawiają, że dochodzę znacznie szybciej?"},
    {"kto": "ON", "tekst": "Zgadnij, w jakiej pozycji mam wizualnie najwspanialszy widok na Twoje ciało?"},
    {"kto": "ONA", "tekst": "Czego chciałabym spróbować częściej, a o co rzadko Cię proszę?"},
    {"kto": "ON", "tekst": "Zgadnij, co we mnie kręci mnie najbardziej, jeśli chodzi o seks oralny (Dawanie vs Branie)?"},
    {"kto": "ONA", "tekst": "Czy według MNIE lepszy seks mamy rano po obudzeniu, czy głęboko w nocy?"},
    {"kto": "ON", "tekst": "Jak bardzo lubię, gdy celowo zostawiasz mi na skórze ślady po pocałunkach/malinki?"},
    {"kto": "ONA", "tekst": "Czy w łóżku wolę pełne światło, by wszystko widzieć, czy całkowity mrok i poleganie na dotyku?"},
    {"kto": "ON", "tekst": "Jak myślę, ile powinna trwać idealna gra wstępna, zanim przejdziemy do konkretów?"},
    {"kto": "ONA", "tekst": "Zgadnij: czy podnieca mnie myśl o tym, że uderzysz mnie lekko w pośladki?"},
    {"kto": "ON", "tekst": "Co uważam za naszą absolutnie najgorętszą, wspólną noc do tej pory?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy pociąga mnie myśl o seksie przed wielkim, wyraźnym lustrem?"},
    {"kto": "ON", "tekst": "Który z MOICH fetyszy lub słabości uważałaś na początku za najdziwniejszy?"},
    {"kto": "ONA", "tekst": "Co sprawia, że podczas zbliżenia czuję w 100%, że mam nad Tobą kontrolę?"},
    {"kto": "ON", "tekst": "Co najbardziej nakręca MNIE, gdy rozmawiamy niegrzecznie (dirty talk)?"}
]

p4 = [
    {"kto": "ONA", "tekst": "Gdybyśmy mieli jutro nagrać pikantne wideo, od jakiej sceny według MNIE powinniśmy zacząć?"},
    {"kto": "ON", "tekst": "W jakiej konkretnie pozie uważam, że Ty dochodzisz najszybciej i najbardziej intensywnie?"},
    {"kto": "ONA", "tekst": "Gdybym to JA mogła Cię mocno uwiązać, do czego dobrałabym się w pierwszej kolejności?"},
    {"kto": "ON", "tekst": "Co w Twoim zachowaniu sprawia, że JA jako mężczyzna całkowicie tracę nad sobą panowanie?"},
    {"kto": "ONA", "tekst": "Którą część Twojego ciała miałabym ochotę pieścić swoimi ustami od zaraz, najdłużej?"},
    {"kto": "ON", "tekst": "Zgadnij, jaka jest MOJA najostrzejsza fantazja z Tobą w roli głównej, która wciąż czeka na realizację?"},
    {"kto": "ONA", "tekst": "Czy kiedykolwiek, w najgłębszych zakamarkach umysłu, rozważałam dołączenie kogoś trzeciego do zabawy?"},
    {"kto": "ON", "tekst": "Jakie miejsce publiczne kręci MNIE najbardziej jako bardzo ryzykowna scena seksu?"},
    {"kto": "ONA", "tekst": "Jaka jest absolutnie najbardziej 'brudna' rzecz, jaką kiedykolwiek pomyślałam, patrząc na Ciebie?"},
    {"kto": "ON", "tekst": "Zgadnij: czy bardziej kręciłaby MNIE na Tobie kostka lodu (zimno), czy kapiący, ciepły wosk ze świecy?"},
    {"kto": "ONA", "tekst": "Czy kiedykolwiek fantazjowałam o byciu dominowaną w sposób, którego nigdy Ci nie zdradziłam?"},
    {"kto": "ON", "tekst": "Kto z Twoich znajomych wydawał MI się kiedyś (nawet na sekundę) fizycznie atrakcyjny?"},
    {"kto": "ONA", "tekst": "Co kręci MNIE bardziej: gdy jesteś ze mną brutalny i zwierzęcy, czy niezwykle powolny i czuły?"},
    {"kto": "ON", "tekst": "Gdybym miał Ci rozkazać założyć dowolny, kiczowaty strój tematyczny do sypialni, co to by było?"},
    {"kto": "ONA", "tekst": "Co we mnie sprawia, że w trakcie ostrego seksu czuję się jak absolutna bogini?"},
    {"kto": "ON", "tekst": "Czy podoba MI się wizja tego, że po wszystkim na Twojej twarzy lub ciele zostają wyraźne ślady?"},
    {"kto": "ONA", "tekst": "Co bym pomyślała, gdybyś bez słowa nagle złapał mnie za włosy w trakcie stosunku?"},
    {"kto": "ON", "tekst": "Jak bardzo kręci MNIE ryzyko bycia złapanym przez obcych ludzi na gorącym uczynku?"},
    {"kto": "ONA", "tekst": "Który moment naszego seksu uważam za najbardziej zwierzęcy w całej naszej historii?"},
    {"kto": "ON", "tekst": "Jakie jest najmocniejsze obelżywe/niegrzeczne słowo, jakim chciałbym, żebyś mnie nazwała w łóżku?"}
]

# Kary zostają te same, co w poprzedniej kolosalnej wersji
# ==========================================
# 4. LOGIKA SYSTEMU WYKUPNEGO I GENEROWANIA GRY
# ==========================================

def get_buyout_info(refusals):
    if refusals < 5: return "FREE", f"ŻYCIE ❤️ (Zostało: {5 - refusals})"
    elif refusals < 8: return "SHOT_05", "KOSZT: 0.5 SHOTA 🥃"
    elif refusals < 11: return "SHOT_1", "KOSZT: 1 CAŁY SHOT 🥃"
    elif refusals < 14: return "SHOT_CLOTHES", "KOSZT: SHOT + UBRANIE 🔞"
    else: return "MANDATORY", "KARA JEST OBOWIĄZKOWA! 😈"

def pobierz_poziom(poziom, ile_par):
    pyt_ona = [q for q in poziom if str(q["kto"]).upper().strip() == "ONA"]
    pyt_on = [q for q in poziom if str(q["kto"]).upper().strip() == "ON"]
    random.shuffle(pyt_ona)
    random.shuffle(pyt_on)
    
    wynik = []
    for i in range(min(ile_par, len(pyt_ona), len(pyt_on))):
        wynik.append(pyt_ona[i])
        wynik.append(pyt_on[i])
    return wynik

def generuj_intro():
    # 3 pary = 6 pytań na rozgrzewkę (bez konsekwencji)
    return pobierz_poziom(pytania_intro, 3)

def generuj_gre():
    talia = pobierz_poziom(p1, 10) + pobierz_poziom(p2, 10) + pobierz_poziom(p3, 10) + pobierz_poziom(p4, 10)
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
# 5. SILNIK SYNCHRONIZACJI
# ==========================================
@st.cache_resource
def get_global_state():
    return {
        "phase": "intro",  # "intro" -> "main"
        "intro_q": 0,
        "intro_gra": generuj_intro(),
        "current_q": 0, 
        "status": "question", 
        "penalty": "", 
        "gra": generuj_gre(),
        "ona_refusals": 0, 
        "on_refusals": 0, 
        "buyout_msg": ""
    }

state = get_global_state()

# ==========================================
# 6. WIDOKI
# ==========================================

if view_type == "selection":
    st.markdown("<div class='elegant-header'>System Wieczoru</div><br>", unsafe_allow_html=True)
    st.link_button("📺 AKTYWUJ EKRAN TV", "/?view=tv", use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.link_button("📱 AKTYWUJ PILOTA", "/?view=pilot", use_container_width=True)

elif view_type == "tv":
    st_autorefresh(interval=1000, key="tv_refresh")
    
    # TV - FAZA ROZGRZEWKI
    if state["phase"] == "intro":
        q_idx = state["intro_q"]
        if q_idx < len(state["intro_gra"]):
            q = state["intro_gra"][q_idx]
            who_val = str(q["kto"]).upper().strip()
            imie_info = f"ROZMOWA: {IMIE_ONA if who_val == 'ONA' else IMIE_ON}"
            
            st.markdown(f"<div class='elegant-header'>Rozgrzewka ({q_idx + 1}/{len(state['intro_gra'])})</div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class='premium-box' style='border-color: #4bd67b;'>
                <div class='turn-badge turn-intro'>{imie_info}</div>
                <div class='gold-text'>{q['tekst']}</div>
                <p style='color: #8c7a96; font-size: 18px; margin-top: 20px;'>Czas na swobodną odpowiedź, bez stresu i kar. 💕</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Ekran przejścia
            st.markdown(f"""
            <div class='premium-box' style='border-color: #d4af37;'>
                <h1 class='gold-text'>ROZGRZEWKA ZAKOŃCZONA</h1>
                <p style='color: #8c7a96; font-size: 24px; margin-top: 20px;'>Pora podnieść temperaturę... Czekam na sygnał z pilota! 😈</p>
            </div>
            """, unsafe_allow_html=True)

    # TV - FAZA GŁÓWNA
    else:
        st.markdown(f"""
        <div class='stats-container'>
            <div class='stat-card'>
                <div class='stat-name'>{IMIE_ONA}</div>
                <div class='stat-lives'>{get_buyout_info(state['ona_refusals'])[1]}</div>
            </div>
            <div class='stat-card'>
                <div class='stat-name'>{IMIE_ON}</div>
                <div class='stat-lives'>{get_buyout_info(state['on_refusals'])[1]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        q_idx = state["current_q"]
        if q_idx < len(state["gra"]):
            q = state["gra"][q_idx]
            
            if state["status"] == "question":
                who_val = str(q["kto"]).upper().strip()
                badge_class = "turn-toast" if who_val == "TOAST" else ("turn-ona" if who_val == "ONA" else "turn-on")
                imie_info = "TOAST!" if who_val == "TOAST" else f"CZYTA: {IMIE_ONA if who_val == 'ONA' else IMIE_ON}"

                st.markdown(f"<div class='elegant-header'>Runda {q_idx + 1}</div>", unsafe_allow_html=True)
                st.markdown(f"""
                <div class='premium-box'>
                    <div class='turn-badge {badge_class}'>{imie_info}</div>
                    <div class='gold-text'>{q['tekst']}</div>
                </div>
                """, unsafe_allow_html=True)
                
            elif state["status"] == "decision":
                st.markdown(f"<div class='elegant-header'>Runda {q_idx + 1}</div>", unsafe_allow_html=True)
                st.markdown(f"""
                <div class='premium-box' style='background:rgba(21, 16, 28, 0.8); border-color:#d4af37;'>
                    <h1 class='gold-text'>ZŁA ODPOWIEDŹ... 🤔</h1>
                    <p style='color: #8c7a96; font-size: 24px; margin-top: 20px;'>Wykupne czy Kara? Decyzja na pilocie!</p>
                </div>
                """, unsafe_allow_html=True)
                
            elif state["status"] == "result":
                if state["buyout_msg"]:
                    txt, bg = state["buyout_msg"], "rgba(212, 175, 55, 0.15)"
                else:
                    txt, bg = f"ZADANIE: {state['penalty']}", "rgba(255, 75, 75, 0.15)"
                
                st.markdown(f"""
                <div class='premium-box' style='background:{bg}; border-color:#d4af37;'>
                    <h1 class='gold-text'>{txt}</h1>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("<div class='premium-box'><h1 class='gold-text'>KONIEC GRY.😈</h1></div>", unsafe_allow_html=True)

elif view_type == "pilot":
    # PILOT - FAZA ROZGRZEWKI
    if state["phase"] == "intro":
        q_idx = state["intro_q"]
        if q_idx < len(state["intro_gra"]):
            st.markdown(f"<p style='text-align:center; color:#4bd67b; font-size:24px;'>ROZGRZEWKA 💕</p>", unsafe_allow_html=True)
            if st.button("NASTĘPNE PYTANIE ➔", use_container_width=True):
                state["intro_q"] += 1
                st.rerun()
        else:
            st.markdown(f"<p style='text-align:center; color:#d4af37; font-size:24px;'>ROZGRZEWKA ZAKOŃCZONA</p>", unsafe_allow_html=True)
            if st.button("ZACZYNAMY GRĘ WŁAŚCIWĄ 😈", use_container_width=True, type="primary"):
                state["phase"] = "main"
                st.rerun()

    # PILOT - FAZA GŁÓWNA
    else:
        q_idx = state["current_q"]
        if q_idx < len(state["gra"]):
            q = state["gra"][q_idx]
            who_val = str(q["kto"]).upper().strip()
            sedzia_imie = IMIE_ONA if who_val == "ONA" else IMIE_ON
            
            if state["status"] == "question":
                if who_val == "TOAST":
                    if st.button("WYPITE! 🥂", use_container_width=True):
                        state["status"] = "result"; state["buyout_msg"] = "NA ZDROWIE!"; st.rerun()
                else:
                    st.markdown(f"<p style='text-align:center; color:#d4af37; font-size:20px;'>Odpowiada: <b>{sedzia_imie}</b></p>", unsafe_allow_html=True)
                    
                    if st.button("TAK (PRAWDA)", use_container_width=True):
                        state["status"] = "result"; state["buyout_msg"] = "PRAWDA ZAAKCEPTOWANA ✅"; st.rerun()
                    
                    if st.button("NIE (WYKUPNE / KARA)", use_container_width=True):
                        state["status"] = "decision"; st.rerun()
            
            elif state["status"] == "decision":
                refusals = state["ona_refusals"] if who_val == "ONA" else state["on_refusals"]
                b_type, b_label = get_buyout_info(refusals)
                
                st.markdown(f"<h2 style='text-align:center; color:#ff4b4b;'>Wybór {sedzia_imie}:</h2>", unsafe_allow_html=True)
                
                if b_type != "MANDATORY":
                    if st.button(f"UŻYJ: {b_label}", use_container_width=True):
                        if who_val == "ONA": state["ona_refusals"] += 1
                        else: state["on_refusals"] += 1
                        state["status"] = "result"; state["buyout_msg"] = f"WYKUPIONE: {b_label}"; st.rerun()
                
                if st.button("WYKONUJĘ KARĘ 😈", use_container_width=True):
                    state["status"] = "result"; state["penalty"] = wylosuj_kare(q_idx, len(state["gra"])); state["buyout_msg"] = ""; st.rerun()

            else:
                if st.button("NASTĘPNE PYTANIE ➔", use_container_width=True):
                    state["current_q"] += 1
                    state["status"] = "question"
                    state["buyout_msg"] = ""
                    state["penalty"] = ""
                    st.rerun()
        
        if st.button("RESET GRY"):
            state["phase"] = "intro"
            state["intro_q"] = 0
            state["intro_gra"] = generuj_intro()
            state["gra"] = generuj_gre()
            state["current_q"] = 0
            state["status"] = "question"
            state["ona_refusals"] = 0
            state["on_refusals"] = 0
            state["penalty"] = ""
            state["buyout_msg"] = ""
            st.rerun()
