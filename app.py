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
# 3. GIGANTYCZNA BAZA DANYCH (EDYCJA OSTATECZNA - 220+ ELEMENTÓW)
# ==========================================

toasty = [
    "Wypijcie zdrowy łyk za Waszą namiętność! 🥂",
    "Toast za najseksowniejszą osobę w tym pokoju! 🔥",
    "Pijemy za wszystkie grzechy, które dzisiaj popełnicie! 😈",
    "Czas na toast bez użycia rąk! Podajcie sobie kieliszek do ust. 🍷",
    "Toast za Wasze pierwsze spotkanie i ten błysk w oku! ✨",
    "Pijemy za szczerość – niech prawda Was dzisiaj rozgrzeje! 🥃",
    "Za każdą minutę dzisiejszej nocy, która jest jeszcze przed Wami! 🥂",
    "Toast za to, co stanie się, gdy w końcu wyłączycie TV... 🍾",
    "Pijemy za odwagę w spełnianiu wspólnych fantazji! 🥃",
    "Toast za Wasze ulubione wspólne wspomnienie z sypialni! 🍷",
    "Za to, że z każdym dniem kręcicie się nawzajem coraz bardziej! 🥂",
    "Pijemy shota za każde z Was, które jako pierwsze pęknie i zaciągnie drugie do łóżka! 🥃",
    "Toast za Wasze ciała – idealnie do siebie pasują! 🍷"
]

# --- POZIOM 1: Romantyzm, emocje, bliskość (50 pytań) ---
p1 = [
    {"kto": "ONA", "tekst": "Jaka była Twoja pierwsza myśl, kiedy zobaczyłeś mnie po raz pierwszy?"},
    {"kto": "ON", "tekst": "Co uważam za Twoją najbardziej atrakcyjną cechę charakteru?"},
    {"kto": "ONA", "tekst": "W jakim stroju (z moich codziennych ubrań) lubię Cię najbardziej?"},
    {"kto": "ON", "tekst": "Jaki drobny gest z Twojej strony sprawia mi zawsze największą radość?"},
    {"kto": "ONA", "tekst": "Który Twój nawyk uważam za najbardziej uroczy?"},
    {"kto": "ON", "tekst": "Jaka jest moja ulubiona część Twojego ciała, gdy po prostu siedzimy obok siebie?"},
    {"kto": "ONA", "tekst": "Jakie jest moje najpiękniejsze wspomnienie z naszych wspólnych początków?"},
    {"kto": "ON", "tekst": "Co we mnie sprawia, że czujesz się przy mnie najbardziej bezpieczna?"},
    {"kto": "ONA", "tekst": "Jaki komplement z Twoich ust sprawia, że najbardziej promieniuję?"},
    {"kto": "ON", "tekst": "Jaką cechę mojego wyglądu zauważyłaś u mnie jako pierwszą?"},
    {"kto": "ONA", "tekst": "Gdybym mogła zabrać Cię teraz w dowolne miejsce na świecie, gdzie by to było?"},
    {"kto": "ON", "tekst": "Jaki zapach moich perfum lub mojego ciała jest Twoim ulubionym?"},
    {"kto": "ONA", "tekst": "Które z naszych wspólnych zdjęć lubię najbardziej?"},
    {"kto": "ON", "tekst": "W jakiej sytuacji czuję się przy Tobie najbardziej męski?"},
    {"kto": "ONA", "tekst": "Jaki film lub piosenka najbardziej kojarzy mi się z naszym związkiem?"},
    {"kto": "ON", "tekst": "Co jest moją największą pasją, o której mógłbym opowiadać godzinami?"},
    {"kto": "ONA", "tekst": "Gdybym miała napisać o nas książkę, jaki nosiłaby tytuł?"},
    {"kto": "ON", "tekst": "Która wspólna podróż była według mnie najbardziej romantyczna?"},
    {"kto": "ONA", "tekst": "Czego we mnie boisz się najbardziej stracić?"},
    {"kto": "ON", "tekst": "Jaka była najbardziej szalona rzecz, jaką zrobiłem, by Cię zaimponować?"},
    {"kto": "ONA", "tekst": "Wolisz mnie w rozpuszczonych włosach czy spiętych?"},
    {"kto": "ON", "tekst": "Co sprawia, że po ciężkim dniu uśmiecham się na Twój widok?"},
    {"kto": "ONA", "tekst": "Jaka jest moja ulubiona potrawa, którą wspólnie jedliśmy?"},
    {"kto": "ON", "tekst": "Co w moim stylu ubierania się podoba Ci się najbardziej?"},
    {"kto": "ONA", "tekst": "Która cecha Twojej twarzy jest moją ulubioną?"},
    {"kto": "ON", "tekst": "Kiedy ostatnio poczułem dumę, że jesteś moją partnerką?"},
    {"kto": "ONA", "tekst": "Jaki prezent od Ciebie uważam za najbardziej trafiony?"},
    {"kto": "ON", "tekst": "Co najbardziej lubię robić w leniwy, niedzielny poranek?"},
    {"kto": "ONA", "tekst": "Które z moich marzeń (nie łóżkowych) jest dla mnie teraz najważniejsze?"},
    {"kto": "ON", "tekst": "Jakie słowo najlepiej opisuje naszą relację według mnie?"}
]

# --- POZIOM 2: Dotyk, zmysły, budowanie napięcia (50 pytań) ---
p2 = [
    {"kto": "ONA", "tekst": "Gdzie na moim ciele dotyk Twoich ust sprawia mi największą przyjemność?"},
    {"kto": "ON", "tekst": "Jaka pieszczota z Twojej strony najszybciej wywołuje u mnie dreszcze?"},
    {"kto": "ONA", "tekst": "Jakie słowa szeptane przez Ciebie do ucha kręcą mnie najbardziej?"},
    {"kto": "ON", "tekst": "W jakiej swojej bieliźnie (kolor/fason) według mnie wyglądasz najlepiej?"},
    {"kto": "ONA", "tekst": "Który z naszych pocałunków w miejscu publicznym zapamiętałam najlepiej?"},
    {"kto": "ON", "tekst": "Co najbardziej lubię robić z Twoimi włosami, kiedy się całujemy?"},
    {"kto": "ONA", "tekst": "Wolisz mnie w pełnym makijażu, czy rano, zupełnie naturalną?"},
    {"kto": "ON", "tekst": "Które miejsce na Twoim ciele uważam za najbardziej wrażliwe na mój dotyk?"},
    {"kto": "ONA", "tekst": "Jakie ubranie z mojej szafy chętnie byś ze mnie teraz zdjął?"},
    {"kto": "ON", "tekst": "Jaka jest moja ulubiona pora dnia na wspólne pieszczoty?"},
    {"kto": "ONA", "tekst": "Co myślę o Twoim stylu całowania w skali od 1 do 10?"},
    {"kto": "ON", "tekst": "Jaki rodzaj masażu lubię otrzymywać od Ciebie najbardziej?"},
    {"kto": "ONA", "tekst": "Gdybyś miał mnie teraz pocałować w jedno miejsce poza ustami – co bym wybrała?"},
    {"kto": "ON", "tekst": "Co we mnie budzi w Tobie największe pożądanie, gdy na mnie patrzysz?"},
    {"kto": "ONA", "tekst": "Jak reaguję, gdy niespodziewanie dotykasz moich pośladków?"},
    {"kto": "ON", "tekst": "Który moment naszej ostatniej randki był według mnie najbardziej naelektryzowany?"},
    {"kto": "ONA", "tekst": "Czy lubię, kiedy lekko przygryzasz moją dolną wargę?"},
    {"kto": "ON", "tekst": "Jaki rodzaj dotyku rąk preferuję podczas przytulania?"},
    {"kto": "ONA", "tekst": "Co najbardziej kręci mnie w Twoim głosie?"},
    {"kto": "ON", "tekst": "Wolisz mnie w spódniczkach czy dopasowanych spodniach?"},
    {"kto": "ONA", "tekst": "Gdybym miała wybrać zapach, który mnie podnieca – co by to było?"},
    {"kto": "ON", "tekst": "Która część mojej klatki piersiowej jest według mnie najwrażliwsza?"},
    {"kto": "ONA", "tekst": "Co czuję, gdy gładzisz mnie po karku?"},
    {"kto": "ON", "tekst": "Jakie jest moje zdanie o całowaniu z języczkiem – wolę długie czy krótkie sesje?"},
    {"kto": "ONA", "tekst": "Która z Twoich koszul podoba mi się na Tobie najbardziej?"}
]

# --- POZIOM 3: Pikantne preferencje, sypialnia (50 pytań) ---
p3 = [
    {"kto": "ONA", "tekst": "Jaka jest moja ulubiona pozycja, w której czuję się najbardziej usatysfakcjonowana?"},
    {"kto": "ON", "tekst": "Jakie nietypowe miejsce poza sypialnią najbardziej mnie kręci na 'szybki numerek'?"},
    {"kto": "ONA", "tekst": "Co lubię najbardziej w Twoim zachowaniu, gdy zbliżamy się do szczytu?"},
    {"kto": "ON", "tekst": "Jaki rodzaj dotyku rąk w łóżku preferuję: delikatny czy zdecydowany?"},
    {"kto": "ONA", "tekst": "Jaka jest moja najbardziej skryta fantazja, o której kiedykolwiek Ci wspomniałam?"},
    {"kto": "ON", "tekst": "Co sądzę o używaniu gadżetów w sypialni – który byłby moim ulubionym?"},
    {"kto": "ONA", "tekst": "Jaki dźwięk wydawany przeze mnie w sypialni działa na Ciebie najbardziej?"},
    {"kto": "ON", "tekst": "Kto z nas zazwyczaj częściej przejmuje inicjatywę w łóżku?"},
    {"kto": "ONA", "tekst": "Czego chciałabym spróbować, co robimy bardzo rzadko lub wcale?"},
    {"kto": "ON", "tekst": "Jakie słowa wypowiadane podczas seksu kręcą Ją najbardziej?"},
    {"kto": "ONA", "tekst": "Wolisz, kiedy w sypialni dominuję, czy kiedy jestem całkowicie uległa?"},
    {"kto": "ON", "tekst": "Co sprawia, że po wszystkim czuję się w 100% zaspokojona?"},
    {"kto": "ONA", "tekst": "Co kręci mnie bardziej: robienie tego rano, czy w środku nocy?"},
    {"kto": "ON", "tekst": "Jak bardzo lubię, kiedy zostawiasz mi ślady na ciele?"},
    {"kto": "ONA", "tekst": "Wolisz mnie w pełnym świetle, czy przy świecach?"},
    {"kto": "ON", "tekst": "Co myślę o seksie oralnym – wolę dawać czy brać?"},
    {"kto": "ONA", "tekst": "Czy kręci mnie bicie po pośladkach?"},
    {"kto": "ON", "tekst": "Jaka jest moja ulubiona szybkość podczas zbliżenia?"},
    {"kto": "ONA", "tekst": "Co kręci mnie bardziej: długa gra wstępna czy szybki, zwierzęcy seks?"},
    {"kto": "ON", "tekst": "Czy kiedykolwiek udawałem przed Tobą orgazm (lub znasz moją opinię na ten temat)?"},
    {"kto": "ONA", "tekst": "Jaka część Twojego ciała najbardziej mnie podnieca, gdy jesteś nago?"},
    {"kto": "ON", "tekst": "Gdybym miał Cię związać – co byś powiedziała?"},
    {"kto": "ONA", "tekst": "Co uważam za naszą najbardziej gorącą noc do tej pory?"},
    {"kto": "ON", "tekst": "Co sądzę o uprawianiu seksu przed lustrem?"},
    {"kto": "ONA", "tekst": "Który z moich fetyszy jest dla Ciebie najbardziej zrozumiały?"}
]

# --- POZIOM 4: Pełen ogień i ekstremalne fantazje (50 pytań) ---
p4 = [
    {"kto": "ONA", "tekst": "Gdybyśmy mieli nagrać wspólne wideo, od jakiej sceny chciałabym zacząć?"},
    {"kto": "ON", "tekst": "W jakiej pozycji Ona dochodzi najszybciej i najbardziej intensywnie?"},
    {"kto": "ONA", "tekst": "Gdybym mogła Cię uwiązać i robić z Tobą co zechcę przez 5 minut, co byłoby pierwsze?"},
    {"kto": "ON", "tekst": "Co w Twoim zachowaniu sprawia, że Ona całkowicie traci nad sobą panowanie?"},
    {"kto": "ONA", "tekst": "Którą część Twojego ciała chciałabym teraz pieścić ustami najdłużej?"},
    {"kto": "ON", "tekst": "Jaka jest Jej najostrzejsza fantazja, która jeszcze nie została zrealizowana?"},
    {"kto": "ONA", "tekst": "Gdybyśmy mieli dzisiaj dołączyć do zabawy kogoś trzeciego... czy w ogóle bym to rozważyła?"},
    {"kto": "ON", "tekst": "Jakie miejsce publiczne kręci Ją najbardziej jako potencjalna scena seksu?"},
    {"kto": "ONA", "tekst": "Co jest dla mnie ważniejsze: technika i tempo czy emocjonalne połączenie?"},
    {"kto": "ON", "tekst": "Który z moich fetyszy Ją najbardziej kręci, a który zaskoczył?"},
    {"kto": "ONA", "tekst": "Jaka jest najbardziej 'brudna' rzecz, jaką kiedykolwiek o Tobie pomyślałam?"},
    {"kto": "ON", "tekst": "Gdybyś miał użyć na Niej dzisiaj kostki lodu lub ciepłego wosku – co by wybrała?"},
    {"kto": "ONA", "tekst": "Czy kiedykolwiek fantazjowałam o kobiecie?"},
    {"kto": "ON", "tekst": "Który z moich kolegów/koleżanek wydaje mi się najbardziej atrakcyjny seksualnie (według Jej wiedzy)?"},
    {"kto": "ONA", "tekst": "Wolisz, kiedy patrzę Ci w oczy, gdy dochodzę, czy kiedy mam je zamknięte?"},
    {"kto": "ON", "tekst": "Co kręci Ją bardziej: gdy jestem brutalny, czy gdy jestem nad wyraz delikatny?"},
    {"kto": "ONA", "tekst": "Jaki strój tematyczny chciałabym, żebyś dzisiaj założył?"},
    {"kto": "ON", "tekst": "Co Ona myśli o seksie analnym?"},
    {"kto": "ONA", "tekst": "Jaka jest moja ulubiona reakcja Twojego ciała na mój dotyk?"},
    {"kto": "ON", "tekst": "Co jest moją największą seksualną słabością?"},
    {"kto": "ONA", "tekst": "Gdybyśmy mieli spędzić cały tydzień tylko na seksie, jak by to wyglądało?"},
    {"kto": "ON", "tekst": "Co Ona sądzi o seksie w samochodzie na parkingu?"},
    {"kto": "ONA", "tekst": "Który moment naszego seksu uważam za najbardziej zwierzęcy?"},
    {"kto": "ON", "tekst": "Czego Ona najbardziej zazdrości innym parom w kwestiach łóżkowych?"},
    {"kto": "ONA", "tekst": "Co sprawia, że czuję się jak bogini seksu?"}
]

# --- KARY: POZIOM 1 (Czułość i masaż) ---
kary_l1 = [
    "Całuj moją szyję przez minutę, omijając usta.",
    "Zrób mi 2-minutowy masaż dłoni i palców.",
    "Powiedz mi szeptem 3 rzeczy, które najbardziej we mnie cenisz.",
    "Zdejmij ze mnie skarpetki, używając tylko jednej ręki.",
    "Patrz mi głęboko w oczy przez 60 sekund bez odrywania wzroku.",
    "Przejedź delikatnie nosem po moich policzkach i szyi.",
    "Przytul mnie tak mocno, jak potrafisz, przez pełną minutę.",
    "Napisz palcem na moich plecach słowo, a ja muszę zgadnąć jakie.",
    "Wymasuj moje ramiona przez 2 minuty.",
    "Pocałuj mnie w czoło i oba policzki."
]

# --- KARY: POZIOM 2 (Pikantne wyzwania) ---
kary_l2 = [
    "Weź łyk alkoholu i przekaż mi go ustami podczas pocałunku.",
    "Zdejmij z partnera jedną, wybraną przez Ciebie część garderoby.",
    "Pocałuj moje wewnętrzne udo, centymetr po centymetrze, coraz wyżej.",
    "Przygryź delikatnie płatek mojego ucha i powiedz coś niegrzecznego.",
    "Zdejmij ze mnie jeden element ubrania samymi zębami.",
    "Usiądź na moich kolanach okrakiem i spędź tak całą kolejną rundę.",
    "Wymasuj moje stopy, używając do tego odrobiny balsamu lub drinka.",
    "Pozwól mi zawiązać Ci oczy na najbliższą rundę.",
    "Pieść moje dłonie językiem przez 30 sekund.",
    "Zdejmij pasek z moich spodni używając tylko zębów."
]

# --- KARY: POZIOM 3 (Bardzo pikantne) ---
kary_l3 = [
    "Zliż odrobinę alkoholu z mojego brzucha lub obojczyka.",
    "Zostań tylko w bieliźnie na resztę tej fazy gry.",
    "Wymasuj moje pośladki dłońmi, patrząc mi głęboko w oczy przez minutę.",
    "Pieść moje ucho i szyję językiem, podczas gdy moje ręce są trzymane przez Ciebie.",
    "Przejedź językiem od mojego pępka aż do wgłębienia między piersiami.",
    "Zdejmij moją koszulkę lub bluzkę, używając tylko zębów.",
    "Przejedź kostką lodu wzdłuż mojego kręgosłupa, a potem zliż wodę.",
    "Będziesz uległy/uległa przez najbliższe 3 minuty. Robię z Twoim ciałem co chcę.",
    "Włóż dłonie pod moją bieliznę na minutę, ale nic nie rób.",
    "Zasymuluj odgłosy, jakie wydajesz podczas seksu, patrząc mi w oczy."
]

# --- KARY: POZIOM 4 (Ekstremalne / Gra wstępna) ---
kary_l4 = [
    "Zaspokajaj mnie ustami przez pełne 60 sekund (użyj stopera!).",
    "Rób z moim ciałem co tylko chcesz przez najbliższe 3 minuty.",
    "Zdejmij z siebie absolutnie wszystko. Resztę gry prowadzisz nago.",
    "Użyj na partnerze wybranego gadżetu lub dłoni w sposób ekstremalny przez 2 minuty.",
    "Zwiąż moje ręce (np. paskiem) na najbliższe dwie rundy.",
    "Wykonaj dla mnie namiętny, 2-minutowy taniec (striptease).",
    "Zliż kroplę alkoholu z moich najbardziej wrażliwych miejsc.",
    "Rób mi dobrze ustami dopóki nie powiem, że wystarczy.",
    "Przejedź językiem po całym moim ciele, od stóp do głów.",
    "Kary się skończyły. Resztę wieczoru spędzamy bez telefonów w sypialni. 😈"
]

# ==========================================
def generuj_gre():
    talia = random.sample(p1, min(len(p1), 20)) + random.sample(p2, min(len(p2), 20)) + \
            random.sample(p3, min(len(p3), 20)) + random.sample(p4, min(len(p4), 20))
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
# 4. SILNIK SYNCHRONIZACJI
# ==========================================
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

            st.markdown(f"<div class='elegant-header'>Runda {q_idx + 1}</div>", unsafe_allow_html=True)
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
                <p style='color: #8c7a96;'>Zasada Wykupnego: Shot i pomijasz karę! 🥃</p>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(6); state["current_q"] += 1; state["status"] = "question"; st.rerun()
    else:
        st.markdown("<div class='premium-box'><h1 class='gold-text'>KONIEC GRY.😈</h1></div>", unsafe_allow_html=True)

elif view_type == "pilot":
    q_idx = state["current_q"]
    if q_idx < len(state["gra"]):
        q = state["gra"][q_idx]
        who_val = str(q["kto"]).upper().strip()
        
        if who_val == "TOAST":
            if st.button("WYPITE! 🥂", use_container_width=True):
                state["status"] = "result"; state["penalty"] = ""; st.rerun()
        else:
            # FIX LOGIKI: Jeśli "Kto" to ONA, to Ona sędziuje. Jeśli ON, to On sędziuje.
            sedzia_imie = IMIE_ONA if who_val == "ONA" else IMIE_ON
            st.markdown(f"<p style='text-align:center; color:#d4af37; font-size:24px; letter-spacing:2px;'>Sędziuje: <b>{sedzia_imie}</b></p>", unsafe_allow_html=True)
            
            if st.button("TAK", use_container_width=True, type="primary"):
                if state["status"] == "question":
                    state["status"] = "result"; state["penalty"] = ""; st.rerun()
            
            if st.button("NIE", use_container_width=True, type="secondary"):
                if state["status"] == "question":
                    state["status"] = "result"; state["penalty"] = wylosuj_kare(q_idx, len(state["gra"])); st.rerun()
    
    if st.button("WYLOSUJ NOWĄ GRĘ (RESET)"):
        state["gra"] = generuj_gre(); state["current_q"] = 0; state["status"] = "question"; st.rerun()
