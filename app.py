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
# 3. BAZA DANYCH (GIGANTYCZNA WERSJA TOTAL EXTREME 🔥🔥🔥)
# ==========================================

pytania_intro = [
    {"kto": "ONA", "tekst": "Zgadnij, w którym momencie naszej pierwszej randki pomyślałam, że chcę Cię pocałować?"},
    {"kto": "ON", "tekst": "Jak myślisz, co dokładnie poczułem, gdy pierwszy raz zobaczyłem Cię nago?"},
    {"kto": "ONA", "tekst": "Zgadnij, jaka Twoja, z pozoru nudna, cecha charakteru niesamowicie mi imponuje?"},
    {"kto": "ON", "tekst": "Jak myślisz, kiedy najczęściej łapię się na tym, że uśmiecham się sam do telefonu przez Ciebie?"},
    {"kto": "ONA", "tekst": "Gdybym to JA mogła urządzić nam sypialnię od nowa bez limitu gotówki, co bym tam wstawiła?"},
    {"kto": "ON", "tekst": "Zgadnij, co jest według MNIE naszym najbardziej 'toksycznym' wspólnym nawykiem?"},
    {"kto": "ONA", "tekst": "Jak myślisz, w jakich chwilach czuję się przy Tobie najbardziej krucha i delikatna?"},
    {"kto": "ON", "tekst": "Zgadnij, co JA uważam za swój największy wkład w rozwój naszego związku?"},
    {"kto": "ONA", "tekst": "Czy według mnie nasz związek to bardziej szalona jazda bez trzymanki, czy bezpieczna przystań?"},
    {"kto": "ON", "tekst": "Jak myślisz, czego w Tobie najbardziej zazdroszczą mi moi kumple?"},
    {"kto": "ONA", "tekst": "Zgadnij, jaki był najbardziej przełomowy moment w naszej relacji według MNIE?"},
    {"kto": "ON", "tekst": "Gdybym miał wymienić jedną rzecz, której nauczyłem się od Ciebie o seksie, co by to było?"},
    {"kto": "ONA", "tekst": "Jak myślisz, co we mnie najbardziej się uspokoiło, odkąd jesteśmy razem?"},
    {"kto": "ON", "tekst": "Zgadnij, jaka nasza wspólna kłótnia z przeszłości teraz bawi MNIE najbardziej?"},
    {"kto": "ONA", "tekst": "Gdybym miała wybrać jedną piosenkę na soundtrack do naszej dzisiejszej nocy, co bym wybrała?"},
    {"kto": "ON", "tekst": "Zgadnij, która Twoja wada jest dla mnie tak urocza, że nigdy bym jej nie zmienił?"},
    {"kto": "ONA", "tekst": "Jak myślisz, do jakiej jednej naszej wspólnej chwili najczęściej wracam myślami, gdy mam zły dzień?"},
    {"kto": "ON", "tekst": "Zgadnij, w jakiej codziennej, domowej czynności wyglądasz dla mnie najbardziej uroczo?"},
    {"kto": "ONA", "tekst": "Gdybym miała spędzić z Tobą cały dzień w łóżku bez seksu, jak myślisz, co byśmy robili?"},
    {"kto": "ON", "tekst": "Jak myślisz, czy według MNIE jesteśmy już w 100% dopasowani, czy wciąż się siebie uczymy?"},
    {"kto": "ONA", "tekst": "Zgadnij, jaka moja tajemnica z przeszłości była dla mnie najtrudniejsza do wyznania Ci?"},
    {"kto": "ON", "tekst": "Czy według MNIE lepsze są nasze głębokie rozmowy nocą, czy nasze milczenie w trasie?"},
    {"kto": "ONA", "tekst": "Zgadnij, za jaką Twoją cechę charakteru oddałabym wszystko, żeby mieć ją też u siebie?"},
    {"kto": "ON", "tekst": "Jak myślisz, jaki drobny, fizyczny szczegół na Twojej twarzy lubię najbardziej badać wzrokiem?"},
    {"kto": "ONA", "tekst": "Zgadnij, o czym pomyślałam po naszym absolutnie pierwszym pocałunku?"},
    {"kto": "ON", "tekst": "Czy według MNIE potrafisz mnie łatwo zmanipulować swoim urokiem?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy bardziej wzrusza mnie, gdy mnie bronisz przy innych, czy gdy pomagasz mi w ukryciu?"},
    {"kto": "ON", "tekst": "Jak myślisz, o jakim wspólnym wyjeździe marzę najbardziej w tym momencie?"},
    {"kto": "ONA", "tekst": "Gdybym mogła dać Ci jedną supermoc, jak myślisz, co bym dla Ciebie wybrała?"},
    {"kto": "ON", "tekst": "Zgadnij, z czego musiałbym najtrudniej zrezygnować, gdybyśmy zamieszkali na bezludnej wyspie?"}
]

toasty = [
    "Zdrowie za tych, którzy dziś rano obudzą się z zakwasami! 🥂",
    "Pijemy za mokre pościele i podrapane plecy! 😈",
    "Toast za to, żebyśmy jutro nie mogli patrzeć ludziom w oczy bez rumieńca! 🔥",
    "Zdrowie za każdego zrzuconego dzisiaj ciucha! 💦",
    "Pijemy za nasze najbrudniejsze, wciąż niespełnione fantazje! 🍷",
    "Toast za tego, kto dziś pierwszy zacznie błagać o więcej! 🍾",
    "Pijemy łyk prosto z ust partnera – bez rozlewania! 🥃",
    "Za orgazmy, o których nie śniło się nawet w filmach! 😈",
    "Toast za to, kto dziś będzie głośniej krzyczeć moje imię! 🤫",
    "Zdrowie za złamane zasady i zerwane hamulce! 🥂",
    "Pijemy ze skrzyżowanymi rękami za najostrzejszy seks w historii tego domu! 🔥",
    "Za każde uderzenie, jęk i kroplę śliny, która dziś padnie! 💦",
    "Toast za dominację, uległość i wszystko to, co pomiędzy! 😈",
    "Zdrowie za to, żeby sąsiedzi jutro patrzyli na nas z oburzeniem! 🍷",
    "Wypijmy za zwierzęcy instynkt, który zaraz przejmie kontrolę! 🍾",
    "Za Ciebie nago – to jedyny widok, jaki mnie dziś interesuje! 🥃"
]

p1 = [
    {"kto": "ONA", "tekst": "Zgadnij, na co zwracam największą uwagę, gdy widzę Cię wychodzącego spod prysznica?"},
    {"kto": "ON", "tekst": "Jak myślisz, co w Twoim głosie sprawia, że od razu mam na Ciebie ochotę?"},
    {"kto": "ONA", "tekst": "W jakim konkretnym momencie dnia MÓJ poziom pożądania do Ciebie jest zazwyczaj najwyższy?"},
    {"kto": "ON", "tekst": "Zgadnij, w jakim Twoim codziennym ubraniu (nie bieliźnie) wyglądasz dla mnie najbardziej 'na pożarcie'?"},
    {"kto": "ONA", "tekst": "Jak myślisz, czy kręci MNIE bardziej to, jak pachniesz rano w łóżku, czy wieczorem przed wyjściem?"},
    {"kto": "ON", "tekst": "Co według MNIE jest najseksowniejszym ruchem, jaki wykonujesz nieświadomie?"},
    {"kto": "ONA", "tekst": "Zgadnij, co JA czuję, gdy w tłumie znajomych rzucasz mi to jedno, konkretne spojrzenie?"},
    {"kto": "ON", "tekst": "Gdybym mógł patrzeć tylko na jedną część Twojej twarzy podczas zbliżenia, co bym wybrał?"},
    {"kto": "ONA", "tekst": "Jak myślisz, co jest MOIM ulubionym wspomnieniem z naszej gry wstępnej z czasów, gdy dopiero się poznawaliśmy?"},
    {"kto": "ON", "tekst": "Zgadnij, czy wolałbym spędzić godzinę na całowaniu Twojej szyi, czy Twoich wewnętrznych ud?"},
    {"kto": "ONA", "tekst": "Jak myślisz, czy w łóżku lubię, gdy to Ty jesteś głośniejszy, czy gdy ja dominuję wokalnie?"},
    {"kto": "ON", "tekst": "Zgadnij, co we MNIE buzuje, gdy widzę, że inni faceci zerkają na Ciebie na ulicy?"},
    {"kto": "ONA", "tekst": "Wybierz: czy JA wolę być mocno dociśnięta do materaca, czy delikatnie przypięta do ściany?"},
    {"kto": "ON", "tekst": "Jak myślisz, co czuję, gdy potajemnie wsuwasz mi dłoń na krocze pod stołem w restauracji?"},
    {"kto": "ONA", "tekst": "Zgadnij, co w Twoich pocałunkach sprawia, że całkowicie tracę grunt pod nogami?"},
    {"kto": "ON", "tekst": "Czy według MNIE najlepszy seks to ten zaplanowany i powolny, czy brudny i spontaniczny?"},
    {"kto": "ONA", "tekst": "Zgadnij, jak reaguję w głowie, gdy specjalnie zakładasz dresy, które opinają to, co trzeba?"},
    {"kto": "ON", "tekst": "Jak myślisz, w jakich momentach jestem z Ciebie najbardziej dumny jako z mojej partnerki?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy podnieca MNIE myśl o tym, że mógłbyś obserwować mnie z ukrycia, gdy się przebieram?"},
    {"kto": "ON", "tekst": "Co sprawia, że JA czuję się przy Tobie jak niepowstrzymany samiec alfa?"},
    {"kto": "ONA", "tekst": "Jak myślisz, czy według MNIE częściej Ty inicjujesz seks, czy ja wysyłam dyskretne sygnały?"},
    {"kto": "ON", "tekst": "Zgadnij, która z Twoich fryzur (spięte/rozpuszczone/mokre) działa na mnie najbardziej zwierzęco?"},
    {"kto": "ONA", "tekst": "Co we mnie płonie, gdy widzę Twoje dłonie zaciśnięte na kierownicy podczas szybkiej jazdy?"},
    {"kto": "ON", "tekst": "Zgadnij, jak reaguję w myślach, gdy schylasz się po coś w obcisłych spodniach?"},
    {"kto": "ONA", "tekst": "Jak myślisz, czy wolałabym, żebyś całował mnie mocno i agresywnie w deszczu, czy namiętnie w windzie?"},
    {"kto": "ON", "tekst": "Co JA czuję, gdy rano przeciągasz się leniwie i widzę kawałek Twojego ciała?"},
    {"kto": "ONA", "tekst": "Zgadnij, co wyobrażam sobie, gdy stoisz nade mną, gdy ja np. siedzę na krześle?"},
    {"kto": "ON", "tekst": "Jak myślisz, czy kręci MNIE, gdy publicznie, niby przypadkiem, ocierasz się o moje krocze?"},
    {"kto": "ONA", "tekst": "Zgadnij, z jakiego miejsca na moim ciele jestem najbardziej dumna, gdy staję przed Tobą nago?"},
    {"kto": "ON", "tekst": "Co w Twoim uśmiechu daje mi natychmiastowy sygnał, że masz niegrzeczne myśli?"}
]

p2 = [
    {"kto": "ONA", "tekst": "Zgadnij, czy wolę, gdy zlizujesz alkohol z mojej szyi, czy z mojego pępka?"},
    {"kto": "ON", "tekst": "Jak myślisz, które miejsce na Twoim ciele sprawia MI największą trudność, by przestać je pieścić?"},
    {"kto": "ONA", "tekst": "Zgadnij, co JA wolę: kiedy zostawiasz na mnie wyraźną malinkę, czy tylko mocny ślad zębów?"},
    {"kto": "ON", "tekst": "Jak myślisz, czy kręci mnie, gdy celowo nosisz spódniczkę bez majtek na naszą randkę?"},
    {"kto": "ONA", "tekst": "Zgadnij, jaki rodzaj dotyku MÓJ kark lubi najbardziej: powolne gładzenie, czy mocne chwycenie?"},
    {"kto": "ON", "tekst": "Co JA czuję, gdy siedzisz mi na kolanach i czuję Twój wilgotny oddech na moim uchu?"},
    {"kto": "ONA", "tekst": "Jak myślisz, od czego powinieneś zacząć, żebym w 3 minuty błagała Cię o więcej?"},
    {"kto": "ON", "tekst": "Zgadnij, w jakiej pozie wyglądasz dla MNIE tak dobrze, że ledwo nad sobą panuję?"},
    {"kto": "ONA", "tekst": "Wybierz: czy JA wolę, gdy dręczysz mnie przez godzinę bez finału, czy gdy od razu przechodzisz do setna?"},
    {"kto": "ON", "tekst": "Jak myślisz, co mnie bardziej nakręca: gdy szepczesz mi obelgi, czy czułe, zakazane słówka?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy podnieca mnie myśl o seksie w przymierzalni w pełnym centrum handlowym?"},
    {"kto": "ON", "tekst": "Co JA wolę u Ciebie: totalną gładkość w miejscach intymnych, czy naturalność?"},
    {"kto": "ONA", "tekst": "Jak myślisz, co sobie wyobrażam, gdy mocno zaciskam uda podczas naszego pocałunku?"},
    {"kto": "ON", "tekst": "Zgadnij, czy wolałbym zobaczyć Cię w tanim, kiczowatym stroju pokojówki, czy w samej siateczce?"},
    {"kto": "ONA", "tekst": "Czy według mnie Twoje dłonie sprawdzają się lepiej w masażu moich pośladków, czy moich piersi?"},
    {"kto": "ON", "tekst": "Zgadnij, w jakim pomieszczeniu w naszym domu marzy mi się wzięcie Cię od tyłu?"},
    {"kto": "ONA", "tekst": "Jak myślisz, czy rajcuje mnie wizja tego, że ktoś słyszy moje jęki przez ścianę?"},
    {"kto": "ON", "tekst": "Co nakręca MNIE bardziej: gdy bierzesz sprawy w swoje ręce, czy gdy jesteś całkowicie uległa?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy lubię być podduszana w trakcie gry wstępnej?"},
    {"kto": "ON", "tekst": "Jak myślisz, z jakiej części mojego ciała najchętniej zmyłbym z Ciebie olejek do masażu własnym językiem?"},
    {"kto": "ONA", "tekst": "Zgadnij, jak reaguję w środku, gdy podczas całowania nagle wciskasz dłoń między moje uda?"},
    {"kto": "ON", "tekst": "Jak myślisz, czy kręcą mnie sytuacje, w których każę Ci się rozebrać, a sam pozostaję w pełni ubrany?"},
    {"kto": "ONA", "tekst": "Zgadnij, co podnieca MNIE bardziej: Twój szorstki zarost drapiący moje udo, czy miękki dotyk warg?"},
    {"kto": "ON", "tekst": "Jak myślisz, czy wyobrażałem sobie kiedyś, że kocha się z nami moja ulubiona aktorka porno?"},
    {"kto": "ONA", "tekst": "Zgadnij, z czego najszybciej moknę: z tego, co do mnie mówisz, czy z tego, jak na mnie patrzysz?"},
    {"kto": "ON", "tekst": "Czy według MNIE jesteś wystarczająco agresywna w łóżku, czy chciałbym, żebyś częściej rzucała mną o ścianę?"},
    {"kto": "ONA", "tekst": "Zgadnij, jak reaguję na myśl o tym, że mógłbyś zdjąć ze mnie majtki samymi zębami przy zgaszonym świetle?"},
    {"kto": "ON", "tekst": "Jak myślisz, czy rajcuje MNIE, gdy celowo nie pozwalasz mi dotknąć swoich piersi przez dłuższy czas?"},
    {"kto": "ONA", "tekst": "Zgadnij, w którym momencie gry wstępnej zazwyczaj mam ochotę krzyczeć z bezsilności?"},
    {"kto": "ON", "tekst": "Co według MNIE jest najbardziej bezwstydną pozycją, w jakiej kiedykolwiek mnie prowokowałaś?"}
]

p3 = [
    {"kto": "ONA", "tekst": "Zgadnij, czy kręci MNIE myśl o tym, że weźmiesz mnie tak brutalnie, że aż się popłaczę z rozkoszy?"},
    {"kto": "ON", "tekst": "Jak myślisz, w jakiej pozycji Twój tyłek wygląda dla MNIE najbardziej wyuzdanie i pociągająco?"},
    {"kto": "ONA", "tekst": "Zgadnij, jaki z moich fetyszy uważam za zbyt ostry, żebyśmy robili to codziennie?"},
    {"kto": "ON", "tekst": "Co JA czuję, gdy zmuszam Cię do patrzenia mi prosto w oczy, podczas gdy we mnie dochodzisz?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy wolę z połykiem (do końca), czy żebyś skończył mi na twarzy/dekolcie?"},
    {"kto": "ON", "tekst": "Jak myślisz, czy rajcuje MNIE seks analny, czy uważam to za coś, czego wolę unikać?"},
    {"kto": "ONA", "tekst": "Zgadnij, jakie wyzwisko lub brudne słowo wypowiedziane przez Ciebie uderza MNIE prosto w strefę V?"},
    {"kto": "ON", "tekst": "Czy według MNIE głębokie gardło (deepthroat) to absolutny szczyt przyjemności z Twojej strony?"},
    {"kto": "ONA", "tekst": "Jak myślisz, co czuję, gdy w środku ostrego seksu chwytasz mnie za włosy i ciągniesz do tyłu?"},
    {"kto": "ON", "tekst": "Zgadnij, czy pociąga mnie myśl o zostawieniu na Twoich pośladkach siniaków od mocnych klapsów?"},
    {"kto": "ONA", "tekst": "Czy według MNIE wibrator podczas stosunku to cudowny dodatek, czy znak, że robisz coś za słabo?"},
    {"kto": "ON", "tekst": "Jak myślisz, co we mnie wybucha, gdy błagasz mnie o to, żebym już w Ciebie wszedł?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy fantazjowałam kiedyś o tym, że każesz mi się onanizować na Twoich oczach i nie wolno mi przestać?"},
    {"kto": "ON", "tekst": "Czy kręci mnie zlizywanie mojego własnego nasienia z Twojego ciała?"},
    {"kto": "ONA", "tekst": "Jak myślisz, czy wolałabym używać na Tobie skórzanego pejczyka, czy być nim bita?"},
    {"kto": "ON", "tekst": "Zgadnij, w której pozycji JA mam poczucie, że jesteś moją całkowitą własnością?"},
    {"kto": "ONA", "tekst": "Czy pociąga MNIE myśl, że przemycasz do mnie wibrator w miejscu publicznym i masz do niego pilota?"},
    {"kto": "ON", "tekst": "Jak myślisz, czy wolałbym zobaczyć Cię w łóżku z inną kobietą, czy z inną parą?"},
    {"kto": "ONA", "tekst": "Zgadnij, jak reaguje MOJE ciało na myśl o byciu związaną i zakneblowaną (zgodnie z safeword)?"},
    {"kto": "ON", "tekst": "Co według MNIE jest najbardziej bezwstydną rzeczą, do jakiej kiedykolwiek Cię zmusiłem?"},
    {"kto": "ONA", "tekst": "Jak myślisz, czy pociąga MNIE wizja tego, że po wszystkim na moim ciele zostają Twoje soki?"},
    {"kto": "ON", "tekst": "Zgadnij, czy według MNIE bycie spoliczkowaną podczas orgazmu wzmocniłoby u Ciebie doznania?"},
    {"kto": "ONA", "tekst": "Co we MNIE pęka, gdy z premedytacją zatrzymujesz się sekundy przed MOIM orgazmem?"},
    {"kto": "ON", "tekst": "Jak myślisz, w którym momencie penetracji czuję, że absolutnie nie mogę się już kontrolować?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy bardziej rajcuje mnie wizja bycia wziętą siłą (konsensualne CNC), czy powolnego uwodzenia?"},
    {"kto": "ON", "tekst": "Co według MNIE powstrzymuje nas przed wypróbowaniem najdziwniejszych rzeczy z branży porno?"},
    {"kto": "ONA", "tekst": "Jak myślisz, jak bardzo lubię, kiedy zmuszasz mnie do połykania w całości?"},
    {"kto": "ON", "tekst": "Zgadnij, czy wyobrażałem sobie kiedyś, że pieprzę Cię przed wielkim lustrem, patrząc tylko na Twoje łzy rozkoszy?"},
    {"kto": "ONA", "tekst": "Czy podnieca MNIE myśl o byciu uległą suką pod Twoimi rozkazami na całą noc?"},
    {"kto": "ON", "tekst": "Jak myślisz, co dokładnie chciałbym zrobić z Twoim ciałem po tym, jak już dojdziesz 3 razy?"}
]

p4 = [
    {"kto": "ONA", "tekst": "Zgadnij, czy podnieca MNIE myśl o zlizaniu Twojego nasienia z moich własnych palców lub ust?"},
    {"kto": "ON", "tekst": "Jak myślisz, czy kręciłaby MNIE sytuacja, w której oddaję Cię innemu facetowi na jedną noc, a sam tylko patrzę (cuckold)?"},
    {"kto": "ONA", "tekst": "Zgadnij, jak bym zareagowała, gdybyś nagle plunął mi do ust podczas ostrego, brudnego seksu?"},
    {"kto": "ON", "tekst": "Czy kręci MNIE wizja, w której traktuję Cię jak zwykłą dziwkę, używając najgorszych obelg?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy zgodziłabym się na 'złoty deszcz' w prysznicu, gdybyś mnie o to poprosił?"},
    {"kto": "ON", "tekst": "Jak myślisz, co bym zrobił, gdybyś założyła obrożę ze smyczą i kazała wyprowadzić się nago do przedpokoju?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy fantazjowałam o byciu używaną jednocześnie we wszystkich trzech dziurkach?"},
    {"kto": "ON", "tekst": "Czy podnieca mnie myśl o seksie w plenerze w ciągu dnia, gdzie każdy może nas nakryć?"},
    {"kto": "ONA", "tekst": "Jak myślisz, czy z przyjemnością przyjęłabym na twarz i oczy Twój gorący finał?"},
    {"kto": "ON", "tekst": "Zgadnij, co czuję na myśl o robieniu Ci dobrze (oral), zaraz po tym, jak skończyliśmy ostry anal?"},
    {"kto": "ONA", "tekst": "Czy podnieca MNIE bycie filmowaną z bliska, gdy dojście wykręca moją twarz w brzydki, zwierzęcy grymas?"},
    {"kto": "ON", "tekst": "Jak myślisz, czy rajcowałoby MNIE uprawianie seksu z Tobą, podczas gdy Ty masz miesiączkę, a my robimy krwawy bałagan?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy kręci mnie odgrywanie scenariusza gwałtu (cnc) z całkowitą bezradnością?"},
    {"kto": "ON", "tekst": "Czy wyobrażałem sobie kiedyś, że budzę Cię rano, gwałtownie wchodząc w Ciebie bez gry wstępnej?"},
    {"kto": "ONA", "tekst": "Jak myślisz, czy ekscytuje mnie wizja bycia wystawioną nago w oknie na widok sąsiadów?"},
    {"kto": "ON", "tekst": "Zgadnij, czy podnieca mnie myśl o peggingu (gdy to Ty używasz strap-ona na mnie)?"},
    {"kto": "ONA", "tekst": "Co bym powiedziała na to, gdybyś kazał mi załatwić się (siku) na Twoich oczach z otwartymi drzwiami do toalety?"},
    {"kto": "ON", "tekst": "Czy podnieca MNIE myśl o byciu całkowitym niewolnikiem pod Twoimi butami (np. lizanie Twoich szpilek)?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy marzy mi się orgia z wieloma mężczyznami (gangbang), w której Ty jesteś reżyserem?"},
    {"kto": "ON", "tekst": "Jak myślisz, co bym zrobił, gdybyś zasnęła, a ja miałbym ochotę po prostu użyć Twojego ciała jako zabawki?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy pociąga mnie myśl o byciu wykorzystywaną przez nieznajomego w barowej toalecie, podczas gdy Ty stoisz na czatach?"},
    {"kto": "ON", "tekst": "Jak myślisz, w jakiej skali od 1 do 10 kręci MNIE myśl o Twoim orgazmie wielokrotnym aż do omdlenia?"},
    {"kto": "ONA", "tekst": "Czy wyobrażałam sobie kiedyś, że uderzasz mnie mocno w twarz w samym środku ostrego rżnięcia?"},
    {"kto": "ON", "tekst": "Zgadnij, co bym poczuł, gdybyś zażyczyła sobie bycia zalaną nasieniem przez kilku moich kumpli?"},
    {"kto": "ONA", "tekst": "Jak myślisz, czy rajcuje MNIE upokarzanie publiczne? (np. bycie zmuszoną do pokazania piersi na ulicy)?"},
    {"kto": "ON", "tekst": "Czy według mnie seks w kościele lub innym zakazanym miejscu to profanacja, czy ostateczne podniecenie?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy kiedykolwiek masturbowałam się myśląc o tym, że patrzysz na mnie ukrytą kamerą?"},
    {"kto": "ON", "tekst": "Jak myślisz, co jest najbardziej chorą, popieprzoną rzeczą, jaką wpisałem kiedykolwiek w wyszukiwarkę porno?"},
    {"kto": "ONA", "tekst": "Czy podnieca MNIE bycie zmuszoną do połykania, nawet gdy krztuszę się ze łzami w oczach?"},
    {"kto": "ON", "tekst": "Zgadnij, czy kiedykolwiek miałem ochotę wyruchać Cię tak mocno, by zostawić Cię niemogącą chodzić przez cały dzień?"}
]

kary_l1 = [
    "Splećcie palce. Patrzcie sobie głęboko w oczy przez 2 minuty – kto pierwszy odwróci wzrok, wykonuje dodatkową karę.",
    "Pocałuj partnera w jego najwrażliwsze, NIE-seksualne miejsce na ciele, i trzymaj tam usta przez 30 sekund.",
    "Wymasuj delikatnie szczękę, kark i skronie partnera opuszkami palców przez 60 sekund.",
    "Usiądź za partnerem i powoli wodź nosem i ustami po jego/jej szyi. Żadnego gryzienia.",
    "Szeptem na ucho powiedz partnerowi dokładnie, co najbardziej lubisz w jego/jej nagim ciele.",
    "Przytulcie się tak mocno, by nie było między Wami milimetra wolnej przestrzeni. Oddychajcie wspólnie przez 90 sekund.",
    "Rozepnij koszulę/bluzkę partnera tylko o 2 guziki. Pocałuj obnażony kawałek skóry.",
    "Pociągnij delikatnie płatek ucha partnera wargami, a potem dmuchnij w niego ciepłym powietrzem.",
    "Poproś partnera o dłoń. Ucałuj każdą kostkę i wnętrze dłoni, patrząc wyzywająco w oczy.",
    "Zawiąż sobie oczy (albo mocno je zamknij) i pozwól partnerowi wodzić palcami po Twojej twarzy przez 60 sekund.",
    "Delikatnie przejedź paznokciami po całych plecach partnera – od karku do lędźwi, 10 razy w dół.",
    "Zliż kroplę potu lub drinka ze skroni lub szyi partnera.",
    "Pocałuj partnera w oba policzki, w nos, a na koniec daj namiętny, głęboki pocałunek bez języka.",
    "Zbliż swoje usta do ust partnera tak, by się niemal stykały. Rozmawiajcie w tej odległości przez 3 rundy.",
    "Ściągnij skarpetki/buty partnera i wymasuj mu/jej stopy, używając swoich dłoni i ust.",
    "Obejmij twarz partnera obiema dłońmi i zmuś go do uśmiechu najsłodszym buziakiem, na jakiego Cię stać.",
    "Niech partner/partnerka wsunie chłodne dłonie pod Twoją koszulkę na plecach. Musisz wytrzymać bez wzdrygnięcia.",
    "Złóż mokry pocałunek dokładnie w dołku między obojczykami partnera.",
    "Usiądź na udach partnera (przodem do niego) i nie schodź do końca fazy pierwszego poziomu.",
    "Zatańcz z partnerem do wyimaginowanej, powolnej piosenki, wtulając głowę w klatkę piersiową/piersi na minutę.",
    "Pogryź bardzo delikatnie kciuk partnera, utrzymując stały kontakt wzrokowy.",
    "Połóż głowę na kolanach partnera i pozwól mu/jej masować Twoją głowę i włosy przez 2 minuty.",
    "Daj partnerowi do zjedzenia kawałek jedzenia (albo lód) z Twoich własnych ust.",
    "Zamknij oczy. Partner ma 3 próby, by pocałować Cię w miejsce, które sam wybierze, a Ty musisz zgadnąć gdzie to było.",
    "Uklęknij przed partnerem/partnerką, obejmij go/ją w pasie i wtul twarz w brzuch na okrągłą minutę.",
    "Muskaj delikatnie rzęsami policzek partnera (tzw. pocałunek motyla).",
    "Splećcie nogi pod stołem, trąc o siebie łydkami przez 3 kolejne pytania.",
    "Złap partnera za biodra i dociśnij lekko do siebie, głęboko wciągając powietrze jego zapachem na szyi.",
    "Pocałuj każdy palec u dłoni partnera, wkładając opuszek na sekundę do swoich ust.",
    "Połóż rękę partnera na swoim sercu, spójrz mu w oczy i nie odzywaj się ani słowem przez 45 sekund.",
    "Wymasuj wewnętrzną część przedramienia partnera dwoma kciukami – to ekstremalnie wrażliwe miejsce.",
    "Odwróć głowę partnera w swoją stronę, trzymając go za brodę i gap się w milczeniu na jego usta.",
    "Niech partner zdejmie Ci bluzę/sweter tak wolno, jak tylko potrafi.",
    "Przejedź bardzo powoli paznokciem wzdłuż linii żuchwy partnera.",
    "Dmuchnij delikatnie w kark partnera z tyłu tak, by wywołać u niego gęsią skórkę."
]

kary_l2 = [
    "Zdejmij górną część swojej garderoby (koszulka/bluzka). Zostajesz tak do końca rundy.",
    "Zdejmij jeden element ubrania partnera/partnerki, używając wyłącznie swoich zębów.",
    "Połóż się. Partner przez minutę ma prawo wodzić dłońmi po Twoim ciele, ale omija strefy intymne. Nie wolno Ci go dotknąć.",
    "Pocałuj wewnętrzną stronę uda partnera – jak najwyżej się odważysz, bez zdejmowania bielizny.",
    "Ugryź partnera w kark na tyle mocno, by zostawić ślad zębów, a potem zliż to miejsce.",
    "Wsuń dłoń w spodnie/pod spódnicę partnera, z tyłu, i namiętnie ugniataj nagie pośladki przez 60 sekund.",
    "Usiądź okrakiem na twarzy/kolanach partnera (w ubraniu) i zacznij powoli, rytmicznie się ocierać (grinding) przez 2 minuty.",
    "Nalej kroplę napoju na swoje piersi/klatkę piersiową i każ partnerowi to zлизаć.",
    "Rozepnij spodnie partnera. Zsuń je do połowy ud. Zostają tak do kolejnej kary.",
    "Złap partnera za nadgarstki, przyszpil je do oparcia kanapy/ściany i namiętnie zdominuj go głębokim pocałunkiem z językiem.",
    "Rozepnij biustonosz/koszulę, chwyć dłoń partnera i przyciśnij ją mocno do swojego ciała w tym miejscu na pełną minutę.",
    "Złóż serię mokrych pocałunków biegnących od pępka w dół, zatrzymując się dosłownie milimetr nad krawędzią bielizny.",
    "Przesuwaj językiem wokół sutków partnera (przez ubranie lub pod nim) przez okrągłą minutę.",
    "Wsuń palce za pasek spodni partnera i szarpnij go agresywnie w swoją stronę, szepcząc coś brudnego.",
    "Zawiąż oczy partnerowi czymkolwiek masz pod ręką. Pozostaje ślepy do następnego wylosowania kary.",
    "Zjedz kostkę lodu, a następnie użyj swoich lodowatych ust do zaspokojenia szyi i klatki piersiowej partnera.",
    "Odwróć partnera tyłem, przytul się mocno, ocierając kroczem o jego/jej pośladki przez 2 minuty (w ubraniu).",
    "Zrób partnerowi 2-minutowy 'suchy' striptiz (lap dance), robiąc z jego/jej ciałem, co tylko zechcesz.",
    "Złap partnera za gardło (lekkie podduszanie) podczas 30-sekundowego, ostrego pocałunku.",
    "Oprzyj nogę na kanapie/krześle i pozwól partnerowi masować swoje udo aż po pachwinę.",
    "Przyłóż usta do ucha partnera i wydaj z siebie najgłośniejszy jęk rozkoszy, na jaki Cię stać w tej chwili.",
    "Rozchyl ubranie na piersiach/torsie partnera i 'wymyj' ten kawałek skóry własnym językiem.",
    "Uderz partnera lekko w pośladek z liścia (spank) z dźwięcznym klaśnięciem. Powtórz 5 razy.",
    "Niech partner potrze Twoje wewnętrzne uda swoimi własnymi udami w silnym uścisku.",
    "Zmuś partnera, by położył się na plecach, po czym obślinił swój własny palec i włożył Ci go do ust do possania.",
    "Rozepnij swój zamek w spodniach i pozwól partnerowi wsunąć tam jeden palec na minutę. Bez ruchu.",
    "Przyciśnij partnera do ściany swoim ciałem, włóż mu kolano między uda i całuj agresywnie.",
    "Użyj kostki lodu z drinka i przejedź nią od szyi prosto między piersi/po brzuchu partnera.",
    "Będąc w samej bieliźnie na dole, usiądź na twarzy partnera (bez dotykania narządami) i każ mu wdychać zapach przez 60 sekund.",
    "Zdejmij swoje majtki bez zdejmowania spodni/sukienki (albo zrób to partnerowi) i odrzuć w kąt pokoju.",
    "Pocałuj partnera na tyle mocno i wilgotno, by po rozłączeniu między Waszymi wargami rozciągnęła się nić śliny.",
    "Zliż sól/cukier z przedramienia partnera po uprzednim polizaniu go.",
    "Wsuń dłoń we włosy partnera i pociągnij jego głowę do tyłu, patrząc z góry prosto w oczy.",
    "Przyłóż mokry język do szyi partnera i zrób mu potężną, widoczną malinkę.",
    "Pozwól partnerowi zawiązać Twoje ręce paskiem z przodu na kolejne 3 pytania."
]

kary_l3 = [
    "Zdejmijcie oboje dół ubrań (spodnie/spódnice). Gracie dalej w samej bieliźnie.",
    "Seks oralny przez ubranie/bieliznę – 2 minuty ocierania ustami i językiem przez materiał. Zostaw partnera mokrego.",
    "Wsuń rękę do majtek partnera od przodu. Złap to, co masz złapać. Masuj agresywnie przez pełne 2 minuty.",
    "Zdejmij partnerce biustonosz/partnerowi koszulkę samymi rękami z tyłu. Zliż i ssij sutki przez okrągłą minutę.",
    "Wypnij się! Partner ma prawo wymierzyć 10 mocnych, soczystych klapsów w Twoje gołe pośladki.",
    "Odsłoń swoje miejsce intymne. Partner ma za zadanie zadowolić Cię językiem przez 60 sekund. Nastawcie stoper.",
    "Zejdź w dół. Użyj ust i dłoni na partnerze przez 2 minuty, ale absolutnie NIE POZWÓL mu dojść. To czysty teasing.",
    "Nałóż na sutki lub krocze partnera kostkę lodu i pozwól jej tam całkowicie stopnieć.",
    "Uklęknij przed partnerem z otwartymi ustami. Partner decyduje, czy włoży tam palce, czy coś innego na minutę.",
    "Odwróć partnera na brzuch. Zdejmij mu bieliznę i poliż go prosto w odbyt (rimming) lub bardzo blisko, przez minutę.",
    "Wejdź na partnera (na jeźdźca), ale bez bielizny. Ocierajcie się wilgotnymi narządami o siebie przez 2 minuty bez wejścia.",
    "Zwiąż ręce partnera paskiem. Pokaż mu wibrator/swoje palce i pieść go w każdym miejscu POZA strefą V przez 3 minuty.",
    "Podejdź do ściany i rozsuń nogi. Partner wchodzi w Ciebie palcami (lub dłonią) tak głęboko i szybko, jak tylko potrafi na 60 sekund.",
    "Partner rozsuwa Twoje nogi i pluje Ci (lekko) na krocze, a następnie rozsmarowuje to własnymi palcami.",
    "Zdejmij całą swoją bieliznę bez dotykania jej dłońmi (użyj stóp, ocierania o kanapę lub partnera).",
    "Zliż alkohol (lub cokolwiek słodkiego) bezpośrednio z narządów intymnych partnera.",
    "Masturbuj się na oczach partnera, patrząc mu w oczy. On/ona mówi Ci, czy masz zwolnić, czy przyspieszyć przez 2 minuty.",
    "Głębokie gardło (Deepthroat). Weź partnera do ust tak głęboko, aż zakrztusisz się lub zaszklą Ci się oczy.",
    "Rozchyl pośladki partnera i złóż gorący, długi pocałunek tuż nad odbytem.",
    "Wymuś pozycję 69, w pełnym ubraniu lub bez. Robicie sobie dobrze nawzajem przez pełne 3 minuty stopera.",
    "Posadź partnera na blacie. Wsadź w nią palce/w niego dłoń, a potem zmuś do zlizania własnych soków z Twojej ręki.",
    "Zaciśnij dłonie na gardle partnera (choking, bezpiecznie) i zmuś go do ssania Twoich palców.",
    "Rozbierz się do naga i zaprezentuj partnerowi przez 2 minuty pozy, w których wolałbyś/wolałabyś być teraz brany/a.",
    "Błagaj partnera o litość lub orgazm, nazywając go najbardziej obleśnymi słowami, jakie znasz.",
    "Nie masz prawa dotykać swoich narządów, dopóki partner nie wejdzie w Ciebie i nie skończy. Kara przechodzi na całą resztę gry.",
    "Włóż dwa palce do ust partnera, by je obślinił, a następnie włóż je prosto w siebie (lub partnera) z powrotem.",
    "Połóż się nago. Partner spuszcza krople gorącego wosku ze świecy (lub lód) w okolicach Twoich piersi i ud.",
    "Piesek! Zdejmujesz bieliznę, odwracasz się, wypinasz i czekasz. Partner wymierza Ci 5 ostrych ciosów skórzanym paskiem.",
    "Użyj jakiejkolwiek zabawki erotycznej przed oczami partnera przez 2 minuty, ale nie możesz wydać żadnego dźwięku.",
    "Partner zdejmuje Ci bieliznę i rozsuwa uda. Masz w tym czasie zadzwonić do jakiejś pizzerii i zachować normalny głos, podczas gdy partner Cię pieści.",
    "Siedź na kolanach partnera. Partner ssie Twoje piersi/sutki z całej siły przez 2 minuty. Możesz tylko jęczeć.",
    "Podnieś koszulkę. Partner rysuje po Twoim ciele szminką lub jedzeniem wulgarny napis. Zostawiasz to do końca gry.",
    "Połóż się i podciągnij kolana do klatki piersiowej. Partner rozchyla Cię dłońmi i zlizuje soki niczym zwierzę z miski na wodę.",
    "Ssij zabawkę (wibrator, dildo) na oczach partnera przez minutę, patrząc w górę błagalnym wzrokiem.",
    "Partner pluje Ci prosto w otwarte usta. Musisz to połknąć patrząc mu w oczy."
]

kary_l4 = [
    "JESTEŚCIE NAGO. Zdejmujecie absolutnie wszystko. Kto się sprzeciwi, pije całego shota czystej wódki.",
    "Penetracja! Wchodzisz w partnera w dowolnej pozycji. Macie 3 minuty dzikiego pieprzenia, zanim wrócicie do pytań.",
    "Face-sitting. Połóż się płasko. Partner siada nagim kroczem prosto na Twojej twarzy. Zaspokajasz go/ją przez 2 minuty pod ciężarem.",
    "Edging (kontrola orgazmu). Doprowadź partnera oralnie/manualnie do samego, ostatecznego skraju i natychmiast przestań. Zostaw go z bólem na 2 rundy.",
    "Weź partnera na pieska. Złap go mocno za włosy i uderzaj w pośladki podczas ostrego wejścia przez 3 minuty.",
    "Seks oralny na maksa. Połykasz lub przyjmujesz finał na twarz. Bez wymówek, to jest ten moment.",
    "Odwróć partnera na brzuch i rozsuń pośladki. Użyj języka, palców (lub czegoś więcej, jeśli macie na to ochotę) w anale na 2 minuty.",
    "Rozłóż nogi partnerki. Plujesz prosto na palce i wchodzisz trzema palcami, robiąc to tak głośno i wulgarnie jak się da.",
    "Złap partnera mocno za gardło. Zmuś go, by patrzył w dół, jak na niego/nią sikasz (Złoty Deszcz - tylko pod prysznicem/w wannie) ALBO plujesz na jego krocze.",
    "Partner leży. Stajesz nad nim, masturbujesz się i kończysz bezpośrednio na jego klatkę piersiową/twarz.",
    "Załóż pętlę ze smyczy/krawata na szyję partnera. Wyprowadź go na czworakach do sypialni. Jesteście zwierzętami przez 5 minut.",
    "Zrób partnerowi brutalne głębokie gardło, używając obu rąk do przytrzymania głowy, narzucając zwierzęce tempo.",
    "Zmuś uległego partnera, by na kolanach błagał Cię o pozwolenie na dotknięcie Twojego krocza językiem.",
    "Zwiąż partnera całkowicie (ręce i nogi, jeśli to możliwe). Wykorzystaj każdą dostępną zabawkę na najwyższych obrotach przez 3 minuty. On/ona musi krzyczeć.",
    "Przerzuć partnera przez kanapę/krzesło i weź go na stojąco w najbardziej upokarzającej pozycji przez 2 minuty.",
    "Usiądź partnerowi na twarzy, odwrócony/a tyłem. Ma zlizywać i ssać każdy centymetr od tyłu przez okrągłą minutę.",
    "Zadaj partnerowi ból (ostre spankowanie pasem, dłonią) na tyle mocno, by błagał o litość. Potem pocałuj to miejsce.",
    "Podejdź do okna (upewnij się, że nie łamiecie prawa), oprzyj partnera o szybę i zrób mu palcówkę/wejdź od tyłu tak, by mógł Was ktoś zobaczyć.",
    "Rozkracz partnera. Użyj wibratora/zabawki na łechtaczce lub anale i nie przerywaj, dopóki partner nie dojdzie trzęsąc się z rozkoszy.",
    "Przyjmij na kolanach wszystko, co partner ma Ci do zaoferowania ustami, połykając każdy dźwięk i płyn.",
    "Zmuś partnera, by lizał i ssał Twoje palce u stóp, a potem użyj tej samej stopy do masażu jego narządów intymnych.",
    "Włóż partnerowi wibrator/korek (jeśli akceptujecie) do anusa i grajcie z tym włączonym gadżetem do końca wieczoru.",
    "Zepchnij partnera na podłogę. Wejdź na niego i zmuś do zrobienia Ci dobrze (oral), plując mu do ust w trakcie.",
    "Doprowadź się samemu do orgazmu na oczach partnera w zaledwie 3 minuty. Partner może Cię tylko lekko podduszać i obrażać.",
    "Złap partnera za włosy, zepchnij na kolana. Niech otworzy usta, a Ty opluj mu twarz lub do ust, nakazując bycię posłusznym.",
    "Rimming (lizanie odbytu). Rozchyl partnera i użyj języka prosto w środek przez pełne, mokre 2 minuty. Żadnych wymówek.",
    "Partner zatyka Ci usta swoimi dłońmi (knebel). Pieprzy Cię lub zaspokaja palcami z taką siłą, by Twoje jęki były całkowicie stłumione.",
    "Kładziesz się. Partner wylewa rozgrzany płyn/wosk prosto na Twoje krocze, a następnie agresywnie wchodzi w Ciebie/robi palcówkę z tym poślizgiem.",
    "Połykasz nasienie/soki partnera po pełnym orgazmie, po czym całujesz go głęboko z językiem, by poczuł własny smak.",
    "SYSTEM OVERLOAD. Rozwalcie ten ekran. Zabierz partnera na podłogę/blat/łóżko. Gra kończy się teraz brutalnym, głośnym seksem. 😈🔥"
]

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
                <div class='rules-item'><strong>1. SĘDZIA CZYTA:</strong> Na ekranie pojawia się pytanie. Osoba wywołana do tablicy (Sędzia) czyta je na głos.</div>
                <div class='rules-item'><strong>2. TEST WIEDZY:</strong> Druga osoba musi odgadnąć myśli, preferencje i fantazje Sędziego.</div>
                <div class='rules-item'><strong>3. PILOT PRAWDY:</strong> Sędzia trzyma pilota i decyduje, czy odpowiedź jest w 100% trafna.</div>
                <div class='rules-item'><strong>4. KARY I WYKUPNE:</strong> Jeśli oblejesz test, musisz wykonać pikantną karę... lub skorzystać z Wykupnego (które staje się z czasem coraz droższe).</div>
                <div class='rules-item'><strong>5. BEZ HAMULCÓW:</strong> Poziom ostrości rośnie z każdą rundą. Bądźcie szczerzy i odważni.</div>
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
            st.markdown(f"""
            <div class='premium-box' style='border-color: #4bd67b;'>
                <div class='turn-badge turn-intro'>{imie_info}</div>
                <div class='gold-text'>{q['tekst']}</div>
                <p style='color: #8c7a96; font-size: 18px; margin-top: 20px;'>Czas na swobodną odpowiedź, bez stresu i kar. 💕</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='premium-box' style='border-color: #d4af37;'>
                <h1 class='gold-text'>ROZGRZEWKA ZAKOŃCZONA</h1>
                <p style='color: #8c7a96; font-size: 24px; margin-top: 20px;'>Pora podnieść temperaturę... Czekam na sygnał z pilota! 😈</p>
            </div>
            """, unsafe_allow_html=True)

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
    if state["phase"] == "rules":
        st.markdown("""
        <div class='pilot-box' style='border-color: #d4af37;'>
            <div class='elegant-header'>Witajcie</div>
            <h1 class='gold-text' style='font-size: 28px; margin-top: 10px;'>PRZECZYTAJCIE ZASADY NA EKRANIE TV</h1>
        </div>
        """, unsafe_allow_html=True)
        if st.button("PRZEJDŹ DO ROZGRZEWKI 💕", use_container_width=True, type="primary"):
            state["phase"] = "intro"
            st.rerun()

    elif state["phase"] == "intro":
        q_idx = state["intro_q"]
        if q_idx < len(state["intro_gra"]):
            st.markdown("""
            <div class='pilot-box' style='border-color: #4bd67b;'>
                <div class='elegant-header'>Panel Sterowania</div>
                <h1 class='gold-text' style='font-size: 32px; color: #4bd67b; margin-top: 10px;'>ROZGRZEWKA 💕</h1>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("NASTĘPNE PYTANIE ➔", use_container_width=True, type="secondary"):
                state["intro_q"] += 1
                st.rerun()
                
            st.markdown("<hr style='border-color: #2a2035; margin: 30px 0;'>", unsafe_allow_html=True)
            if st.button("ZACZYNAMY GRĘ WŁAŚCIWĄ 😈", use_container_width=True, type="primary"):
                state["phase"] = "main"
                st.rerun()
        else:
            st.markdown("""
            <div class='pilot-box' style='border-color: #ff4b4b;'>
                <div class='elegant-header'>Rozgrzewka</div>
                <h1 class='gold-text' style='font-size: 26px; color: #ff4b4b; margin-top: 10px;'>PYTANIA WYCZERPANE</h1>
            </div>
            """, unsafe_allow_html=True)
            if st.button("ZACZYNAMY GRĘ WŁAŚCIWĄ 😈", use_container_width=True, type="primary"):
                state["phase"] = "main"
                st.rerun()

    else:
        q_idx = state["current_q"]
        if q_idx < len(state["gra"]):
            q = state["gra"][q_idx]
            who_val = str(q["kto"]).upper().strip()
            sedzia_imie = IMIE_ONA if who_val == "ONA" else IMIE_ON
            badge_class = "turn-ona" if who_val == "ONA" else "turn-on"
            
            if state["status"] == "question":
                if who_val == "TOAST":
                    st.markdown("""
                    <div class='pilot-box' style='border-color: #ff4b4b;'>
                        <div class='elegant-header'>Panel Sterowania</div>
                        <div class='turn-badge turn-toast' style='margin-bottom: 0; margin-top: 15px;'>CZAS NA TOAST! 🥂</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("WYPITE! ➔", use_container_width=True, type="primary"):
                        state["status"] = "result"; state["buyout_msg"] = "NA ZDROWIE!"; st.rerun()
                else:
                    st.markdown(f"""
                    <div class='pilot-box'>
                        <div class='elegant-header'>Runda {q_idx + 1}</div>
                        <div class='turn-badge {badge_class}' style='margin-bottom: 0; margin-top: 15px;'>SĘDZIUJE: {sedzia_imie}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("TAK (PRAWDA) ✅", use_container_width=True, type="primary"):
                        state["status"] = "result"; state["buyout_msg"] = "PRAWDA ZAAKCEPTOWANA ✅"; st.rerun()
                    
                    if st.button("NIE (KARA / WYKUPNE) ❌", use_container_width=True, type="secondary"):
                        state["status"] = "decision"; st.rerun()
            
            elif state["status"] == "decision":
                refusals = state["ona_refusals"] if who_val == "ONA" else state["on_refusals"]
                b_type, b_label = get_buyout_info(refusals)
                
                st.markdown(f"""
                <div class='pilot-box' style='border-color: #ff4b4b;'>
                    <div class='elegant-header'>Panel Sterowania</div>
                    <div class='turn-badge turn-toast' style='margin-bottom: 0; margin-top: 15px;'>DECYDUJE: {sedzia_imie}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if b_type != "MANDATORY":
                    if st.button(f"UŻYJ: {b_label} 🛡️", use_container_width=True, type="primary"):
                        if who_val == "ONA": state["ona_refusals"] += 1
                        else: state["on_refusals"] += 1
                        state["status"] = "result"; state["buyout_msg"] = f"WYKUPIONE: {b_label}"; st.rerun()
                
                if st.button("WYKONUJĘ KARĘ 😈", use_container_width=True, type="secondary"):
                    state["status"] = "result"; state["penalty"] = wylosuj_kare(q_idx, len(state["gra"])); state["buyout_msg"] = ""; st.rerun()

            else:
                st.markdown(f"""
                <div class='pilot-box' style='border-color: #4bd67b;'>
                    <div class='elegant-header'>Panel Sterowania</div>
                    <h1 class='gold-text' style='font-size: 24px; color: #4bd67b; margin-top: 15px;'>WYNIK NA EKRANIE TV</h1>
                </div>
                """, unsafe_allow_html=True)
                if st.button("NASTĘPNE PYTANIE ➔", use_container_width=True, type="primary"):
                    state["current_q"] += 1
                    state["status"] = "question"
                    state["buyout_msg"] = ""
                    state["penalty"] = ""
                    st.rerun()
        
        if st.button("RESETUJ GRĘ"):
            state["phase"] = "rules"
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
