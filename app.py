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
    {"kto": "ONA", "tekst": "Zgadnij, w jakiej jednej rzeczy uważam, że mam nad Tobą absolutną przewagę?"},
    {"kto": "ON", "tekst": "Jak myślisz, którą Twoją cechę próbowałem kiedyś po cichu 'naprawić', ale w końcu odpuściłem?"},
    {"kto": "ONA", "tekst": "Zgadnij, co jest najbardziej irytującą rzeczą, którą robisz, a o której Ci nie mówię, żeby Cię nie zranić?"},
    {"kto": "ON", "tekst": "Gdybyśmy byli parą w filmie akcji, zgadnij, które z nas pierwsze by nas niechcący zdradziło?"},
    {"kto": "ONA", "tekst": "Jak myślisz, za co Twoi rodzice lub znajomi powinni mi postawić pomnik w kontekście życia z Tobą?"},
    {"kto": "ON", "tekst": "Zgadnij, jaka Twoja opinia na mój temat na początku znajomości okazała się kompletnie błędna?"},
    {"kto": "ONA", "tekst": "Jak myślisz, w jakiej dziedzinie życia najbardziej potrzebujesz mojego 'prowadzenia za rękę'?"},
    {"kto": "ON", "tekst": "Zgadnij, kiedy ostatnio udawałem, że Cię słucham, a tak naprawdę myślałem o czymś zupełnie innym?"},
    {"kto": "ONA", "tekst": "Czy według mnie nasz związek przetrwałby na bezludnej wyspie dłużej niż tydzień?"},
    {"kto": "ON", "tekst": "Jak myślisz, która z Twoich koleżanek/kolegów jest według mnie najbardziej irytująca, choć udaję, że jest okej?"},
    {"kto": "ONA", "tekst": "Zgadnij, co uważam za naszą największą wspólną 'porażkę', z której dziś się śmiejemy?"},
    {"kto": "ON", "tekst": "Gdybyś mogła zmienić we mnie jedną fizyczną cechę za dotknięciem różdżki, zgadnij, co by to było?"},
    {"kto": "ONA", "tekst": "Jak myślisz, kto w naszym związku częściej 'pociąga za sznurki' w kluczowych decyzjach?"},
    {"kto": "ON", "tekst": "Zgadnij, o co byłbym najbardziej zazdrosny, gdybyśmy nie byli tak pewni siebie, jak jesteśmy?"},
    {"kto": "ONA", "tekst": "Gdybyśmy mieli wziąć udział w reality show, zgadnij, o co pokłócilibyśmy się w pierwszym odcinku?"},
    {"kto": "ON", "tekst": "Zgadnij, czy wolę, gdy prosisz mnie o pomoc, czy gdy udowadniasz mi, że poradzisz sobie sama?"},
    {"kto": "ONA", "tekst": "Jak myślisz, jaką moją tajemnicę (niegroźną!) uważam za najbardziej absurdalną?"},
    {"kto": "ON", "tekst": "Zgadnij, co w naszym mieszkaniu/domu wyrzuciłbym przez okno, gdybym wiedział, że się nie pogniewasz?"},
    {"kto": "ONA", "tekst": "Gdybyś miał mnie opisać jako postać historyczną, zgadnij, czy byłabym tyranem, czy dyplomatką?"},
    {"kto": "ON", "tekst": "Jak myślisz, czy według mnie częściej Ty masz rację, czy to ja po prostu szybciej odpuszczam?"},
    {"kto": "ONA", "tekst": "Zgadnij, jaka Twoja umiejętność sprawia, że czuję się przy Tobie najbardziej bezradna?"},
    {"kto": "ON", "tekst": "Czy według mnie jesteśmy dla siebie wyzwaniem, czy raczej bezpieczną przystanią, w której można się rozleniwić?"},
    {"kto": "ONA", "tekst": "Zgadnij, jakiego pytania najbardziej boisz się ode mnie usłyszeć w przyszłości?"},
    {"kto": "ON", "tekst": "Jak myślisz, z czego najtrudniej byłoby mi zrezygnować, gdybyś postawiła mi ultimatum?"},
    {"kto": "ONA", "tekst": "Zgadnij, jaka jest najbardziej 'obciachowa' rzecz, którą robimy razem, gdy nikt nie patrzy?"},
    {"kto": "ON", "tekst": "Czy według mnie Twoja intuicja częściej ratuje nam skórę, czy pakuje nas w kłopoty?"},
    {"kto": "ONA", "tekst": "Zgadnij, w jakiej sytuacji najbardziej czuję, że tracę nad Tobą kontrolę?"},
    {"kto": "ON", "tekst": "Jak myślisz, który z Twoich nawyków najczęściej staje się tematem moich żartów w pracy?"},
    {"kto": "ONA", "tekst": "Gdybyśmy mieli zostać 'Power Couple' (np. w polityce), kto według mnie byłby liderem, a kto strategiem?"},
    {"kto": "ON", "tekst": "Zgadnij, czy według mnie częściej wybaczam Ci błędy, bo Cię kocham, czy dlatego, że jestem do nich przyzwyczajony?"}
]

toasty = [
    "WYZWANIE: Kto ma na sobie więcej warstw ubrań (lub biżuterii), pije shota – w tej grze im mniej, tym lepiej! 🥃",
    "POJEDYNEK: Powiedzcie jednocześnie miejsce, w którym najchętniej zrobilibyście 'to' publicznie. Różne odpowiedzi? Pijecie oboje! 👀",
    "MECHANIKA: Pijecie razem. Osoba, która czuje się dziś bardziej 'grzeszna', narzuca tempo. Druga musi skończyć dokładnie w tym samym momencie! 💦",
    "WYZWANIE: Wypijcie shota, ale kieliszek partnera trzymasz Ty, a on Twój. Nie wolno uronić ani kropli! 🍷",
    "ZADANIE: Sędzia robi partnerowi 'body shota' z obojczyka lub wgłębienia przy szyi. 💋",
    "POJEDYNEK: Bitwa na spojrzenia podczas picia. Kto pierwszy mrugnie lub się zaśmieje, musi zdjąć jeden element garderoby! ⚡",
    "WYZWANIE: Kto w tym związku częściej przejmuje inicjatywę w sypialni? Ta osoba pije teraz podwójnie za swoją odwagę! 🥂",
    "ZADANIE: Jedno z Was pije shota, a drugie w tym czasie musi czule (lub drapieżnie) całować je po szyi. Nie wolno przestać pić! 🍾",
    "ZADANIE: Przesuń zimnym kieliszkiem po brzuchu partnera pod ubraniem. Jeśli partner drgnie, pije shota! 😈",
    "WYZWANIE: Powiedz partnerowi najbardziej sprośny komplement, jaki przychodzi Ci do głowy. Jeśli się zarumieni – pije! 🔥",
    "POJEDYNEK: Kto szybciej odepnie/zdejmie jeden element ubrania partnera, używając tylko jednej ręki? Przegrany pije! ✂️",
    "ZADANIE: Pijecie shota, podczas gdy jedno z Was siedzi drugiemu na kolanach (przodem do siebie). 🤫",
    "WYZWANIE: Toast za najbardziej szaloną rzecz, którą zamierzacie zrobić dzisiejszej nocy, gdy ta gra się skończy! 🥂"
]

p1 = [
    {"kto": "ONA", "tekst": "Zgadnij, jaki Twój gest w miejscu publicznym sprawia, że mam ochotę natychmiast zabrać Cię do domu?"},
    {"kto": "ON", "tekst": "Jak myślisz, który element Twojego ubioru uważam za największą 'przeszkodę', którą najchętniej bym z Ciebie zdjął?"},
    {"kto": "ONA", "tekst": "Wybierz: czy JA wolę, gdy dominujesz nade mną siłą, czy gdy kusisz mnie powolnym, delikatnym dotykiem?"},
    {"kto": "ON", "tekst": "Czy według MNIE kręci Cię bardziej moja pewność siebie, czy momenty, w których pokazuję przed Tobą słabość?"},
    {"kto": "ONA", "tekst": "Jak myślisz, co pomyślałam o Twoich umiejętnościach w łóżku, zanim jeszcze pierwszy raz się tam znaleźliśmy?"},
    {"kto": "ON", "tekst": "Gdybym miał opisać zapach Twojej skóry po upojnej nocy, jakich trzech przymiotników bym użył?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy kręci mnie, gdy patrzysz na mnie z zaborczą zazdrością, gdy ktoś inny zawiesi na mnie wzrok?"},
    {"kto": "ON", "tekst": "Gdybym miał wskazać jeden dźwięk, który wydajesz, a który działa na mnie najbardziej – zgadnij, co by to było?"},
    {"kto": "ONA", "tekst": "Jak myślisz, co najbardziej podnieca mnie w Twoim spojrzeniu, gdy wiemy oboje, że zaraz będziemy sami?"},
    {"kto": "ON", "tekst": "Zgadnij, czy wolałbym, żebyś obudziła mnie w nocy namiętnym szeptem, czy po prostu zaczęła mnie dotykać?"},
    {"kto": "ONA", "tekst": "Jak myślisz, w którym momencie czuję się przy Tobie najbardziej bezbronna, a jednocześnie najbardziej pożądana?"},
    {"kto": "ON", "tekst": "Zgadnij, jaka Twoja niedoskonałość fizyczna jest dla mnie najbardziej seksowna, mimo że Ty jej nie lubisz?"},
    {"kto": "ONA", "tekst": "Wybierz: czy JA wolę, gdy mnie niespodziewanie przyszpilisz do ściany, czy gdy powoli przejmujesz nade mną kontrolę?"},
    {"kto": "ON", "tekst": "Jak myślisz, o czym marzę, gdy w towarzystwie kładę rękę na Twoim kolanie i powoli przesuwam ją wyżej?"},
    {"kto": "ONA", "tekst": "Zgadnij, jak bardzo muszę się hamować, żeby nie zacząć Cię całować, gdy widzę Cię skupionego na pracy?"},
    {"kto": "ON", "tekst": "Czy według MNIE nasz najbardziej szalony raz był zaplanowany w Twojej głowie, czy po prostu straciliśmy nad sobą panowanie?"},
    {"kto": "ONA", "tekst": "Zgadnij, która część Twoich dłoni – palce, wnętrze dłoni czy uścisk – najbardziej pobudza moją wyobraźnię?"},
    {"kto": "ON", "tekst": "Jak myślisz, z jakiej 'niegrzecznej' rzeczy, którą robimy, jestem najbardziej dumny, że odważyliśmy się na nią razem?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy podnieca MNIE bardziej myśl o tym, co Ty chcesz mi zrobić, czy o tym, co ja chcę zrobić Tobie?"},
    {"kto": "ON", "tekst": "Co sprawia, że JA czuję się najbardziej męsko w Twoich oczach – moja siła, opiekuńczość czy determinacja?"},
    {"kto": "ONA", "tekst": "Jak myślisz, czy kręci mnie, gdy nosisz ubrania, które podkreślają Twoje mięśnie, czy wolisz mnie kusić tym, co pod nimi?"},
    {"kto": "ON", "tekst": "Zgadnij, czy wolę, gdy podczas seksu przejmujesz stery i mówisz mi dokładnie, co mam robić?"},
    {"kto": "ONA", "tekst": "Co we mnie wibruje, gdy widzę, jak patrzysz na mnie z absolutnym głodem w oczach?"},
    {"kto": "ON", "tekst": "Zgadnij, jaka Twoja mina lub wyraz twarzy sprawia, że od razu wiem, że masz ochotę na coś więcej?"},
    {"kto": "ONA", "tekst": "Jak myślisz, czy wolałabym, żebyś zerwał ze mnie ubranie w pośpiechu, czy powoli celebrował każdy centymetr mojego ciała?"},
    {"kto": "ON", "tekst": "Co JA czuję, gdy widzę, że specjalnie założyłaś coś, co wiem, że uwielbiam, mimo że 'oficjalnie' tego nie ustalaliśmy?"},
    {"kto": "ONA", "tekst": "Zgadnij, o czym myślę, gdy widzę Cię rano, zupełnie nagiego i jeszcze zaspany?"},
    {"kto": "ON", "tekst": "Jak myślisz, czy kręci MNIE, gdy w miejscu publicznym szepczesz mi do ucha coś, czego nie powinien usłyszeć nikt inny?"},
    {"kto": "ONA", "tekst": "Zgadnij, która część Twojego ciała jest dla mnie najbardziej 'zakazanym owocem', gdy jesteśmy wśród ludzi?"},
    {"kto": "ON", "tekst": "Co w Twoim głosie zmienia się, gdy zaczynasz mnie kusić, i jak myślisz, jak to na mnie działa?"}
]

p2 = [
    {"kto": "ONA", "tekst": "Zgadnij, co w Twoim zachowaniu sprawia, że przestaję myśleć o czymkolwiek innym niż Ty i łóżko?"},
    {"kto": "ON", "tekst": "Jak myślisz, które moje słowo szepnięte Ci do ucha wywołuje u Ciebie największy dreszcz?"},
    {"kto": "ONA", "tekst": "Zgadnij, co JA wolę: kiedy Ty masz pełną kontrolę nade mną, czy kiedy to ja decyduję o każdym Twoim ruchu?"},
    {"kto": "ON", "tekst": "Jak myślisz, czy bardziej kręci mnie Twoja pewność siebie w sypialni, czy Twoje rzadkie chwile nieśmiałości?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy wolę, gdy Twoje dłonie są silne i zaborcze, czy gdy ledwie muskasz moją skórę opuszkami palców?"},
    {"kto": "ON", "tekst": "Co JA czuję, gdy podczas namiętnego momentu patrzysz mi głęboko w oczy i nie pozwalasz mi mrugnąć?"},
    {"kto": "ONA", "tekst": "Jak myślisz, jaka sytuacja 'nie do końca na miejscu' najbardziej pobudza moją wyobraźnię?"},
    {"kto": "ON", "tekst": "Zgadnij, w jakim wydaniu – naturalnym (rano) czy 'odstawionym' (wieczorem) – działasz na mnie mocniej?"},
    {"kto": "ONA", "tekst": "Wybierz: czy JA wolę, gdy stopniowo budujesz napięcie godzinami, czy gdy bierzesz mnie tu i teraz bez ostrzeżenia?"},
    {"kto": "ON", "tekst": "Jak myślisz, co mnie bardziej nakręca: świadomość, że inni Cię podziwiają, czy świadomość, że tylko ja Cię mam?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy podnieca mnie wizja zrobienia czegoś 'zakazanego', o czym nigdy wcześniej nie rozmawialiśmy?"},
    {"kto": "ON", "tekst": "Co JA wolę: kiedy jesteś kompletnie cicha i skupiona na doznaniach, czy gdy wydajesz z siebie dźwięki, których nie kontrolujesz?"},
    {"kto": "ONA", "tekst": "Jak myślisz, co czuję, gdy czuję Twój wzrok na moich plecach, wiedząc, że analizujesz każdy mój ruch?"},
    {"kto": "ON", "tekst": "Zgadnij, czy wolałbym, żebyś przejęła inicjatywę w miejscu, gdzie ktoś mógłby nas teoretycznie usłyszeć?"},
    {"kto": "ONA", "tekst": "Czy według mnie Twoje usta są bardziej niebezpieczne, gdy całują moją szyję, czy gdy szepczą sprośne obietnice?"},
    {"kto": "ON", "tekst": "Zgadnij, czy pociąga mnie myśl o Tobie w roli 'szefowej', która wydaje mi polecenia przez cały wieczór?"},
    {"kto": "ONA", "tekst": "Jak myślisz, czy rajcuje mnie wizja wspólnego prysznica, podczas którego zabraniasz mi Cię dotykać przez pierwsze 5 minut?"},
    {"kto": "ON", "tekst": "Co nakręca MNIE bardziej: Twój zapach tuż po treningu, czy zapach Twoich ulubionych perfum na randce?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy lubię, gdy w trakcie bliskości używasz lekkiej siły, by pokazać mi swoją dominację?"},
    {"kto": "ON", "tekst": "Jak myślisz, który moment naszej nocy uważam za swój osobisty 'podpis', który zawsze na Ciebie działa?"},
    {"kto": "ONA", "tekst": "Zgadnij, jak reaguję w środku, gdy podczas nudnego spotkania przesyłasz mi wiadomość o tym, co mi zrobisz w domu?"},
    {"kto": "ON", "tekst": "Jak myślisz, czy kręci MNIE wizja, w której to ja jestem Twoją 'nagrodą' za ciężki dzień?"},
    {"kto": "ONA", "tekst": "Zgadnij, co podnieca MNIE bardziej: Twoja klatka piersiowa przyciśnięta do moich pleców, czy Twoje nogi splecione z moimi?"},
    {"kto": "ON", "tekst": "Jak myślisz, czy kręci MNIE myśl o byciu Twoim jedynym widzem, gdy tańczysz lub przebierasz się tylko dla mnie?"},
    {"kto": "ONA", "tekst": "Zgadnij, z czego najszybciej tracę zmysły: z Twojego oddechu na moim karku, czy z Twoich dłoni zaciskających się na moich biodrach?"},
    {"kto": "ON", "tekst": "Czy według MNIE jesteś w łóżku bardziej tą, która bierze co chce, czy tą, która uwielbia być brana?"},
    {"kto": "ONA", "tekst": "Zgadnij, jak reaguję na myśl, że mógłbyś zdjąć ze mnie ubranie... zębami?"},
    {"kto": "ON", "tekst": "Jak myślisz, czy rajcuje MNIE bycie 'niegrzecznym' w miejscach, które kojarzą się z codziennością (np. kuchnia, biurko)?"},
    {"kto": "ONA", "tekst": "Zgadnij, w jakim stanie emocjonalnym (radość, złość, zmęczenie) mam największą ochotę na ekstremalną bliskość?"},
    {"kto": "ON", "tekst": "Co według MNIE jest najbardziej erotyczną rzeczą, jaką kiedykolwiek zrobiłaś całkowicie nieświadomie?"}
]

p3 = [
    {"kto": "ONA", "tekst": "Zgadnij, czy podnieca MNIE bardziej bycie obserwowaną przez Ciebie w lustrze, czy świadomość, że masz zamknięte oczy i tylko mnie czujesz?"},
    {"kto": "ON", "tekst": "Jak myślisz, w którym momencie stosunku czuję, że tracę nad sobą ludzką kontrolę i staję się czystym instynktem?"},
    {"kto": "ONA", "tekst": "Zgadnij, która z moich 'brudnych' fantazji najbardziej mnie przeraża, a jednocześnie sprawia, że robi mi się mokro na samą myśl?"},
    {"kto": "ON", "tekst": "Co JA czuję, gdy widzę na Twoim ciele ślady (zadrapania, ugryzienia), które zostawiłem po naszej ostatniej nocy?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy wolałabym, żebyś traktował mnie jak kruchą porcelanę, czy jak swoją własność, z którą możesz zrobić wszystko?"},
    {"kto": "ON", "tekst": "Jak myślisz, czy kręci MNIE wizja użycia kajdanek lub krępowania Cię, byś była całkowicie zdana na moją łaskę?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy bardziej rajcuje mnie seks w miejscu, gdzie ktoś może nas usłyszeć, czy tam, gdzie ktoś mógłby nas przypadkiem zobaczyć?"},
    {"kto": "ON", "tekst": "Czy według MNIE lepszy jest seks, który kończy się Twoim całkowitym wycieńczeniem, czy taki, który zostawia Cię nienasyconą?"},
    {"kto": "ONA", "tekst": "Jak myślisz, co czuję, gdy podczas szczytowania zakrywasz mi usta dłonią, bym nie mogła krzyczeć?"},
    {"kto": "ON", "tekst": "Zgadnij, czy pociąga mnie myśl o zaspokajaniu Cię oralnie, gdy Ty w tym czasie rozmawiasz z kimś przez telefon?"},
    {"kto": "ONA", "tekst": "Czy według MNIE to Ty powinieneś decydować, kiedy wolno mi osiągnąć orgazm, czy wolisz, bym to ja Cię o niego błagała?"},
    {"kto": "ON", "tekst": "Jak myślisz, co we mnie wstępuje, gdy widzę Cię w roli absolutnej dominy, która nie znosi sprzeciwu?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy fantazjowałam o tym, byś 'wziął mnie' siłą po naszej bardzo ostrej kłótni, żeby rozładować napięcie?"},
    {"kto": "ON", "tekst": "Czy kręci mnie myśl, że mogłabyś zaprosić do naszej sypialni 'trzeci element' (zabawkę lub osobę), bym mógł tylko patrzeć?"},
    {"kto": "ONA", "tekst": "Jak myślisz, czy pociąga MNIE ból wymieszany z rozkoszą, gdy podczas seksu ciągniesz mnie mocno za włosy?"},
    {"kto": "ON", "tekst": "Zgadnij, w którym momencie seksu od tyłu czuję największą więź z Twoją pierwotną, dziką naturą?"},
    {"kto": "ONA", "tekst": "Czy pociąga MNIE myśl o byciu Twoją 'niegrzeczną zabawką' przez cały wyjazd, wykonującą każde Twoje polecenie bez pytania?"},
    {"kto": "ON", "tekst": "Jak myślisz, czy wolałbym zobaczyć Cię ubraną w coś, co kompletnie nie pasuje do Twojej grzecznej codzienności (np. skóra, obroża)?"},
    {"kto": "ONA", "tekst": "Zgadnij, jak reaguje MOJE ciało na wizję długiego, męczącego seksu, po którym nie mamy siły nawet na słowo?"},
    {"kto": "ON", "tekst": "Co według MNIE jest bardziej erotyczne: Twój widok, gdy walczysz z orgazmem, czy moment, w którym całkowicie mu się poddajesz?"},
    {"kto": "ONA", "tekst": "Jak myślisz, czy pociąga MNIE wizja, w której zakradasz się do mojego łóżka w nocy i bierzesz mnie, gdy jeszcze śpię?"},
    {"kto": "ON", "tekst": "Zgadnij, czy według MNIE seks powinien być zawsze wyrazem miłości, czy czasem może być po prostu brudnym, czystym pożądaniem?"},
    {"kto": "ONA", "tekst": "Co we MNIE pęka, gdy podczas seksu nazywasz mnie słowami, których nigdy nie użyłbyś przy obiedzie?"},
    {"kto": "ON", "tekst": "Jak myślisz, w którym momencie czuję, że masz nade mną absolutną władzę, mimo że to ja fizycznie dominuję?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy bardziej rajcuje mnie ryzyko bycia przyłapaną przez kogoś bliskiego, czy przez kogoś zupełnie obcego?"},
    {"kto": "ON", "tekst": "Co według MNIE sprawia, że nasz seks jest 'niebezpieczny' i przez to tak bardzo uzależniający?"},
    {"kto": "ONA", "tekst": "Jak myślisz, czy pozycje wymagające ode mnie dużego wysiłku podniecają mnie, bo pokazują moją sprawność, czy bo pokazują moje oddanie?"},
    {"kto": "ON", "tekst": "Zgadnij, czy wyobrażałem sobie kiedyś, że uprawiamy seks, a Ty musisz udawać przed kimś innym, że nic się nie dzieje?"},
    {"kto": "ONA", "tekst": "Czy podnieca MNIE myśl o seksie w miejscu publicznym, gdzie musielibyśmy zachować absolutną ciszę, by nie zostać wykrytym?"},
    {"kto": "ON", "tekst": "Jak myślisz, co dokładnie czuję, gdy widzę Cię uległą, czekającą na mój następny ruch z niepokojem i ekscytacją?"}
]

p4 = [
    {"kto": "ONA", "tekst": "Zgadnij, czy podnieca MNIE bardziej fakt, że odbierasz mi głos (knebel), czy to, że odbierasz mi możliwość ruchu (więzy)?"},
    {"kto": "ON", "tekst": "Jak myślisz, czy kręci mnie rola 'reżysera', który dokumentuje Twoje najbardziej intymne momenty, by mieć nad nimi wieczystą kontrolę?"},
    {"kto": "ONA", "tekst": "Zgadnij, jak bardzo mokra bym się stała, gdybyś bez słowa wymusił moją uległość w momencie, w którym najmniej się tego spodziewam?"},
    {"kto": "ON", "tekst": "Czy według MNIE kręci Cię moment, w którym tracisz panowanie nad odruchem wymiotnym, a ja nie pozwalam Ci przestać?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy pociąga mnie myśl o szoku termicznym w sypialni – od parzącego wosku po lodowaty dotyk w samym centrum rozkoszy?"},
    {"kto": "ON", "tekst": "Jak myślisz, czy rajcuje mnie wizja wymierzania Ci 'lekcji dyscypliny' za każdym razem, gdy Twoje zachowanie odbiega od moich oczekiwań?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy w głębi duszy marzę o tym, byś potraktował mnie brutalnie, ignorując moje prośby o litość, dopóki sama nie pęknę?"},
    {"kto": "ON", "tekst": "Czy według MNIE seks analny jest dla nas najwyższą formą Twojego oddania mi się, czy tylko kolejnym sposobem na rozrywkę?"},
    {"kto": "ONA", "tekst": "Jak myślisz, czy czuję dumę i podniecenie, wiedząc, że przyjmuję Cię do końca i nie marnuję ani kropli Twojego nasycenia?"},
    {"kto": "ON", "tekst": "Zgadnij, czy kręci mnie Twój naturalny, zwierzęcy zapach po wysiłku tak bardzo, że chciałbym Cię posiąść zanim pójdziesz pod prysznic?"},
    {"kto": "ONA", "tekst": "Czy podnieca MNIE myśl, że w trakcie seksu sprowadzasz moją wartość tylko do Twojej zabawki, używając najgorszych słów, jakie znasz?"},
    {"kto": "ON", "tekst": "Jak myślisz, czy bardziej kręci mnie ryzyko, że ktoś nas nakryje w lesie, czy to, że Ty będziesz się tego panicznie bała?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy kręci mnie rola 'nieznajomej', którą uwodzisz w hotelu, zapominając o wszystkim, co nas łączy na co dzień?"},
    {"kto": "ON", "tekst": "Zgadnij, czy czuję satysfakcję, gdy widzę Twoją twarz naznaczoną moją obecnością, niszcząc Twój staranny wizerunek?"},
    {"kto": "ONA", "tekst": "Jak myślisz, czy rajcuje mnie bycie Twoją 'uwięzioną' w publicznym miejscu, gdzie pilot w Twojej kieszeni decyduje o moim orgazmie?"},
    {"kto": "ON", "tekst": "Zgadnij, czy podnieca mnie doprowadzanie Cię na skraj szaleństwa tylko po to, by w ostatniej sekundzie odebrać Ci nagrodę i patrzeć na Twoją frustrację?"},
    {"kto": "ONA", "tekst": "Co byś poczuł, gdybym zaproponowała, byś dzielił się mną z kimś innym, tylko po to, byś mógł czerpać satysfakcję z obserwacji?"},
    {"kto": "ON", "tekst": "Czy podnieca MNIE fakt, że doprowadzasz się do szczytu na moich oczach, wiedząc, że nie masz prawa mnie dotknąć bez pozwolenia?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy marzy mi się chwila, w której nie mogę zrobić nic, by sobie ulżyć, a cały mój los zależy od sprawności Twoich dłoni?"},
    {"kto": "ON", "tekst": "Jak myślisz, czy wolałbym być przez Ciebie brutalnie wybudzony ze snu i zmuszony do zaspokojenia Twoich najbardziej dzikich potrzeb?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy podnieca mnie wizja bycia wystawioną na widok obcych ludzi, wiedząc, że tylko Ty masz do mnie pełny dostęp?"},
    {"kto": "ON", "tekst": "W skali od 1 do 10 – jak bardzo podnieca mnie myśl, że Twoje ciało należy do mnie w tak absolutny sposób, że mogę Cię związać i zostawić?"},
    {"kto": "ONA", "tekst": "Czy wyobrażałam sobie, że nasza namiętność jest tak niszczycielska, że demolujemy wszystko wokół nas, nie zważając na straty?"},
    {"kto": "ON", "tekst": "Zgadnij, czy pociąga mnie myśl o przełamaniu Twojego ostatniego bastionu wstydu poprzez eksplorację miejsc, które dotąd były tabu?"},
    {"kto": "ONA", "tekst": "Jak myślisz, czy rajcuje mnie smak własnego pożądania na moich ustach, gdy zmuszasz mnie do skosztowania tego, co we mnie wywołałeś?"},
    {"kto": "ON", "tekst": "Czy według mnie Twoje soki to esencja Twojej uległości, którą chcę pić prosto z Twojego ciała bez żadnych zahamowań?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy kiedykolwiek fantazjowałam o byciu 'przyłapaną' na czymś sprośnym przez kogoś, kto nigdy nie powinien nas tak widzieć?"},
    {"kto": "ON", "tekst": "Jak myślisz, czy moja najmroczniejsza fantazja dotyczy Twojego bólu, Twojego całkowitego upokorzenia czy Twojej nieskończonej rozkoszy?"},
    {"kto": "ONA", "tekst": "Czy podnieca MNIE bycie traktowaną jak przedmiot, który nie ma uczuć, a jedynie funkcję zaspokojenia Twojego głodu?"},
    {"kto": "ON", "tekst": "Zgadnij, czy według mnie seks po nienawiści jest jedynym momentem, w którym nasze maski opadają i zostaje sama, brudna prawda?"}
]

kary_l1 = [
    "Przyprzyj partnera do ściany, unieruchom jego biodra swoimi i przez 60 sekund oddychaj mu prosto w usta, nie pozwalając na pocałunek.",
    "Usiądź na partnerze odwrócona tyłem (plecami do jego twarzy) i poruszaj się rytmicznie przez pełną minutę, nie pozwalając mu na żaden ruch rękami.",
    "Zassij skórę na szyi partnera dokładnie w jego ulubionym miejscu i przytrzymaj tak długo, aż poczujesz pod językiem puls.",
    "Wsuń dłonie pod ubranie partnera, znajdź jego łopatki i przejedź po nich paznokciami z taką siłą, by przeszył go dreszcz, jednocześnie gryząc go w ramię.",
    "Złap partnera za ręce, spleć swoje palce z jego i dociśnij je do łóżka/kanapy, szepcząc mu prosto w usta najbardziej sprośne życzenie.",
    "Zębami powoli rozepnij jeden guzik lub odchyl materiał przy dekolcie partnera i zostaw tam gorący ślad po ssaniu skóry.",
    "Wydaj partnerowi bezwzględne polecenie dotyczące tego, co ma Ci zrobić dzisiaj w sypialni, trzymając go w tym czasie mocno za pasek od spodni.",
    "Uciśnij mocno uda partnera swoimi kolanami (pomiędzy nimi) i trzymaj tak przez minutę, patrząc mu wyzywająco prosto w oczy.",
    "Złap partnera za podbródek, wymuś kontakt wzrokowy i poliż jego dolną wargę tak powoli, jak to tylko możliwe, nie zamykając oczu.",
    "Zwiąż ręce partnera jego własnym paskiem lub krawatem. Przez minutę rób z nim co chcesz, pod warunkiem, że nie użyjesz do tego dłoni.",
    "Chwyć wargami płatek ucha partnera i pociągnij go mocno, jednocześnie wsuwając dłoń głęboko pod jego ubranie na brzuchu.",
    "Każ partnerowi zamknąć oczy. Przesuwaj po jego ciele (od szyi w dół) zimnym przedmiotem lub kostką lodu, dopóki nie zacznie drżeć.",
    "Nagryź lekko linię szczęki partnera, a potem zliż to miejsce, zostawiając po sobie zapach swojej skóry.",
    "Stań za partnerem, obejmij go mocno w pasie i przyciśnij swoje ciało do jego pleców tak ciasno, by poczuł każdy Twój oddech przez 60 sekund.",
    "Zrób partnerowi 'body shot' – wylej kroplę alkoholu lub napoju w dołek między obojczykami i spij go powoli, używając tylko języka.",
    "Włóż dłoń między uda partnera i trzymaj ją tam nieruchomo (bardzo blisko celu) podczas czytania 3 kolejnych pytań.",
    "Przejedź językiem po wnętrzu dłoni partnera, a potem mocno zaciśnij na niej swoje zęby, nie spuszczając wzroku z jego twarzy.",
    "Zafunduj partnerowi agresywny pocałunek, w trakcie którego siłą wepchniesz swój język do jego ust, dominując go całkowicie.",
    "Złap zębami koszulkę partnera na wysokości klatki piersiowej i szarpnij nią tak, by poczuł Twoją niecierpliwość.",
    "Złóż serię krótkich, bolesnych ugryzień wzdłuż mięśnia kapturowego (między szyją a ramieniem) partnera.",
    "Usiądźcie naprzeciwko siebie. Przez minutę musicie ocierać się o siebie tylko kolanami i udami, zachowując absolutną ciszę i powagę.",
    "Oprzyj stopę o krocze partnera (pod stołem lub na kanapie) i wywieraj miarowy nacisk przez 3 kolejne pytania.",
    "Wbij paznokcie w przedramiona partnera i przyciągnij go do siebie tak blisko, by poczuł żar bijący z Twojej twarzy.",
    "Podejdź do partnera od tyłu, odchyl mu głowę i przejedź językiem po jego krtani, aż poczujesz, że przełyka ślinę.",
    "Wciągnij gwałtownie zapach partnera przy samej jego skórze (za uchem), a potem szepnij mu bardzo niskim głosem: 'Jesteś mój/moja'."
]

kary_l2 = [
    "Pozbądź się wszystkiego powyżej pasa i stań przed partnerem z rękami splecionymi za plecami. Nie wolno Ci się zakryć do następnej kary.",
    "Wsuń dłoń głęboko pod bieliznę partnera od przodu i zaciśnij ją pewnie na jego najczulszym miejscu. Trzymaj tak przez 60 s, patrząc mu wyzywająco w oczy.",
    "Wybierz jeden element swojej bielizny, zdejmij go na oczach partnera i każ mu go trzymać w dłoni przez następne dwie rundy.",
    "Każ partnerowi rozchylić nogi, uklęknij przed nim i przez minutę drażnij jego strefę V gorącym oddechem, nie dotykając jej ani razu ustami.",
    "Wykonaj agresywny lap dance, podczas którego partner ma całkowity zakaz dotykania Cię dłońmi – może tylko patrzeć, jak go prowokujesz.",
    "Zostaw ścieżkę z alkoholu od szyi aż po sam dół brzucha partnera i zliż ją, zatrzymując się na dłużej przy każdym napotkanym wgłębieniu.",
    "Wgryź się w ramię lub kark partnera tak mocno, by przez resztę wieczoru nosił na skórze Twój 'podpis' – wyraźny ślad zębów.",
    "Rozsuń zamek w spodniach partnera, pochyl się i przez 60 sekund drażnij go tam samym językiem, nie używając rąk.",
    "Połóż się na brzuchu. Partner siada na Tobie, dociska Cię do ziemi i przez 2 minuty ma pełną władzę nad Twoim ciałem.",
    "Wymierz partnerowi soczystego klapsa w udo, a gdy skóra poczerwienieje, każ mu podziękować za tę karę i dopiero wtedy go pocałuj.",
    "Używając wyłącznie zębów, zdejmij z partnera element garderoby, który najbardziej utrudnia Ci dostęp do jego nagiej skóry.",
    "Przesuń kostką lodu po ustach partnera, a potem natychmiast wymuś na nim głęboki pocałunek, by poczuł uderzenie zimna wewnątrz Twoich ust.",
    "Wsuń dłonie pod ubranie partnera i zaciśnij je na jego piersiach/klatce z taką siłą, by usłyszeć jego przyspieszony oddech. Nie puszczaj przez minutę.",
    "Przybij partnera do ściany swoim ciałem, unieś jedną jego nogę i opleć ją wokół swojego biodra, po czym całuj go, jakbyś chciał go pożreć.",
    "Rozepnij spodnie/spódnicę partnera na tyle, by zobaczyć jego bieliznę, i złóż tam długi, wilgotny pocałunek, zostawiając wyraźną plamę.",
    "Przejmij kontrolę: każ partnerowi odegrać rolę Twojej uległej własności i zabroń mu odzywać się bez Twojego wyraźnego pozwolenia.",
    "Rozsmaruj odrobinę napoju na swoich obojczykach i każ partnerowi spić go z Twojej skóry, podczas gdy Ty będziesz mocno trzymać go za włosy.",
    "Złap partnera za szyję (pewnie, ale z wyczuciem) i powiedz mu niskim głosem, co dokładnie zamierzasz z nim zrobić, gdy ta gra dobiegnie końca.",
    "Mocno poliż swój palec i przesuń nim wzdłuż linii pośladków partnera (pod ubraniem), wywołując u niego nagły dreszcz zaskoczenia.",
    "Zdejmij górę ubrania, chwyć partnera za dłonie i skrzyżuj je na swojej nagiej piersi/klatce, trzymając je tam siłą przez pełną minutę.",
    "Zmuś partnera do uklęknięcia przed Tobą. Wsuń mu palce do ust i nakłoń go do ich ssania, jednocześnie dyktując mu rytm drugą ręką na jego karku.",
    "Złap partnera za koszulę na klatce piersiowej i pociągnij go za sobą do innego pomieszczenia (lub w ciemny kąt), by tam namiętnie go 'ukarać'.",
    "Napełnij usta napojem i przelej go partnerowi, ale zrób to w taki sposób, by połowa płynu spłynęła po Waszych ciałach.",
    "Przez całą minutę trzymaj dłoń wciśniętą mocno między nogi partnera (od przodu), wymuszając na nim utrzymanie kontaktu wzrokowego.",
    "Klep partnera lekko w twarz (gest upokorzenia/dominacji) i każ mu wyznać, która z Twoich dzisiejszych kar podnieciła go najbardziej.",
]

kary_l3 = [
    "Oboje pozbywacie się dolnej części garderoby. Każ mu/jej patrzeć prosto w Twoje krocze przez 30 sekund w milczeniu, zanim wrócicie do gry.",
    "Tortura przez materiał – drażnij partnera ustami i gorącym oddechem przez bieliznę przez 2 minuty, ale za każdy jego/jej jęk dodajesz 10 sekund.",
    "Wsuń dłoń do bielizny partnera, zaciśnij ją pewnie i dyktuj rytm przez 2 minuty, zabraniając mu/jej jakiegokolwiek ruchu biodrami.",
    "Odsłoń klatkę partnera. Drażnij jego sutki zębami i językiem, dopóki nie usłyszysz, że jego oddech stał się rwanym szeptem.",
    "Uklęknij między nogami partnera. Całuj wnętrze ud, zatrzymując się milimetr przed celem – jeśli on/ona spróbuje przybliżyć biodra, kara zaczyna się od nowa.",
    "Całkowite oddanie: masz 60 sekund na to, by użyć swojego języka na partnerze tak agresywnie, by zapomniał o bożym świecie. Stoper start.",
    "Ekstremalny Edging: Doprowadź partnera na samą krawędź używając ust i dłoni, a gdy zacznie błagać o koniec – brutalnie przestań i odsuń się na metr.",
    "Lodowy szlak: Przesuń kostkę lodu od szyi aż po genitalia partnera, a potem ogrzej te miejsca swoim gorącym oddechem, nie dotykając ich wargami.",
    "Symulacja dominacji: Usiądź na partnerze w bieliźnie i ruszaj się tak, jakbyś chciał go/ją posiąść, ale trzymaj ręce zaciśnięte na jego/jej szyi (bezpiecznie).",
    "Partner na brzuchu, dół kompletnie nagi. Wykorzystaj balsam, by masować pośladki, ale używaj do tego głównie swoich piersi lub klatki piersiowej.",
    "Unieruchomienie: Zwiąż ręce partnera za plecami. Przez 3 minuty rób z jego nagim brzuchem i udami co chcesz – on/ona nie ma prawa do oporu.",
    "Połóż się na plecach. Oddajesz partnerowi pełnię władzy nad swoimi ustami na 2 minuty – on/ona decyduje, co i jak głęboko tam trafi.",
    "Pełna ekspozycja: Zdejmij całą bieliznę. Przez następne 3 pytania siedzisz nago naprzeciwko partnera z szeroko rozstawionymi nogami.",
    "Zliż kroplę alkoholu z samego środka pożądania partnera, używając do tego tylko czubka języka i patrząc mu wyzywająco w oczy.",
    "Zaborczy pocałunek: 2 minuty walki języków, podczas gdy oboje badacie swoje najczulsze miejsca pod bielizną, sprawdzając, kto pierwszy pęknie.",
    "Pozycja 69: Skupiacie się na wzajemnym doprowadzeniu się do obłędu, ale możecie używać tylko języków. Ręce muszą być splecione za Waszymi plecami.",
    "Stół jako ołtarz: Posadź partnera na blacie, wejdź między jego nogi i zdejmij mu bieliznę zębami, a potem pieść go przez 2 minuty bez użycia dłoni.",
    "Wydaj partnerowi rozkaz, który zawsze uważałaś/eś za zbyt odważny – on/ona musi go teraz wykonać na Twoich oczach przez 60 sekund.",
    "Nagie show: Rozbierz się do rosołu i odtwórz pozycję, w której najbardziej boisz się, że stracisz nad sobą kontrolę. Partner ma tylko patrzeć.",
    "Ślady własności: Zdejmij bieliznę, wypnij się w stronę partnera i przyjmij 3 mocne klapsy, które mają być słyszalne w całym domu.",
    "Bezwzględna uległość: Przez 3 minuty jesteś rzeczą. Partner może Cię przesuwać, dotykać i ustawiać tak, jak mu się podoba. Nie wolno Ci mrugnąć.",
    "Solo przed widzem: Użyj zabawki lub dłoni na sobie, patrząc partnerowi w oczy i opisując na głos, jak bardzo chcesz, żeby to on/ona Cię teraz zastąpił/a.",
    "Gorący masaż: Ściągnij partnerowi bieliznę i przez 2 minuty ugniataj jego strefy intymne, ale używaj do tego tylko kciuków, wywierając mocny nacisk.",
    "Zrzucenie skóry: Pozbądź się bielizny ocierając się o meble lub ciało partnera. Ręce muszą pozostać wysoko nad Twoją głową.",
    "Ostatni oddech: Przyciągnij partnera tak gwałtownie, by poczuł Twoje tętno na swojej skórze, i zafunduj mu pocałunek, który smakuje jak obietnica bezsennej nocy."
]

kary_l4 = [
    "NAGOŚĆ ABSOLUTNA. Palicie za sobą mosty. Ubrania lądują w drugim końcu pokoju. Do końca nocy każde z Was jest tylko ciałem do dyspozycji drugiego.",
    "WŁADZA I PENETRACJA. Bierzesz partnera tu i teraz. Masz 3 minuty na to, by swoimi ruchami pokazać mu, do kogo należy to pomieszczenie.",
    "USTA PEŁNE POSŁUSZEŃSTWA. Kładziesz się, a partner ma 3 minuty na to, by wyssać z Ciebie duszę. Jeśli nie stracisz nad sobą kontroli, kara zostaje przedłużona.",
    "PSYCHICZNE KATUSZE (Edging). Doprowadź partnera na samą krawędź obłędu dłonią lub językiem, a gdy zacznie błagać o finał – wyjdź z pokoju na 30 sekund.",
    "DOBYTEK (Piesek). Bierzesz partnera od tyłu, trzymając go za włosy lub kark. Przez 3 minuty narzucasz mu swój rytm, traktując go jak swoją własność.",
    "GŁĘBOKI GŁÓD. Masz 3 minuty na doprowadzenie partnera do szaleństwa ustami. Żądam głębokiego gardła i pełnego zaangażowania aż po sam finał.",
    "PRZYBITY DO ŚCIANY. Unosisz partnera, opierasz o ścianę i wchodzisz w niego z furią. 2 minuty seksu, w którym jedynym podparciem jest Twoja siła.",
    "DYKTATURA JEŹDŹCA. Siadasz na partnerze i z zimną krwią decydujesz o każdym centymetrze głębokości. Patrz mu w oczy, gdy odbierasz mu oddech.",
    "69 BEZ CENZURY. Oboje nago, w pełnym splocie. Walczycie o to, kto szybciej zmusi drugą stronę do wydania z siebie zwierzęcego krzyku.",
    "SENSORYCZNA PUSTKA. Opaska na oczy. Partner staje się manekinem, na którym testujesz swoje najbardziej wyuzdane techniki. On ma tylko czuć i drżeć.",
    "WIĘZI ROZKOSZY. Krępujesz dłonie partnera. Masz 3 minuty na bezkarne używanie jego ciała tak, jakbyś go właśnie kupił na aukcji.",
    "PROŚ O WIĘCEJ. Partner musi na głos wyznać, jak bardzo potrzebuje Twojego wypełnienia, zanim pozwolisz mu poczuć choćby gram ulgi.",
    "TWARDY BLAT. Rzucasz partnera na stół. Bez gry wstępnej, bez czułości – 2 minuty surowego rżnięcia, które ma trząść całym domem.",
    "MECHANICZNA PRZEWAGA. Wykręć gadżet na maksimum. Użyj go tak bezlitośnie, by partner stracił kontakt z rzeczywistością przez 3 minuty.",
    "KONTRAKT NA ORGAZM. Gra zostaje zawieszona. Żadne z Was nie wstanie, dopóki partner nie doświadczy orgazmu, który sprawi, że zemdleje z rozkoszy.",
    "WODNA ORGIA. Pod prysznicem, w oparach pary i piany, bierzesz partnera tak mocno, by kafelki dudniły od Waszych ciał przez 10 minut.",
    "BRUDNE SZEPTY (Łyżeczka). Wchodzisz powoli od tyłu, paraliżując partnera dłońmi na jego krtani i szeptem opisując, co zaraz mu zrobisz.",
    "TRON DOMINACJI. Partner klęczy u Twoich stóp, zaspokajając Cię ustami. Ty nadajesz tempo, trzymając jego głowę tak mocno, by nie mógł uciec.",
    "SLIPPERY POSSESSION. Całe ciało w olejku. Używasz swojej klatki/piersi jako smaru, ślizgając się po partnerze aż po samą penetrację.",
    "EKSHIBICJONIZM SOLO. Partner ma patrzeć, jak doprowadzasz się do szczytu, opisując dokładnie każdy brudny detal tego, co sobie wyobrażasz.",
    "PODSTOŁOWY SERWIS. Podczas gdy partner próbuje udawać, że nic się nie dzieje, Ty pod stołem robisz mu najbardziej zachłanny oral w jego życiu.",
    "DUSZA W OCZACH. Misjonarz. Najgłębsza możliwa penetracja z zakazem mrugania. Patrzcie w swoje mroczne wnętrza, gdy Wasze ciała się stapiają.",
    "FACE-SITTING / DOMINACJA. Siadasz partnerowi na twarzy, odbierając mu tlen i dyktując ustami rytm swojej własnej ekstazy. Jesteś bogiem.",
    "PRYMALNY CHWYT. Zaciśnij dłoń na włosach partnera, wymuś brutalny pocałunek i wbij palce w jego krocze, sprawdzając jak bardzo jest spragniony.",
    "DESTRUKCJA SYSTEMU. Zapomnij o zasadach. Bierzesz partnera tam, gdzie stoicie. Ma być głośno, mokro i tak intensywnie, by sąsiedzi chcieli wezwać policję. 😈🔥"
]

# BOSS FIGHTS (Zadania Specjalne przy 100% napięcia)
zadania_boss = [
    "🚨 PROTOKÓŁ ZERO: Oboje stajecie nago na środku pokoju. Napełniasz swoje usta alkoholem, a partner musi go spić bezpośrednio z Twojego gardła, podczas gdy Ty kontrolujesz jego oddech, zaciskając dłoń na jego karku.",
    "🚨 PROTOKÓŁ CAŁKOWITEJ WŁADZY: Dominacja absolutna! Przez 5 minut partner staje się Twoim przedmiotem. Nie ma prawa do ruchu, słowa ani mrugnięcia, podczas gdy Ty robisz z jego ciałem dokładnie to, na co miałeś ochotę od pierwszej minuty gry.",
    "🚨 PROTOKÓŁ REAKCJI ŁAŃCUCHOWEJ: Nagie 69 z jednym brutalnym warunkiem: ręce macie spięte za plecami (lub unieruchomione). Jedynym sposobem na komunikację jest język. Gra nie ruszy dalej, dopóki pokój nie wypełni się zapachem Waszego spełnienia.",
    "🚨 PROTOKÓŁ EWAKUACJI: Koniec patrzenia. Koniec czekania. Macie 10 minut na najbardziej prymarny, zwierzęcy seks w Waszym życiu, w miejscu, w którym nigdy wcześniej tego nie robiliście. Jeśli nie wrócicie spoceni i bez tchu – kara zostaje powtórzona.",
    "🚨 PROTOKÓŁ OSTATECZNEGO TABU: Wyznaj partnerowi swoją najbardziej mroczną, brudną fantazję, której do tej pory się wstydziłeś... a potem zmuś go, by zaczął ją realizować tu i teraz, bez zadawania pytań i bez cienia wstydu."
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
