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
# 2. GŁÓWNY CSS (LUKSUSOWY PREMIUM GOLD + PILOT)
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

    /* PUDEŁKA TV */
    .premium-box {
        background: linear-gradient(145deg, #15101c, #0d0a13);
        border: 1px solid #2a2035; border-radius: 25px;
        padding: 60px 40px; box-shadow: 0 30px 60px rgba(0, 0, 0, 0.8);
        text-align: center; margin: 20px auto; max-width: 1000px;
    }
    /* PUDEŁKA PILOTA (Wersja Mobile) */
    .pilot-box {
        background: linear-gradient(145deg, #15101c, #0d0a13);
        border: 1px solid #2a2035; border-radius: 20px;
        padding: 30px 20px; box-shadow: 0 15px 30px rgba(0, 0, 0, 0.8);
        text-align: center; margin: 10px auto 20px auto; max-width: 600px;
    }

    .gold-text {
        font-size: 54px; font-weight: 300; color: #d4af37; 
        text-shadow: 0 4px 20px rgba(212, 175, 55, 0.3); line-height: 1.4;
    }
    .elegant-header {
        color: #8c7a96; font-size: 16px; text-transform: uppercase;
        letter-spacing: 6px; text-align: center; margin-bottom: 10px;
    }
    .turn-badge {
        display: inline-block; padding: 8px 24px; border-radius: 30px;
        font-size: 18px; font-weight: bold; letter-spacing: 3px;
        margin-bottom: 20px; text-transform: uppercase; box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    .turn-ona { background-color: rgba(212, 175, 55, 0.1); border: 1px solid #d4af37; color: #d4af37; text-shadow: 0 0 10px rgba(212,175,55,0.5); }
    .turn-on { background-color: rgba(140, 122, 150, 0.1); border: 1px solid #8c7a96; color: #8c7a96; text-shadow: 0 0 10px rgba(140,122,150,0.5); }
    .turn-toast { background-color: rgba(255, 75, 75, 0.1); border: 1px solid #ff4b4b; color: #ff4b4b; text-shadow: 0 0 10px rgba(255,75,75,0.5); }
    .turn-intro { background-color: rgba(75, 214, 123, 0.1); border: 1px solid #4bd67b; color: #4bd67b; text-shadow: 0 0 10px rgba(75,214,123,0.5); }
    
    /* LISTA ZASAD NA TV */
    .rules-list { text-align: left; margin-top: 30px; display: inline-block; max-width: 800px;}
    .rules-item { font-size: 20px; margin-bottom: 15px; color: #e0d8d3; line-height: 1.5; }
    .rules-item strong { color: #d4af37; letter-spacing: 1px; }
    
    /* PASEK NAPIĘCIA */
    .tension-container {
        width: 100%; background: #1a1225; border-radius: 10px; 
        border: 1px solid #2a2035; height: 30px; margin: 20px 0; overflow: hidden;
    }
    .tension-bar {
        height: 100%; background: linear-gradient(90deg, #d4af37, #ff4b4b);
        transition: width 0.5s ease-in-out;
    }
    .tension-text { color: #ff4b4b; font-weight: bold; letter-spacing: 2px; font-size: 14px; margin-top: 5px; }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
    
    /* PANEL STATYSTYK TV */
    .stats-container { display: flex; justify-content: space-around; max-width: 1000px; margin: 0 auto; }
    .stat-card {
        background: rgba(21, 16, 28, 0.6); padding: 15px 30px; border-radius: 20px;
        border: 1px solid #2a2035; text-align: center; min-width: 200px;
    }
    .stat-name { color: #8c7a96; font-size: 14px; letter-spacing: 2px; margin-bottom: 5px; }
    .stat-lives { color: #d4af37; font-size: 24px; font-weight: bold; }

    /* PRZYCISKI PILOTA - POZYTYWNE / POTWIERDZAJĄCE (ZIELONE) */
    button[data-testid="baseButton-primary"] {
        height: 12vh !important; width: 100% !important;
        border-radius: 20px !important; margin-top: 1vh !important;
        background: linear-gradient(145deg, #112217, #0a120e) !important;
        border: 1px solid #4bd67b !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5) !important;
    }
    button[data-testid="baseButton-primary"] p { 
        font-size: 24px !important; font-weight: 300 !important; letter-spacing: 2px; color: #4bd67b !important; 
    }

    /* PRZYCISKI PILOTA - NEGATYWNE / KARY / STANDARDOWE (ZŁOTE) */
    button[data-testid="baseButton-secondary"] {
        height: 12vh !important; width: 100% !important;
        border-radius: 20px !important; margin-top: 1vh !important;
        background: linear-gradient(145deg, #1a1323, #0d0a13) !important;
        border: 1px solid #d4af37 !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5) !important;
    }
    button[data-testid="baseButton-secondary"] p { 
        font-size: 24px !important; font-weight: 300 !important; letter-spacing: 2px; color: #d4af37 !important; 
    }

    /* PRZYCISK RESETU NA SAMYM DOLE */
    div.stButton:last-of-type > button {
        height: 50px !important; background-color: transparent !important;
        border: 1px solid #2a2035 !important; box-shadow: none !important; margin-top: 30px !important;
    }
    div.stButton:last-of-type > button p { font-size: 14px !important; color: #8c7a96 !important; letter-spacing: 1px;}

    div[data-testid="stLinkButton"] > a {
        background: linear-gradient(145deg, #1a1323, #0d0a13) !important;
        border: 1px solid #d4af37 !important; color: #d4af37 !important;
        border-radius: 20px !important; padding: 25px !important;
        font-size: 24px !important; text-align: center !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# ==========================================
# 3. BAZA DANYCH (NOWY SEZON - CAŁKOWICIE NOWE PYTANIA I KARY 🔥)
# ==========================================

pytania_intro = [
    {"kto": "ONA", "tekst": "Zgadnij, jaki był mój pierwszy sen o nas, który pamiętam?"},
    {"kto": "ON", "tekst": "Jak myślisz, co pomyślałem sobie po naszej pierwszej, poważnej rozmowie?"},
    {"kto": "ONA", "tekst": "Zgadnij, jaka Twoja drobna wada z czasem stała się dla mnie urocza?"},
    {"kto": "ON", "tekst": "Jak myślisz, w jakich momentach najbardziej boję się, że Cię zawiodę?"},
    {"kto": "ONA", "tekst": "Gdybym mogła spędzić z Tobą jeden dzień z naszej przeszłości jeszcze raz, co by to było?"},
    {"kto": "ON", "tekst": "Zgadnij, co we mnie najbardziej się zmieniło pod Twoim wpływem?"},
    {"kto": "ONA", "tekst": "Jak myślisz, za co najczęściej dziękuję w myślach, gdy na Ciebie patrzę?"},
    {"kto": "ON", "tekst": "Zgadnij, co jest moim ulubionym sposobem na spędzanie z Tobą deszczowego popołudnia?"},
    {"kto": "ONA", "tekst": "Czy według mnie nasz związek potrzebuje więcej spontaniczności, czy rutyny?"},
    {"kto": "ON", "tekst": "Jak myślisz, jaki Twój gest najszybciej potrafi rozładować moje napięcie po pracy?"},
    {"kto": "ONA", "tekst": "Zgadnij, co uważam za nasz najbardziej 'filmowy' moment w całej relacji?"},
    {"kto": "ON", "tekst": "Gdybym miał Cię opisać komuś w trzech słowach, zgadnij, jakie to by były słowa?"},
    {"kto": "ONA", "tekst": "Jak myślisz, czego najbardziej nie lubię robić w domu, a co Ty robisz za mnie?"},
    {"kto": "ON", "tekst": "Zgadnij, jaki był mój ulubiony komplement, który kiedykolwiek od Ciebie usłyszałem?"},
    {"kto": "ONA", "tekst": "Gdybyśmy mieli rzucić wszystko i wyjechać, jaki kraj według mnie byłby dla nas idealny?"},
    {"kto": "ON", "tekst": "Zgadnij, czy wolę, gdy prowadzisz długie monologi, czy gdy to ja mówię, a Ty słuchasz?"},
    {"kto": "ONA", "tekst": "Jak myślisz, w jakiej sytuacji byłam z Ciebie najbardziej dumna przy innych ludziach?"},
    {"kto": "ON", "tekst": "Zgadnij, o czym marzę dla nas w perspektywie najbliższych 5 lat?"},
    {"kto": "ONA", "tekst": "Gdybym miała napisać o Tobie książkę, jaki nosiłaby tytuł?"},
    {"kto": "ON", "tekst": "Jak myślisz, czy według mnie jesteś bardziej duszą towarzystwa, czy domatorką?"},
    {"kto": "ONA", "tekst": "Zgadnij, w jaki sposób najłatwiej jest Ci mnie udobruchać po kłótni?"},
    {"kto": "ON", "tekst": "Czy według mnie to my uratowaliśmy siebie nawzajem, czy po prostu mieliśmy szczęście?"},
    {"kto": "ONA", "tekst": "Zgadnij, jaki Twój nawyk z poranków lubię obserwować w ciszy?"},
    {"kto": "ON", "tekst": "Jak myślisz, z kim z Twojej rodziny/znajomych czuję się najbardziej komfortowo?"},
    {"kto": "ONA", "tekst": "Zgadnij, jakiego mojego marzenia jeszcze nie znasz, a jest dla mnie ważne?"},
    {"kto": "ON", "tekst": "Czy według mnie potrafisz mnie zmotywować do działania lepiej niż ktokolwiek inny?"},
    {"kto": "ONA", "tekst": "Zgadnij, w którym momencie dnia lubię pisać do Ciebie wiadomości najbardziej?"},
    {"kto": "ON", "tekst": "Jak myślisz, o jakiej naszej wspólnej przygodzie najchętniej opowiadam znajomym?"},
    {"kto": "ONA", "tekst": "Gdybym mogła ugotować dla Ciebie tylko jedno danie do końca życia, co byś chciał, żebym wybrała?"},
    {"kto": "ON", "tekst": "Zgadnij, czy częściej patrzę na Twoje oczy, czy na usta, gdy z Tobą rozmawiam?"}
]

toasty = [
    "WYZWANIE: Kto ma teraz ciemniejszą bieliznę (lub nie ma jej wcale), rozdaje jednego shota karniaka! 🥃",
    "POJEDYNEK: Powiecie na głos na '3-4' swoje ulubione pozycje. Kto się zawaha, pije! 👀",
    "WODOSPAD: Odpowiadający zaczyna pić. Sędzia pije tak długo, jak długo odpowiadający nie odstawi kieliszka! 💦",
    "WYZWANIE: Wypijcie shota ze skrzyżowanymi rękami (bruderszaft), nie odrywając od siebie wzroku! 🍷",
    "ZADANIE: Sędzia nalewa alkohol do swoich ust i powoli przelewa go partnerowi. 💋",
    "POJEDYNEK: Szybkie całowanie. Kto pierwszy użyje języka, przegrywa i pije! ⚡",
    "WYZWANIE: Kto w tym związku ma mocniejszą głowę? Ta osoba pije teraz podwójnie! 🥂",
    "ZADANIE: Oboje zamykacie oczy, bierzecie kieliszki i pijecie. Kto pierwszy otworzy oczy, pije jeszcze raz. 🍾",
    "ZADANIE: Upuść kroplę napoju na udo partnera i zliż ją bez użycia rąk. 😈",
    "WYZWANIE: Sędzia mówi jedno brudne słowo. Druga osoba musi wypić shota bez żadnej mimiki twarzy. 🔥",
    "POJEDYNEK ROZBIERANY: Kto pierwszy zdejmie z siebie cokolwiek (nawet zegarek), ratuje się przed shotem! ✂️",
    "ZADANIE: Pijecie shota, trzymając się za ręce pod stołem. 🤫",
    "WYZWANIE: Zamieniacie się miejscami na kanapie, a podczas mijania wypijacie zdrowie za dzisiejszą noc! 🥂"
]

p1 = [
    {"kto": "ONA", "tekst": "Zgadnij, co czuję, gdy nagle łapiesz mnie mocno za rękę w miejscu publicznym?"},
    {"kto": "ON", "tekst": "Jak myślisz, w jakim kolorze bielizny u Ciebie najszybciej tracę zdrowy rozsądek?"},
    {"kto": "ONA", "tekst": "Wybierz: czy JA wolę, gdy niespodziewanie całujesz mnie w kark, czy w czoło?"},
    {"kto": "ON", "tekst": "Czy według MNIE lepsze jest długie, leniwe przytulanie, czy szybki, zaborczy dotyk?"},
    {"kto": "ONA", "tekst": "Jak myślisz, co pomyślałam, gdy pierwszy raz zobaczyłam Cię w garniturze/koszuli?"},
    {"kto": "ON", "tekst": "Co według MNIE najbardziej wyróżnia Twój zapach spośród innych?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy kręci mnie, gdy pokazujesz swoją siłę fizyczną na co dzień?"},
    {"kto": "ON", "tekst": "Gdybym miał opisać Twoje usta komuś innemu, jakich słów bym użył?"},
    {"kto": "ONA", "tekst": "Jak myślisz, co uwielbiam w sposobie, w jaki na mnie patrzysz, gdy myślę, że nie widzisz?"},
    {"kto": "ON", "tekst": "Zgadnij, czy wolałbym zasypiać z Twoją głową na mojej piersi, czy obejmując Cię od tyłu?"},
    {"kto": "ONA", "tekst": "Jak myślisz, w której z moich sukienek czuję się najbardziej atrakcyjna dla Ciebie?"},
    {"kto": "ON", "tekst": "Zgadnij, w jakim domowym stroju wyglądasz dla mnie najbardziej 'do schrupania'?"},
    {"kto": "ONA", "tekst": "Wybierz: czy JA wolę być prowadzona za rękę, czy w obejęciu za talię?"},
    {"kto": "ON", "tekst": "Jak myślisz, co czuję, gdy podczas jazdy samochodem kładziesz dłoń na moim udzie?"},
    {"kto": "ONA", "tekst": "Zgadnij, jak szybko bije mi serce, gdy szepczesz mi coś do ucha w towarzystwie?"},
    {"kto": "ON", "tekst": "Czy według MNIE nasz pierwszy pocałunek był wyreżyserowany, czy 100% spontaniczny?"},
    {"kto": "ONA", "tekst": "Zgadnij, co w Twoich dłoniach daje mi największe poczucie bezpieczeństwa i pożądania?"},
    {"kto": "ON", "tekst": "Jak myślisz, z jakiej części mojego ciała jestem najbardziej dumny w sypialni?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy podnieca MNIE myśl, że o mnie fantazjujesz, gdy jesteśmy osobno w pracy?"},
    {"kto": "ON", "tekst": "Co sprawia, że JA najszybciej robię się o Ciebie zazdrosny, nawet jeśli tego nie pokazuję?"},
    {"kto": "ONA", "tekst": "Jak myślisz, czy kręcą mnie faceci w mundurach/garniturach, czy preferuję Twój luźny styl?"},
    {"kto": "ON", "tekst": "Zgadnij, czy wolę, gdy to Ty robisz pierwszy krok wieczorem, czy wolisz, żebym to był ja?"},
    {"kto": "ONA", "tekst": "Co we mnie płonie, gdy widzę, jak radzisz sobie z trudną, męską sytuacją (np. naprawa czegoś, asertywność)?"},
    {"kto": "ON", "tekst": "Zgadnij, jak reaguję w myślach, gdy nakładasz na usta czerwoną szminkę przed wyjściem?"},
    {"kto": "ONA", "tekst": "Jak myślisz, czy wolałabym dostawać od Ciebie rano kawę do łóżka, czy pikantnego SMS-a?"},
    {"kto": "ON", "tekst": "Co JA czuję, gdy z premedytacją zostawiasz mi w łazience swoją seksowną bieliznę na widoku?"},
    {"kto": "ONA", "tekst": "Zgadnij, co sobie myślę, gdy po wyjściu spod prysznica chodzisz po domu tylko w ręczniku?"},
    {"kto": "ON", "tekst": "Jak myślisz, czy kręci MNIE, gdy publicznie, niby przypadkiem, dotykasz moich włosów?"},
    {"kto": "ONA", "tekst": "Zgadnij, z jakiego miejsca na Twoim ciele najchętniej zlizywałabym słodki deser?"},
    {"kto": "ON", "tekst": "Co w Twoim sposobie chodzenia sprawia, że nie mogę oderwać od Ciebie wzroku?"}
]

p2 = [
    {"kto": "ONA", "tekst": "Zgadnij, w którym momencie gry wstępnej zaczynam tracić całkowitą kontrolę nad oddechem?"},
    {"kto": "ON", "tekst": "Jak myślisz, które miejsce na moich plecach jest najbardziej wrażliwe na Twój dotyk?"},
    {"kto": "ONA", "tekst": "Zgadnij, co JA wolę: długie i bardzo powolne rozbieranie mnie, czy gwałtowne zrzucenie ubrań?"},
    {"kto": "ON", "tekst": "Jak myślisz, czy kręci mnie, gdy rano budzisz mnie pieszczotami, zanim zdążę otworzyć oczy?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy wolę, gdy podczas całowania Twoje dłonie błądzą po moich pośladkach, czy wplątują się we włosy?"},
    {"kto": "ON", "tekst": "Co JA czuję, gdy podczas namiętnego pocałunku przyciskasz mnie nagle do ściany?"},
    {"kto": "ONA", "tekst": "Jak myślisz, od jakiego dotyku w samochodzie najszybciej robi mi się gorąco?"},
    {"kto": "ON", "tekst": "Zgadnij, w jakiej Twojej koszuli nocnej/piżamie chciałbym Cię dziś zobaczyć w łóżku?"},
    {"kto": "ONA", "tekst": "Wybierz: czy JA wolę, gdy prowokujesz mnie słowami, czy gdy prowokujesz mnie ciszą i wzrokiem?"},
    {"kto": "ON", "tekst": "Jak myślisz, co mnie bardziej nakręca: gdy całujesz mnie z językiem, czy gdy delikatnie ssiesz moją wargę?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy podnieca mnie myśl o pójściu na imprezę bez bielizny pod sukienką, wiedząc, że tylko Ty o tym wiesz?"},
    {"kto": "ON", "tekst": "Co JA wolę u Ciebie: kiedy masz zamknięte oczy i się oddajesz, czy gdy mierzysz mnie drapieżnym wzrokiem?"},
    {"kto": "ONA", "tekst": "Jak myślisz, co sobie wyobrażam, gdy dyskretnie gładzisz moje kolano pod obrusem na kolacji ze znajomymi?"},
    {"kto": "ON", "tekst": "Zgadnij, czy wolałbym, żebyś związała mi oczy, czy ręce w trakcie naszej gry wstępnej?"},
    {"kto": "ONA", "tekst": "Czy według mnie Twoje dłonie potrafią zdziałać więcej cudów na moich udach, czy na moim karku?"},
    {"kto": "ON", "tekst": "Zgadnij, czy pociąga mnie myśl o seksie na tylnym siedzeniu naszego samochodu w trakcie deszczu?"},
    {"kto": "ONA", "tekst": "Jak myślisz, czy rajcuje mnie wizja kąpieli we dwoje, w której to ja myję całe Twoje ciało?"},
    {"kto": "ON", "tekst": "Co nakręca MNIE bardziej: Twój głośny, niekontrolowany jęk, czy ciche, zduszone wzdychanie?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy lubię, gdy w trakcie pocałunku używasz swoich zębów na mojej szyi?"},
    {"kto": "ON", "tekst": "Jak myślisz, która część mojej gry wstępnej sprawia mi najwięcej satysfakcji, gdy widzę Twoją reakcję?"},
    {"kto": "ONA", "tekst": "Zgadnij, jak reaguję w środku, gdy stajesz za mną w kuchni i opierasz brodę na moim ramieniu?"},
    {"kto": "ON", "tekst": "Jak myślisz, czy kręcą mnie zarysowane pończochy, czy po prostu nagie, gładkie nogi?"},
    {"kto": "ONA", "tekst": "Zgadnij, co podnieca MNIE bardziej: masaż olejkiem, czy masaż kostką lodu po moich plecach?"},
    {"kto": "ON", "tekst": "Jak myślisz, czy kręci MNIE myśl o byciu uwiedzionym przez Ciebie, gdy wracam zły z pracy?"},
    {"kto": "ONA", "tekst": "Zgadnij, z czego najszybciej miękną mi nogi: z Twojego dotyku po pachwinach, czy pocałunków na brzuchu?"},
    {"kto": "ON", "tekst": "Czy według MNIE jesteś w łóżku bardziej kocicą, czy niewinną anielicą?"},
    {"kto": "ONA", "tekst": "Zgadnij, jak reaguję na myśl o tym, że mógłbyś zdjąć mi stanik jednym, zwinnym ruchem ręki?"},
    {"kto": "ON", "tekst": "Jak myślisz, czy rajcuje MNIE zostawianie po sobie śladów na Twoim ciele, by inni widzieli, że jesteś moja?"},
    {"kto": "ONA", "tekst": "Zgadnij, w którym momencie dnia mam największą ochotę na 'szybki numerek'?"},
    {"kto": "ON", "tekst": "Co według MNIE jest najgorętszym miejscem, w którym do tej pory się całowaliśmy?"}
]

p3 = [
    {"kto": "ONA", "tekst": "Zgadnij, czy kręci MNIE wchodzenie w pozycję 'na jeźdźca' przodem do Ciebie, czy tyłem (odwrócona)?"},
    {"kto": "ON", "tekst": "Jak myślisz, w jakiej pozycji mam poczucie najgłębszej penetracji i bliskości z Tobą?"},
    {"kto": "ONA", "tekst": "Zgadnij, jaki z moich fetyszy wciąż czeka, aż nabierzemy oboje odwagi, by go w 100% zrealizować?"},
    {"kto": "ON", "tekst": "Co JA czuję, gdy podczas seksu wbijasz paznokcie w moje plecy i mocno mnie drapiesz?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy wolę, gdy przejmujesz inicjatywę brutalnie i po męsku, czy gdy jesteś delikatny i pytasz?"},
    {"kto": "ON", "tekst": "Jak myślisz, czy kręci MNIE myśl o użyciu wibratora na Twojej łechtaczce podczas stosunku?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy bardziej kręci mnie seks na stojąco pod prysznicem, czy przed wielkim lustrem w sypialni?"},
    {"kto": "ON", "tekst": "Czy według MNIE lepsze jest uprawianie miłości w całkowitym mroku, czy przy przygaszonym świetle lampek?"},
    {"kto": "ONA", "tekst": "Jak myślisz, co czuję, gdy zmuszasz mnie do patrzenia na Twoją twarz tuż przed moim orgazmem?"},
    {"kto": "ON", "tekst": "Zgadnij, czy pociąga mnie myśl o seksie oralnym zaraz po przebudzeniu, zanim zdążymy umyć zęby?"},
    {"kto": "ONA", "tekst": "Czy według MNIE Twoje tempo podczas seksu jest idealne, czy wolałabym, byś częściej zwalniał?"},
    {"kto": "ON", "tekst": "Jak myślisz, co we mnie wybucha, gdy mówisz mi dokładnie, co mam teraz z Tobą zrobić?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy fantazjowałam kiedyś o tym, by uprawiać z Tobą głośny seks w pokoju hotelowym z cienkimi ścianami?"},
    {"kto": "ON", "tekst": "Czy kręci mnie patrzenie, jak onanizujesz się sama, gdy ja tylko leżę i daję Ci wskazówki?"},
    {"kto": "ONA", "tekst": "Jak myślisz, czy pociąga MNIE bycie spankowaną (klapsy) podczas ostrego seksu od tyłu?"},
    {"kto": "ON", "tekst": "Zgadnij, w której pozycji najbardziej podnieca mnie widok Twoich piersi?"},
    {"kto": "ONA", "tekst": "Czy pociąga MNIE myśl o byciu dominującą stroną i wydawaniu Ci bezwzględnych poleceń przez całą noc?"},
    {"kto": "ON", "tekst": "Jak myślisz, czy wolałbym zobaczyć Cię ubraną w pełny strój lateksowy, czy w subtelnej, białej koronce?"},
    {"kto": "ONA", "tekst": "Zgadnij, jak reaguje MOJE ciało na myśl o seksie oralnym na mnie przez pełne 30 minut bez przerwy?"},
    {"kto": "ON", "tekst": "Co według MNIE jest najseksowniejszym dźwiękiem, jaki wydajesz w momencie szczytowania?"},
    {"kto": "ONA", "tekst": "Jak myślisz, czy pociąga MNIE wizja, w której używasz moich własnych majtek do zakneblowania mi ust?"},
    {"kto": "ON", "tekst": "Zgadnij, czy według MNIE gra wstępna rano jest w ogóle potrzebna, czy wolę od razu przejść do rzeczy?"},
    {"kto": "ONA", "tekst": "Co we MNIE pęka, gdy w trakcie stosunku przybliżasz się do mojego ucha i używasz wulgarnego języka?"},
    {"kto": "ON", "tekst": "Jak myślisz, w którym momencie oralnego zaspokajania czuję, że robisz to absolutnie po mistrzowsku?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy bardziej rajcuje mnie 'szybki numerek' z ryzykiem nakrycia, czy maraton na bezpiecznym terytorium?"},
    {"kto": "ON", "tekst": "Co według MNIE najbardziej wyróżnia nasz seks na tle moich wyobrażeń i fantazji z przeszłości?"},
    {"kto": "ONA", "tekst": "Jak myślisz, jak bardzo lubię pozycję 69 – to dla mnie czysta przyjemność, czy męcząca akrobacja?"},
    {"kto": "ON", "tekst": "Zgadnij, czy wyobrażałem sobie kiedyś uprawianie seksu z Tobą na kuchennym blacie, podczas gdy szykujesz obiad?"},
    {"kto": "ONA", "tekst": "Czy podnieca MNIE myśl o seksie w przymierzalni sklepu odzieżowego, gdzie każdy szmer może nas zdradzić?"},
    {"kto": "ON", "tekst": "Jak myślisz, co dokładnie czuję, gdy zdejmujesz wszystko, zostawiając na sobie tylko wysokie szpilki?"}
]

p4 = [
    {"kto": "ONA", "tekst": "Zgadnij, czy podnieca MNIE myśl o zostawieniu całkowitej władzy w Twoich rękach, łącznie ze związaniem i zakneblowaniem?"},
    {"kto": "ON", "tekst": "Jak myślisz, czy kręciłaby MNIE sytuacja, w której nagrywamy nasz seks na wideo, by potem wspólnie to oglądać?"},
    {"kto": "ONA", "tekst": "Zgadnij, jak bym zareagowała, gdybyś bez słowa kazał mi uklęknąć zaraz po powrocie z pracy?"},
    {"kto": "ON", "tekst": "Czy kręci MNIE wizja głębokiego gardła (deepthroat), w której nie możesz złapać oddechu, a ja dyktuję tempo?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy zgodziłabym się na użycie lodu na moich strefach intymnych w momencie największego uniesienia?"},
    {"kto": "ON", "tekst": "Jak myślisz, co bym zrobił, gdybyś przebrała się za niegrzeczną uczennicę i kazała się wymierzyć 'karę'?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy fantazjowałam o byciu braną brutalnie od tyłu z jednoczesnym ciągnięciem za włosy i podduszaniem?"},
    {"kto": "ON", "tekst": "Czy podnieca mnie myśl o seksie analnym z Tobą, czy jest to strefa, która mnie nie pociąga?"},
    {"kto": "ONA", "tekst": "Jak myślisz, czy z przyjemnością skończyłabym oral, połykając wszystko do ostatniej kropli, patrząc Ci w oczy?"},
    {"kto": "ON", "tekst": "Zgadnij, co czuję na myśl o robieniu Ci dobrze ustami bezpośrednio po ostrym treningu na siłowni?"},
    {"kto": "ONA", "tekst": "Czy podnieca MNIE bycie nazywaną poniżającymi, wulgarnymi określeniami w samym środku szczytowania?"},
    {"kto": "ON", "tekst": "Jak myślisz, czy rajcowałoby MNIE uprawianie seksu w miejscu publicznym nocą, np. na masce naszego auta w lesie?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy kręci mnie odgrywanie ról (roleplay), w których udajemy obcych sobie ludzi w hotelowym barze?"},
    {"kto": "ON", "tekst": "Czy wyobrażałem sobie kiedyś, że kończę na Twojej twarzy, całkowicie brudząc Twój makijaż?"},
    {"kto": "ONA", "tekst": "Jak myślisz, czy ekscytuje mnie wizja noszenia zdalnie sterowanego wibratora (jajeczka) w restauracji, gdy Ty trzymasz pilota?"},
    {"kto": "ON", "tekst": "Zgadnij, czy podnieca mnie myśl o edgingu – czyli prowokowaniu Cię do szczytu i nagłym przerywaniu zabawy kilkukrotnie?"},
    {"kto": "ONA", "tekst": "Co bym powiedziała na to, gdybyś zażyczył sobie, by inna kobieta dołączyła do nas na jedną noc?"},
    {"kto": "ON", "tekst": "Czy podnieca MNIE myśl o obserwowaniu, jak pieścisz się sama przed lustrem, podczas gdy ja nie mogę Cię dotknąć?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy marzy mi się orgazm wywołany wyłącznie przez Twoje dłonie, podczas gdy moje są związane za plecami?"},
    {"kto": "ON", "tekst": "Jak myślisz, co bym zrobił, gdybyś obudziła mnie w środku nocy wślizgując się pode mnie i biorąc to, na co masz ochotę?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy pociąga mnie bycie przypartą do szyby okna na wysokim piętrze, z ryzykiem, że ktoś z naprzeciwka coś zobaczy?"},
    {"kto": "ON", "tekst": "Jak myślisz, w jakiej skali od 1 do 10 kręci MNIE myśl o byciu przywiązanym do ramy łóżka, całkowicie na Twojej łasce?"},
    {"kto": "ONA", "tekst": "Czy wyobrażałam sobie kiedyś, że podczas seksu na stole zrzucasz na podłogę wszystkie kieliszki i talerze?"},
    {"kto": "ON", "tekst": "Zgadnij, co bym poczuł, gdybyś bez ostrzeżenia wsadziła mi palec w miejsce, którego zazwyczaj unikamy?"},
    {"kto": "ONA", "tekst": "Jak myślisz, czy rajcuje MNIE zlizywanie Twoich soków ze swoich palców po tym, jak doprowadzisz mnie do orgazmu?"},
    {"kto": "ON", "tekst": "Czy według mnie 'sok z Twojego ciała' jest najsłodszym smakiem, jaki znam, czy traktuję to po prostu naturalnie?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy kiedykolwiek masturbowałam się wyobrażając sobie, że jesteśmy nakryci przez Twoich rodziców/znajomych?"},
    {"kto": "ON", "tekst": "Jak myślisz, co jest najostrzejszą fantazją, którą zachowuję tylko dla siebie i boję się o nią poprosić?"},
    {"kto": "ONA", "tekst": "Czy podnieca MNIE bycie traktowaną jak zwykły przedmiot służący tylko Twojej przyjemności przez krótką chwilę?"},
    {"kto": "ON", "tekst": "Zgadnij, czy kiedykolwiek miałem ochotę na tzw. 'hate sex' po kłótni, gdzie jedyne co nami kieruje to złość i instynkt?"}
]

kary_l1 = [
    "Przyciśnij partnera mocno do ściany i zafunduj mu głęboki, bardzo zachłanny pocałunek z językiem przez 60 sekund.",
    "Usiądź na kolanach partnera okrakiem i ocierajcie się o siebie bardzo powoli przez pełną minutę.",
    "Przejedź językiem po szyi partnera, zatrzymując się na płatku ucha, by go zmysłowo, lekko ugryźć.",
    "Wsuń dłonie pod koszulkę partnera na plecach, dociśnij go mocno do siebie i całuj przez 45 sekund.",
    "Złap partnera za nadgarstki, unieś je nad jego głowę i całuj zaborczo w szyję przez pół minuty.",
    "Rozepnij koszulę/bluzkę partnera i złóż mokry, gorący pocałunek tuż nad dekoltem/klatką piersiową.",
    "Szepnij partnerowi do ucha z detalami, co zrobisz z nim dzisiejszej nocy, jednocześnie gładząc jego udo blisko krocza.",
    "Wymasuj wewnętrzną stronę ud partnera oburącz (przez ubranie), celowo zbliżając się bardzo blisko środka.",
    "Złap partnera za włosy z tyłu głowy, odchyl lekko do tyłu i zmuś go do namiętnego pocałunku.",
    "Zawiąż partnerowi oczy. Całuj jego twarz, szyję i ramiona przez minutę – na przemian niezwykle czule i drapieżnie.",
    "Włóż palec partnera do swoich ust i powoli go ssij przez 20 sekund, utrzymując stały kontakt wzrokowy.",
    "Zmuś partnera do zamknięcia oczu. Przesuwaj dłońmi po jego klatce piersiowej/piersiach (przez ubranie) przez 60 sekund.",
    "Przeciągnij nosem i wargami wzdłuż linii szczęki partnera, zostawiając po sobie wyraźny, wilgotny ślad.",
    "Oprzyj dłonie na pośladkach partnera i dociśnij mocno jego biodra do swoich na całą minutę (na stojąco).",
    "Pocałuj partnera na tyle głęboko i wilgotno, by po rozłączeniu między Waszymi wargami rozciągnęła się nić śliny.",
    "Usiądź bardzo blisko, wsuń swoją dłoń na udo partnera i zostaw ją tam podczas czytania 3 kolejnych pytań.",
    "Weź palec partnera i powoli przesuń nim po swoich własnych ustach, patrząc mu prosto w oczy.",
    "Daj partnerowi namiętny pocałunek, jednocześnie wsuwając mu z tyłu dłoń pod pasek od spodni.",
    "Pociągnij dolną wargę partnera własnymi zębami i przytrzymaj przez kilka sekund.",
    "Złóż bardzo mokry pocałunek dokładnie w zgięciu łokcia partnera, a potem poprowadź język aż do nadgarstka.",
    "Przytulcie się przodem. Ocierajcie się swoimi klatkami piersiowymi przez okrągłą minutę bez słowa.",
    "Splećcie nogi pod stołem, trąc o siebie łydkami i udami najmocniej jak potraficie przez 3 pytania.",
    "Wymasuj kark partnera dwoma kciukami używając dużej siły, jednocześnie wpatrując się w jego usta.",
    "Oprzyj partnera o oparcie kanapy i wymij całą jego szyję swoim ciepłym językiem.",
    "Dmuchnij bardzo ciepłym powietrzem prosto w ucho partnera tak, by wywołać u niego gęsią skórkę."
]

kary_l2 = [
    "Zdejmij górną część swojego ubrania (koszulka/stanik/koszula) i zostań tak do kolejnej wylosowanej kary.",
    "Wsuń dłoń w spodnie/spódnicę partnera z tyłu i masuj jego nagie pośladki przez 60 sekund.",
    "Zdejmij majtki partnera (lub swoje), nie zdejmując przy tym spodni, i odrzuć je na środek pokoju.",
    "Rozsuń nogi partnera i złóż gorący pocałunek na wewnętrznej stronie uda, zaledwie centymetr od strefy V.",
    "Zrób partnerowi 2-minutowy lap dance, wyraźnie ocierając się swoimi narządami (w ubraniu) o jego/jej ciało.",
    "Zliż kroplę alkoholu (lub czegoś słodkiego) bezpośrednio z nagiego brzucha lub piersi partnera.",
    "Ugryź partnera w kark na tyle odważnie, by zostawić po sobie widoczny, czerwony ślad (malinkę).",
    "Rozepnij rozporek partnera (lub zsuń lekko bieliznę) i wsuń dłoń na okrągłą minutę. Tylko prowokujący dotyk.",
    "Połóż się na plecach. Partner siada na Tobie okrakiem i całkowicie dyktuje zasady pocałunków przez 2 minuty.",
    "Uderz partnera w pośladek z liścia na tyle mocno, by usłyszeć wyraźny dźwięk. Następnie pocałuj to miejsce.",
    "Zdejmij jeden element ubrania partnera, nie używając do tego w ogóle swoich rąk (pomóż sobie zębami).",
    "Włóż kostkę lodu do ust i przejedź bardzo powoli po kręgosłupie lub dekolcie partnera.",
    "Wsuń dłonie pod ubranie partnera i zmysłowo, dość mocno ugniataj jego/jej piersi/klatkę przez minutę.",
    "Przyciśnij partnera do ściany, wsuń swoje udo głęboko i twardo między jego nogi i całuj agresywnie przez 60 s.",
    "Rozchyl odrobinę ubranie partnera z przodu, pochyl się i zostaw serię mokrych pocałunków na samym dole brzucha.",
    "Przejmij całkowitą kontrolę: przywiąż partnera do krzesła jego własną koszulą na najbliższe 2 rundy.",
    "Zliż odrobinę soli/cukru z obojczyka partnera, po uprzednim mocnym polizaniu go własnym językiem.",
    "Wsuń palce głęboko we włosy partnera, pociągnij jego głowę i powiedz mu prosto w twarz, czego teraz od niego oczekujesz.",
    "Obliż swój własny palec, by był bardzo mokry, a następnie wsuń go do ucha partnera na sekundę.",
    "Rozepnij swój stanik/koszulę, chwyć dłoń partnera i przyciśnij ją mocno do swojej nagiej skóry na pełną minutę.",
    "Zmuś partnera, by położył się na plecach, po czym wsadź mu do ust swój palec i każ mu go namiętnie ssać.",
    "Pocałuj partnera tak mocno, by musiał cofnąć się o kilka kroków aż do najbliższego mebla lub ściany.",
    "Nalej sobie napój do ust i przekaż go partnerowi w trakcie tak zwanego 'francuskiego pocałunku'.",
    "Spędźcie 60 sekund w pełnym uścisku, gdzie Twoja dłoń twardo spoczywa na kroczu partnera (przez ubranie).",
    "Klep partnera po twarzy (bardzo delikatnie, dominująco) i zmuś go do wyznania Ci swojej brudnej fantazji."
]

kary_l3 = [
    "Zdejmijcie oboje dół ubrań (spodnie/spódnice). Od teraz gracie dalej w samej bieliźnie.",
    "Seks oralny przez bieliznę – 2 minuty pieszczenia ustami, językiem i gorącym oddechem przez materiał. To czysty teasing.",
    "Wsuń rękę do majtek partnera od przodu. Złap to, co masz złapać, i masuj rytmicznie przez pełne 2 minuty.",
    "Zdejmij partnerce biustonosz / partnerowi koszulkę. Zliż i delikatnie pieść sutki ustami przez okrągłą minutę.",
    "Rozsuń nogi partnera i całuj wnętrze ud tuż przy linii bielizny przez 60 sekund. Bądź tak blisko środka, jak się da, ale go nie dotykaj.",
    "Odsłoń miejsce intymne partnera. Masz za zadanie zadowolić go językiem przez równe 60 sekund. Nastawcie stoper.",
    "Zejdź w dół. Użyj ust i dłoni na partnerze przez 2 minuty, ale absolutnie NIE POZWÓL mu dojść. Przerwij na najgorętszym etapie.",
    "Użyj kostki lodu: przejedź nią po ciele partnera od dekoltu do samego dołu brzucha, a potem powoli zliż każdą kroplę.",
    "Zasymuluj pozycję na jeźdźca w bieliźnie: usiądź na partnerze i poruszaj biodrami przez 60 sekund, ocierając się o siebie.",
    "Odwróć partnera na brzuch. Zdejmij mu bieliznę do połowy i zmysłowo masuj nagie pośladki olejkiem lub balsamem.",
    "Zwiąż z tyłu ręce partnera krawatem. Przez 3 minuty całuj jego/jej szyję i brzuch – on/ona może tylko oddychać i czuć.",
    "Połóż się na plecach. Partner ma prawo przez 2 minuty pieścić Cię językiem wszędzie, gdzie tylko zechce.",
    "Zdejmij całą swoją bieliznę. Siedzisz nago od pasa w dół na kanapie przez 3 następne pytania.",
    "Zliż odrobinę alkoholu (lub czegoś słodkiego) z dolnych partii brzucha partnera, bardzo blisko strefy V.",
    "Głębokie pocałunki z użyciem języka, w trakcie których oboje macie dłonie wsunięte pod swoją bieliznę przez 2 minuty.",
    "Wymuś pozycję 69 (w bieliźnie lub bez). Robicie sobie dobrze ustami/dłońmi nawzajem przez pełne 2 minuty stopera.",
    "Posadź partnera na blacie w kuchni lub stole. Wejdź między jego nogi, przytul się i pieść go dłońmi przez 2 minuty.",
    "Szepnij partnerowi do ucha niegrzeczne polecenie dotyczące dotyku, a partner musi je teraz na sobie wykonać przez 60 sekund.",
    "Rozbierz się do naga i zaprezentuj partnerowi przez minutę pozycję, w której chciałbyś/chciałabyś być teraz z nim/nią w łóżku.",
    "Zdejmij bieliznę, odwróć się tyłem i pozwól partnerowi uderzyć Cię 3 razy z otwartej dłoni w pośladki (klapsy za zgodą).",
    "Będziesz w 100% uległy/a przez następne 3 minuty. Partner przejmuje stery i pieści Twoje ciało tak, jak sam ma na to ochotę.",
    "Użyj jakiejkolwiek zabawki erotycznej (lub swoich dłoni) przed oczami partnera przez 2 minuty, patrząc mu w oczy.",
    "Połóż partnera na plecach, ściągnij mu bieliznę i przez 2 minuty rób mu niezwykle czuły i gorący masaż stref intymnych dłońmi.",
    "Zdejmij swoją bieliznę bez pomocy rąk – użyj do tego wyłącznie swojego ciała lub ocierania się o partnera.",
    "Wejdź w przestrzeń osobistą partnera, przyciągnij go do siebie mocno za talię i zafunduj mu pocałunek, po którym zbraknie mu tchu."
]

kary_l1 = [
    "Splećcie dłonie i patrzcie sobie głęboko w oczy bez słowa przez pełne 60 sekund. Uśmiech dozwolony.",
    "Złóż bardzo wolny, 15-sekundowy pocałunek w wewnętrzną stronę nadgarstka partnera.",
    "Wymasuj skronie i czoło partnera bardzo delikatnymi, uspokajającymi ruchami przez minutę.",
    "Usiądź za partnerem i powoli całuj jego/jej kark. Niech to będzie czułe i zmysłowe.",
    "Powiedz partnerowi komplement dotyczący części jego ciała, której normalnie nie chwalisz.",
    "Złap partnera w tali i przyciągnij go mocno do siebie. Stójcie tak przytuleni przez 90 sekund.",
    "Pogłaszcz partnera po policzku, a potem złóż delikatny pocałunek na jego nosie.",
    "Pociągnij delikatnie płatek ucha partnera wargami, a potem szepnij mu coś miłego.",
    "Ucałuj każdą kostkę dłoni partnera, jedną po drugiej, nie spuszczając z niego wzroku.",
    "Pozwól partnerowi wodzić palcami po Twojej szyi i obojczykach przez 60 sekund. Zamknij oczy.",
    "Delikatnie przejedź paznokciami od ramion partnera, aż po jego dłonie. Powtórz 5 razy.",
    "Pocałuj partnera w oba policzki, w czoło, a na koniec daj długi, namiętny pocałunek w usta.",
    "Zbliż swoje usta do ust partnera na odległość milimetra. Pozostańcie tak przez 1 minutę bez całowania.",
    "Zdejmij partnerowi skarpetki i bardzo delikatnie pomasuj mu stopy kciukami.",
    "Obejmij twarz partnera obiema dłońmi i uśmiechnij się do niego, patrząc z absolutną czułością.",
    "Wsuń dłoń we włosy partnera i powoli je przeczesz, masując przy tym skórę głowy.",
    "Złóż mokry pocałunek dokładnie w dołku między obojczykami partnera i zostań tam na 10 sekund.",
    "Usiądź tak blisko partnera, by wasze kolana i uda stykały się przez całą następną rundę pytań.",
    "Zatańcz z partnerem (nawet na siedząco), wtulając się mocno w jego klatkę piersiową na minutę.",
    "Pogryź bardzo delikatnie dolną wargę partnera podczas pocałunku.",
    "Połóż głowę na kolanach partnera i pozwól mu/jej gładzić Twoją twarz przez 2 minuty.",
    "Ucałuj wewnętrzną stronę ramienia partnera, przesuwając się powoli ku górze.",
    "Zamknij oczy. Partner ma 3 próby, by musnąć Cię palcem w twarz, a Ty musisz zgadnąć gdzie to było.",
    "Oprzyjcie się czołami o siebie i zsynchronizujcie oddechy przez 60 sekund.",
    "Złap partnera za ramiona i wymasuj je bardzo stanowczym, odprężającym chwytem."
]

kary_l2 = [
    "Zdejmij bluzę, sweter lub koszulę (pozostań w t-shircie lub bieliźnie) do końca gry.",
    "Zdejmij jeden mały element ubrania partnera, używając do tego tylko jednej ręki i patrząc mu w oczy.",
    "Połóż partnera na plecach i wodź po jego ciele (z wyłączeniem stref intymnych) przez minutę.",
    "Złóż serię pocałunków na wewnętrznej stronie uda partnera, tuż nad kolanem.",
    "Ugryź partnera w kark na tyle mocno, by poczuł dreszcz, a potem powoli zliż to miejsce.",
    "Wsuń dłoń pod koszulkę partnera na plecach i zmysłowo masuj jego skórę przez 60 sekund.",
    "Usiądź okrakiem na nogach partnera (w ubraniu) i ocieraj się delikatnie w rytm muzyki przez 2 minuty.",
    "Rozepnij pasek u spodni partnera lub guzik u spódnicy. Zostają tak do następnej wylosowanej kary.",
    "Złap partnera za dłonie, spleć je ze swoimi i przyciśnijcie się do siebie, wymieniając francuski pocałunek.",
    "Złóż gorące pocałunki biegnące wzdłuż brzucha partnera, zatrzymując się milimetr nad krawędzią spodni/bielizny.",
    "Przesuwaj językiem po płatku ucha i szyi partnera, oddychając ciężko przez okrągłą minutę.",
    "Wsuń palce za pasek spodni partnera i przyciągnij go mocno do siebie, zderzając się ciałami.",
    "Zawiąż oczy partnerowi szalikiem. Skup się na dotykaniu jego szyi i klatki piersiowej na najbliższą rundę.",
    "Pocałuj brzuch partnera, a następnie chuchnij na to miejsce ciepłym powietrzem.",
    "Odwróć partnera tyłem, przytul się do jego pleców i całuj wzdłuż linii ramion.",
    "Zrób partnerowi krótki, 1-minutowy striptiz z muzyką (możesz tylko zmysłowo tańczyć i zsunąć np. ramiączko).",
    "Wsuń dłoń we włosy partnera z tyłu głowy, odchyl do tyłu i pocałuj łapczywie w otwarte usta.",
    "Oprzyj nogę na meblu i pozwól partnerowi powoli i namiętnie masować Twoją łydkę i udo.",
    "Przyłóż usta do ucha partnera i wyznaj mu szeptem, co dzisiaj na sobie nosisz pod ubraniem.",
    "Rozchyl lekko dekolt partnera i zostaw na skórze wilgotny pocałunek.",
    "Zmuś partnera do rozluźnienia. Masuj jego pośladki przez ubranie mocnym, dominującym uciskiem.",
    "Złap partnera w talii tak mocno, żeby aż musiał z głębokim wdechem przylgnąć do Ciebie.",
    "Będąc bardzo blisko twarzy partnera, zjedz coś zmysłowo ze swojego palca, nie spuszczając z niego wzroku.",
    "Złóż pocałunek na szyi partnera, jednocześnie dociskając jedno udo mocno między jego nogi.",
    "Rozepnij swój zamek/guzik i pozwól partnerowi trzymać dłoń na samej krawędzi Twojej bielizny przez 2 pytania."
]

kary_l3 = [
    "Zdejmij dół ubrań (spodnie/spódnicę). Gracie dalej, mając na dole tylko bieliznę.",
    "Seks oralny przez ubranie/bieliznę – 2 minuty ocierania twarzą, ustami i gorącym oddechem przez materiał.",
    "Wsuń dłoń do majtek partnera. Złap to miejsce i masuj bardzo rytmicznie przez pełne 2 minuty.",
    "Zdejmij partnerce stanik / partnerowi t-shirt. Zliż i delikatnie pieść sutki ustami przez 60 sekund.",
    "Rozsuń nogi partnera i całuj wnętrze ud tuż przy linii bielizny. Jesteś o krok od centrum przez minutę.",
    "Odsłoń miejsce intymne partnera. Masz za zadanie zadowolić go swoim językiem przez równe 60 sekund (stoper).",
    "Zejdź w dół i zacznij sprawiać partnerowi czystą rozkosz ustami. Przerwij bezlitośnie po 2 minutach. Żadnego orgazmu.",
    "Użyj kostki lodu: przejedź nią po klatce i brzuchu partnera, a potem zliż zimną wodę, zjeżdżając aż do pępka.",
    "Zasymuluj pozycję na jeźdźca w samej bieliźnie. Usiądź na partnerze, ocieraj się intensywnie o niego przez 2 minuty.",
    "Odwróć partnera na brzuch. Zdejmij mu bieliznę do połowy i zmysłowo wymasuj nagie pośladki, dodając pocałunki.",
    "Zwiąż z tyłu ręce partnera. Przez 3 minuty całuj jego/jej nagie ciało od szyi w dół – partner nie może się bronić.",
    "Połóż się na plecach z zamkniętymi oczami. Partner przez 2 minuty pieści Cię dłońmi wszędzie, gdzie tylko zechce.",
    "Zdejmij całą swoją bieliznę. Pozostajesz nago od pasa w dół na 3 następne rundy pytań.",
    "Rozlej dosłownie kilka kropel słodkiego napoju na podbrzusze partnera i dokładnie zliż wszystko językiem.",
    "Głębokie pocałunki, w trakcie których oboje wsuwacie sobie dłonie pod bieliznę i pieszczecie się przez 2 minuty.",
    "Wymuś pozycję 69 (w bieliźnie lub bez). Zadowalacie się dłońmi i ustami przez pełne 2 minuty ze stoperem.",
    "Posadź partnera wysoko (np. na blacie/stole). Stań między jego nogami i pieść jego uda oraz krocze przez 2 min.",
    "Szepnij partnerowi do ucha brudne polecenie, a partner musi zacząć dotykać samego siebie na Twoich oczach przez 60 sek.",
    "Rozbierz się do naga od pasa w górę i zaprezentuj się partnerowi z dumą. Zostań tak przez 2 rundy.",
    "Zdejmij bieliznę, odwróć się tyłem. Partner daje Ci 3 solidne, rozgrzewające klapsy w pośladki.",
    "Jesteś uległy/a przez 3 minuty. Partner przejmuje całkowitą kontrolę i używa swoich dłoni/ust na Tobie według własnych zasad.",
    "Użyj przed partnerem zabawki erotycznej (jeśli macie) przez 2 minuty, głośno mówiąc, jak dobrze się czujesz.",
    "Połóż partnera, rozsuń mu nogi i przez 2 minuty zrób mu precyzyjny, bardzo intymny masaż dłońmi stref erogennych.",
    "Zdejmij z siebie absolutnie całą bieliznę (jeśli coś jeszcze masz) bez użycia rąk. Użyj tylko ruchów bioder.",
    "Wciśnij partnera w kanapę, przygnieć go swoim ciałem, zacznij zaborczo całować szyję i łapczywie ściągać jego ubrania."
]

kary_l4 = [
    "JESTEŚCIE NAGO. Zdejmujecie absolutnie wszystko, co na Was zostało. Do końca gry zero ubrań.",
    "Penetracja! Wchodzisz w partnera (lub on w Ciebie). Macie 3 minuty dzikiego, prawdziwego seksu, zanim wrócicie do pytań.",
    "Połóż się płasko na plecach. Partner siada nad Tobą. Zaspokajasz go ustami tak namiętnie, by zapomniał jak się nazywa. 3 minuty.",
    "Edging (kontrola). Doprowadź partnera oralnie lub dłonią do samego skraju orgazmu i natychmiast przestań. Ochłońcie.",
    "Weź partnera na pieska. Złap go mocno za talię i wchodź w niego rytmicznie przez 3 minuty. Stoper odmierza czas.",
    "Seks oralny. Zejdź na dół i przez 3 minuty daj z siebie wszystko. Doprowadź partnera do szaleństwa. Pełne połykanie/finał dowolone.",
    "Oprzyj partnera/partnerkę o ścianę, podnieś nogę i wejdź z dużą siłą. Uprawiajcie namiętny seks na stojąco przez 2 minuty.",
    "Partner leży na plecach. Siadasz na nim (na jeźdźca) i całkowicie kontrolujesz głębokość i tempo rżnięcia przez 3 min.",
    "Pozycja 69 nago. Oboje używacie ust z maksymalnym zaangażowaniem. Jeśli ktoś z Was dojdzie – to tylko lepiej! 3 minuty.",
    "Załóż opaskę na oczy partnera. Pieść jego nagie ciało, w tym strefy intymne, dłońmi i językiem. On nie może Cię dotknąć. 3 minuty.",
    "Zdominuj partnera: przywiąż jego dłonie do łóżka lub krzesła. Używaj ust, dłoni i oddechu wszędzie tam, gdzie sprawi mu to szał. 3 min.",
    "Zmuś partnera, by poprosił Cię ładnie o orgazm. Połóż go na plecach i pieść dopóki oboje nie zapomnicie o grze.",
    "Szybki numerek na stole! Sadzasz partnera na twardym blacie, rozsuwasz nogi i wchodzisz bardzo dynamicznie na 2 minuty.",
    "Weźcie swój najmocniejszy wibrator/gadżet. Użyj go na najczulszym miejscu partnera przez 3 minuty na wysokich obrotach.",
    "Zadanie ostateczne: Nie wracacie do gry, dopóki ustami lub dłońmi nie doprowadzisz partnera do głośnego, pełnego orgazmu.",
    "Pauzujecie grę na 10 minut. Wchodzicie pod gorący prysznic i tam, cali w pianie, kochacie się na stojąco.",
    "Odwróć partnera tyłem do siebie (na łyżeczkę). Wejdź w niego delikatnie i powoli. Masuj piersi/klatkę i szepcz obrzydliwości do ucha. 3 min.",
    "Partner klęczy przed Tobą. Zaspokaja Cię ustami, a Ty przytrzymujesz jego głowę, nadając rytm. 2 minuty.",
    "Rozsmaruj olejek do masażu na całym nagim ciele partnera. Wmasuj go dłońmi i swoimi nagimi piersiami/torsem. Zakończ penetracją.",
    "Doprowadź się samemu/samej do orgazmu, podczas gdy partner leży obok i tylko na Ciebie patrzy i mówi, jak gorąco to wygląda.",
    "Wejdź pod stół. Zrób partnerowi doskonały, głęboki seks oralny przez 2 minuty, podczas gdy on siedzi prosto na kanapie.",
    "Seks z pełnym kontaktem wzrokowym. Misjonarz. Ty narzucasz bardzo równe, wolne tempo. Nie odrywajcie od siebie wzroku przez 3 minuty.",
    "Zrzucasz partnera na plecy. Siadasz mu na twarzy (lub na klatce), wymuszając na nim oralne usługi przez 3 minuty Twojej czystej dominacji.",
    "Chwyć partnera mocno za włosy z tyłu, przyciągnij do siebie, pocałuj brutalnie i wsadź mu dłoń w krocze, sprawiając by oszalał na 2 minuty.",
    "SYSTEM OVERLOAD. Koniec z pilotem. Kładziesz partnera na dywanie lub łóżku. Kochacie się tak głośno i namiętnie, aż sąsiedzi to usłyszą. 😈🔥"
]

# BOSS FIGHTS (Zadania Specjalne przy 100% napięcia)
zadania_boss = [
    "🚨 ALARM KRYTYCZNY: Oboje zdejmujecie WSZYSTKO, nalewacie wspólnego shota z jednego kieliszka i pijecie go, trzymając go w ustach!",
    "🚨 ALARM KRYTYCZNY: Dominacja! Sędzia przejmuje całkowitą kontrolę nad ciałem partnera na 5 minut. Wszelki dotyk, bez sprzeciwu.",
    "🚨 ALARM KRYTYCZNY: Pozycja 69 nago przez pełne 3 minuty. System się wyłącza, wraca do pracy dopiero po wybuchowym finale!",
    "🚨 ALARM KRYTYCZNY: Pauzujecie TV. Idziecie prosto do sypialni na ostry, 10-minutowy numerek bez żadnych barier. Zobaczymy się później!",
    "🚨 ALARM KRYTYCZNY: Najbrudniejsza Rzecz! Wykonujecie tu i teraz na sobie nawzajem najbardziej bezwstydną rzecz, o jakiej pomyśleliście dziś podczas gry."
]

# ==========================================
# ==========================================
# 4. LOGIKA SYSTEMU WYKUPNEGO I GENEROWANIA GRY
# ==========================================

def get_shot_cost(refusals):
    """Zwraca ilość shotów do dodania do licznika na ekranie TV"""
    if refusals < 1: 
        return 0  # Darmowe życie
    elif refusals < 9: 
        return 1  # Etapy kosztujące 1 shota
    elif refusals < 17: 
        return 2  # Etapy kosztujące 2 shoty
    else: 
        return 0  # Ostateczna nagość lub kara (tu już nie doliczamy shotów do licznika)

def get_buyout_info(refusals):
    # 1. Jedno życie (indeks 0)
    if refusals < 1:
        return "FREE", "ŻYCIE ❤️ (Zostało: 1)"
    
    # 2. Cztery razy po 1 shocie (indeksy 1, 2, 3, 4)
    elif refusals < 5:
        return "SHOT_1", "KOSZT: 1 SHOT 🥃"
    
    # 3. Cztery razy po 1 shocie + 1 część ubrania (indeksy 5, 6, 7, 8)
    elif refusals < 9:
        return "SHOT_1_CLOTHES_1", "KOSZT: 1 SHOT + 1 UBRANIE 🔞"
    
    # 4. Cztery razy po 2 shoty + 1 część ubrania (indeksy 9, 10, 11, 12)
    elif refusals < 13:
        return "SHOT_2_CLOTHES_1", "KOSZT: 2 SHOTY + 1 UBRANIE 🔥"
    
    # 5. Cztery razy po 2 shoty + 2 części ubrania (indeksy 13, 14, 15, 16)
    elif refusals < 17:
        return "SHOT_2_CLOTHES_2", "KOSZT: 2 SHOTY + 2 UBRANIA 🌶️"
    
    # 6. Ostateczna kara: zdejmujesz wszystko (indeks 17)
    elif refusals < 18:
        return "FULL_NUDE", "WYKUPNE: ZDEJMUJESZ WSZYSTKO! 🔞🔥"
    
    # 7. Po wszystkim kara z TV staje się obowiązkowa
    else:
        return "MANDATORY", "KARA JEST OBOWIĄZKOWA! 😈"

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
    return pobierz_poziom(pytania_intro, 20)

def generuj_gre():
    talia = (
        pobierz_poziom(p1, 10) + 
        pobierz_poziom(p2, 10) + 
        pobierz_poziom(p3, 10) + 
        pobierz_poziom(p4, 10)
    )
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
        "phase": "rules",  
        "intro_q": 0,
        "intro_gra": generuj_intro(),
        "current_q": 0, 
        "status": "question", 
        "penalty": "", 
        "gra": generuj_gre(),
        "ona_refusals": 0, 
        "on_refusals": 0,
        "ona_shots": 0,  
        "on_shots": 0,
        "ona_veto": 1,
        "on_veto": 1,
        "tension_level": 0, # <-- NOWE
        "boss_task": "",    # <-- NOWE
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
    
    if state["phase"] == "rules":
        st.markdown("""
        <div class='premium-box' style='max-width: 900px;'>
            <h1 class='gold-text' style='font-size: 48px;'>ZASADY GRY 😈</h1>
            <div class='rules-list'>
                <div class='rules-item'><strong>1. SĘDZIA CZYTA:</strong> Na ekranie pojawia się pytanie. Osoba wywołana (Sędzia) czyta je na głos.</div>
                <div class='rules-item'><strong>2. TEST WIEDZY:</strong> Druga osoba musi odgadnąć myśli i fantazje Sędziego.</div>
                <div class='rules-item'><strong>3. PILOT PRAWDY:</strong> Sędzia trzyma pilota i ocenia odpowiedź.</div>
                <div class='rules-item'><strong>4. KARY I WYKUPNE:</strong> Jeśli oblejesz, wykonujesz karę lub wykupujesz się. Złe odpowiedzi i VETO ładują PASEK NAPIĘCIA!</div>
                <div class='rules-item'><strong>5. TRYB KRYTYCZNY:</strong> Gdy Pasek Napięcia osiągnie 100%, gra przerywa rundę i aktywuje Zadanie Specjalne.</div>
            </div>
            <p style='color: #8c7a96; font-size: 20px; margin-top: 30px; letter-spacing: 2px;'>Czekam na sygnał z Pilota...</p>
        </div>
        """, unsafe_allow_html=True)

    elif state["phase"] == "intro":
        q_idx = state["intro_q"]
        if q_idx < len(state["intro_gra"]):
            q = state["intro_gra"][q_idx]
            who_val = str(q["kto"]).upper().strip()
            imie_info = f"ROZMOWA: {IMIE_ONA if who_val == 'ONA' else IMIE_ON}"
            
            st.markdown(f"<div class='elegant-header'>Rozgrzewka ({q_idx + 1}/{len(state['intro_gra'])})</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='premium-box' style='border-color: #4bd67b;'><div class='turn-badge turn-intro'>{imie_info}</div><div class='gold-text'>{q['tekst']}</div></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='premium-box' style='border-color: #d4af37;'><h1 class='gold-text'>ROZGRZEWKA ZAKOŃCZONA</h1><p style='color: #8c7a96; font-size: 24px; margin-top: 20px;'>Pora podnieść temperaturę... Czekam na Pilota! 😈</p></div>", unsafe_allow_html=True)

    elif state["status"] == "boss_fight":
        # EKRAN TRYBU KRYTYCZNEGO (100% NAPIĘCIA)
        st.markdown(f"""
        <div class='premium-box' style='background: rgba(255, 0, 0, 0.15); border: 3px solid #ff4b4b; animation: pulse 1.5s infinite;'>
            <h1 style='color: #ff4b4b; font-size: 64px; margin-bottom: 20px;'>TRYB KRYTYCZNY! 🚨</h1>
            <p style='color: #e0d8d3; font-size: 32px; font-weight: bold;'>{state['boss_task']}</p>
        </div>
        """, unsafe_allow_html=True)

    else:
        # EKRAN GŁÓWNY GRY (Ze statystykami i paskiem napięcia)
        veto_ona = "✅ DOSTĘPNA" if state["ona_veto"] > 0 else "❌ ZUŻYTA"
        veto_on = "✅ DOSTĘPNA" if state["on_veto"] > 0 else "❌ ZUŻYTA"
        
        st.markdown(f"""
        <div class='stats-container'>
            <div class='stat-card'>
                <div class='stat-name'>{IMIE_ONA}</div>
                <div class='stat-lives'>{get_buyout_info(state['ona_refusals'])[1]}</div>
                <div class='stat-shots'>🥃 WYPITE: {state['ona_shots']}</div>
                <div style='color: #8c7a96; font-size: 14px; margin-top: 10px;'>KARTA VETO: {veto_ona}</div>
            </div>
            <div class='stat-card'>
                <div class='stat-name'>{IMIE_ON}</div>
                <div class='stat-lives'>{get_buyout_info(state['on_refusals'])[1]}</div>
                <div class='stat-shots'>🥃 WYPITE: {state['on_shots']}</div>
                <div style='color: #8c7a96; font-size: 14px; margin-top: 10px;'>KARTA VETO: {veto_on}</div>
            </div>
        </div>
        
        <div style='max-width: 1000px; margin: 20px auto; text-align: center;'>
            <div class='tension-text'>PASEK NAPIĘCIA: {state['tension_level']}%</div>
            <div class='tension-container'>
                <div class='tension-bar' style='width: {state['tension_level']}%;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        q_idx = state["current_q"]
        if q_idx < len(state["gra"]):
            q = state["gra"][q_idx]
            
            if state["status"] == "question":
                who_val = str(q["kto"]).upper().strip()
                badge_class = "turn-toast" if who_val == "TOAST" else ("turn-ona" if who_val == "ONA" else "turn-on")
                imie_info = "TOAST!" if who_val == "TOAST" else f"CZYTA SĘDZIA: {IMIE_ONA if who_val == 'ONA' else IMIE_ON}"
                st.markdown(f"<div class='elegant-header'>Runda {q_idx + 1}</div><div class='premium-box'><div class='turn-badge {badge_class}'>{imie_info}</div><div class='gold-text'>{q['tekst']}</div></div>", unsafe_allow_html=True)
                
            elif state["status"] == "decision":
                st.markdown(f"<div class='elegant-header'>Runda {q_idx + 1}</div><div class='premium-box' style='background:rgba(21, 16, 28, 0.8); border-color:#d4af37;'><h1 class='gold-text'>ZŁA ODPOWIEDŹ... 🤔</h1><div style='background: rgba(255, 75, 75, 0.15); padding: 20px; border-radius: 15px; border: 1px solid #ff4b4b; margin: 30px 0;'><h3 style='color: #ff4b4b; margin-top: 0; font-size: 18px; letter-spacing: 2px;'>ZAGROŻENIE KARĄ:</h3><p style='color: #e0d8d3; font-size: 28px; font-weight: bold;'>{state['penalty']}</p></div><p style='color: #8c7a96; font-size: 20px; margin-top: 20px;'>Wykupujesz się, używasz VETO, czy podejmujesz wyzwanie?</p></div>", unsafe_allow_html=True)
                
            elif state["status"] == "result":
                txt, bg = (state["buyout_msg"], "rgba(212, 175, 55, 0.15)") if state["buyout_msg"] else (f"ZADANIE:<br><span style='color: #ff4b4b;'>{state['penalty']}</span>", "rgba(255, 75, 75, 0.15)")
                st.markdown(f"<div class='premium-box' style='background:{bg}; border-color:#d4af37;'><h1 class='gold-text' style='font-size: 40px;'>{txt}</h1></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='premium-box'><h1 class='gold-text'>KONIEC GRY.😈</h1></div>", unsafe_allow_html=True)

elif view_type == "pilot":
    if state["phase"] == "rules":
        st.markdown("<div class='pilot-box' style='border-color: #d4af37;'><div class='elegant-header'>Witajcie</div><h1 class='gold-text' style='font-size: 28px; margin-top: 10px;'>PRZECZYTAJCIE ZASADY NA EKRANIE TV</h1></div>", unsafe_allow_html=True)
        if st.button("PRZEJDŹ DO ROZGRZEWKI 💕", use_container_width=True, type="primary"): state["phase"] = "intro"; st.rerun()

    elif state["phase"] == "intro":
        q_idx = state["intro_q"]
        if q_idx < len(state["intro_gra"]):
            st.markdown("<div class='pilot-box' style='border-color: #4bd67b;'><div class='elegant-header'>Panel Sterowania</div><h1 class='gold-text' style='font-size: 32px; color: #4bd67b; margin-top: 10px;'>ROZGRZEWKA 💕</h1></div>", unsafe_allow_html=True)
            if st.button("NASTĘPNE PYTANIE ➔", use_container_width=True, type="secondary"): state["intro_q"] += 1; st.rerun()
            st.markdown("<hr style='border-color: #2a2035; margin: 30px 0;'>", unsafe_allow_html=True)
            if st.button("ZACZYNAMY GRĘ WŁAŚCIWĄ 😈", use_container_width=True, type="primary"): state["phase"] = "main"; st.rerun()
        else:
            st.markdown("<div class='pilot-box' style='border-color: #ff4b4b;'><div class='elegant-header'>Rozgrzewka</div><h1 class='gold-text' style='font-size: 26px; color: #ff4b4b; margin-top: 10px;'>PYTANIA WYCZERPANE</h1></div>", unsafe_allow_html=True)
            if st.button("ZACZYNAMY GRĘ WŁAŚCIWĄ 😈", use_container_width=True, type="primary"): state["phase"] = "main"; st.rerun()

    elif state["status"] == "boss_fight":
        st.markdown("<div class='pilot-box' style='border-color: #ff4b4b;'><div class='elegant-header'>WYZWANIE KRYTYCZNE</div><h1 class='gold-text' style='font-size: 28px; color: #ff4b4b; margin-top: 10px;'>WYKONAJCIE ZADANIE Z EKRANU TV!</h1></div>", unsafe_allow_html=True)
        if st.button("ZADANIE WYKONANE ✅ (Reset Napięcia)", use_container_width=True, type="primary"):
            state["status"] = "question"
            state["tension_level"] = 0
            state["boss_task"] = ""
            state["current_q"] += 1
            st.rerun()

    else:
        q_idx = state["current_q"]
        if q_idx < len(state["gra"]):
            q = state["gra"][q_idx]
            who_val = str(q["kto"]).upper().strip()
            
            sedzia_imie = IMIE_ONA if who_val == "ONA" else IMIE_ON
            odpowiada_kto = "on" if who_val == "ONA" else "ona"
            odpowiada_imie = IMIE_ON if who_val == "ONA" else IMIE_ONA
            badge_class = "turn-ona" if who_val == "ONA" else "turn-on"
            
            if state["status"] == "question":
                if who_val == "TOAST":
                    st.markdown("<div class='pilot-box' style='border-color: #ff4b4b;'><div class='elegant-header'>Panel Sterowania</div><div class='turn-badge turn-toast' style='margin-bottom: 0; margin-top: 15px;'>WYZWANIE ALKOHOLOWE! 🥂</div></div>", unsafe_allow_html=True)
                    if st.button("WYPITE! (+1 SHOT DLA OBOJGA) ➔", use_container_width=True, type="primary"):
                        state["ona_shots"] += 1; state["on_shots"] += 1; state["status"] = "result"; state["buyout_msg"] = "NA ZDROWIE!"
                        st.rerun()
                else:
                    st.markdown(f"<div class='pilot-box'><div class='elegant-header'>Runda {q_idx + 1}</div><div class='turn-badge {badge_class}' style='margin-bottom: 0; margin-top: 15px;'>SĘDZIUJE: {sedzia_imie}</div></div>", unsafe_allow_html=True)
                    if st.button("TAK (ODGADŁ/A ZGODNIE Z PRAWDĄ) ✅", use_container_width=True, type="primary"):
                        state["status"] = "result"; state["buyout_msg"] = "PRAWDA ZAAKCEPTOWANA ✅"; st.rerun()
                    if st.button("NIE ❌ (+10% NAPIĘCIA)", use_container_width=True, type="secondary"):
                        state["status"] = "decision"
                        state["penalty"] = wylosuj_kare(q_idx, len(state["gra"]))
                        state["tension_level"] += 10
                        if state["tension_level"] >= 100:
                            state["status"] = "boss_fight"
                            state["boss_task"] = random.choice(zadania_boss)
                        st.rerun()
            
            elif state["status"] == "decision":
                refusals = state[f"{odpowiada_kto}_refusals"]
                b_type, b_label = get_buyout_info(refusals)
                shots_to_add = get_shot_cost(refusals)
                
                st.markdown(f"<div class='pilot-box' style='border-color: #ff4b4b;'><div class='elegant-header'>ZŁA ODPOWIEDŹ!</div><div class='turn-badge turn-toast' style='margin-bottom: 0; margin-top: 15px;'>KARA DLA: {odpowiada_imie}</div><div style='margin-top: 20px; padding: 15px; border: 1px solid #ff4b4b; border-radius: 10px; background: rgba(255, 75, 75, 0.1);'><p style='color: #ff4b4b; font-size: 14px; margin-bottom: 5px; text-transform: uppercase;'>Wylosowana kara:</p><p style='color: #e0d8d3; font-size: 18px; font-weight: bold;'>{state['penalty']}</p></div></div>", unsafe_allow_html=True)
                
                if b_type != "MANDATORY":
                    if st.button(f"UŻYJ: {b_label} 🛡️", use_container_width=True, type="primary"):
                        state[f"{odpowiada_kto}_shots"] += shots_to_add
                        state[f"{odpowiada_kto}_refusals"] += 1
                        state["status"] = "result"; state["buyout_msg"] = f"WYKUPIONE: {b_label}"
                        st.rerun()
                
                if state[f"{odpowiada_kto}_veto"] > 0:
                    if st.button("VETO 🔄 (+20% NAPIĘCIA)", use_container_width=True, type="primary"):
                        state[f"{odpowiada_kto}_veto"] -= 1
                        state["tension_level"] += 20
                        if state["tension_level"] >= 100:
                            state["status"] = "boss_fight"
                            state["boss_task"] = random.choice(zadania_boss)
                        else:
                            state["status"] = "result"
                            kara = state["penalty"]
                            state["buyout_msg"] = f"🔄 KARTA VETO UŻYTA!<br><span style='font-size: 24px; color: #8c7a96;'><br>Role się odwracają!<br>Teraz {sedzia_imie} musi wykonać tę karę na partnerze:</span><br><br><span style='color: #ff4b4b;'>{kara}</span>"
                        st.rerun()

                if st.button("WYKONUJĘ KARĘ 😈", use_container_width=True, type="secondary"):
                    state["status"] = "result"; state["buyout_msg"] = ""
                    st.rerun()

            else:
                st.markdown("<div class='pilot-box' style='border-color: #4bd67b;'><div class='elegant-header'>Panel Sterowania</div><h1 class='gold-text' style='font-size: 24px; color: #4bd67b; margin-top: 15px;'>WYNIK NA EKRANIE TV</h1></div>", unsafe_allow_html=True)
                if st.button("NASTĘPNE PYTANIE ➔", use_container_width=True, type="primary"):
                    state["current_q"] += 1; state["status"] = "question"; state["buyout_msg"] = ""; state["penalty"] = ""
                    st.rerun()
        
        if st.button("RESETUJ GRĘ (ZACZNIJ OD NOWA)"):
            state["phase"] = "rules"; state["intro_q"] = 0; state["intro_gra"] = generuj_intro(); state["gra"] = generuj_gre(); state["current_q"] = 0; state["status"] = "question"
            state["ona_refusals"] = 0; state["on_refusals"] = 0; state["ona_shots"] = 0; state["on_shots"] = 0; state["ona_veto"] = 1; state["on_veto"] = 1; state["tension_level"] = 0; state["boss_task"] = ""
            state["penalty"] = ""; state["buyout_msg"] = ""
            st.rerun()
