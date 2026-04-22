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
    {"kto": "ON", "tekst": "Gdybym miał zaplanować dla nas mój wymarzony dzień od A do Z, co byśmy robili po południu?"},
    {"kto": "ONA", "tekst": "Zgadnij, co JA uważam za najzabawniejszą wspólną wpadkę, jaka nam się przytrafiła?"},
    {"kto": "ON", "tekst": "Jak myślisz, z jakiego MOJEGO osobistego osiągnięcia w trakcie naszego związku jestem najbardziej dumny?"},
    {"kto": "ONA", "tekst": "Zgadnij, jaki był mój absolutnie ulubiony prezent, który kiedykolwiek od Ciebie dostałam?"},
    {"kto": "ON", "tekst": "Jaką jedną rzecz, którą wspólnie kupiliśmy do domu, uważam za najlepszą inwestycję?"},
    {"kto": "ONA", "tekst": "Zgadnij, które Twoje ubranie najchętniej bym potajemnie wyrzuciła do kosza?"},
    {"kto": "ON", "tekst": "Jak myślisz, za co najbardziej podziwiam Cię w Twoich relacjach z innymi ludźmi?"},
    {"kto": "ONA", "tekst": "Gdybym mogła magicznie pozbyć się jednego z moich własnych lęków, zgadnij co by to było?"},
    {"kto": "ON", "tekst": "Jakie wspomnienie z naszych pierwszych 3 miesięcy związku najczęściej wywołuje u mnie uśmiech?"},
    {"kto": "ONA", "tekst": "Zgadnij, do jakiego miejsca na świecie najchętniej zabrałabym Cię na naszą wymarzoną rocznicę?"},
    {"kto": "ON", "tekst": "Czego, według MNIE, najbardziej zazdroszczą nam inne pary z naszego otoczenia?"},
    {"kto": "ONA", "tekst": "Zgadnij, w jakiej domowej czynności lubię Cię obserwować najbardziej?"},
    {"kto": "ON", "tekst": "Jak myślisz, która piosenka sprawia, że od razu wyobrażam sobie naszą wspólną przyszłość?"},
    {"kto": "ONA", "tekst": "Gdybym miała spędzić z Tobą cały weekend bez prądu i internetu, zgadnij, od czego bym zaczęła?"},
    {"kto": "ON", "tekst": "Jaką jedną radę dałbym dzisiaj sobie samemu z dnia, w którym się poznaliśmy?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy według MNIE jesteśmy bardziej do siebie podobni, czy przeciwieństwa się przyciągają?"},
    {"kto": "ON", "tekst": "Co we mnie wzbudza największy szacunek do tego, jak radzisz sobie w kryzysowych sytuacjach?"},
    {"kto": "ONA", "tekst": "Zgadnij, która z moich przyjaźni znaczy dla mnie najwięcej zaraz po Tobie?"},
    {"kto": "ON", "tekst": "Gdybym miał opisać Twój uśmiech osobie, która nigdy Cię nie widziała, jakich słów bym użył?"},
    {"kto": "ONA", "tekst": "Jak myślisz, w jakich momentach najbardziej doceniam Twoje poczucie humoru?"},
    {"kto": "ON", "tekst": "Zgadnij, jakiego mojego marzenia z dzieciństwa jeszcze nie zrealizowałem, a bardzo bym chciał?"}
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

# --- POZIOM 1: Emocje, wspomnienia, codzienność i romantyzm ---
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
    {"kto": "ON", "tekst": "Gdy patrzę na Ciebie z drugiego końca pokoju, na co najczęściej zwracam uwagę?"},
    {"kto": "ONA", "tekst": "Zgadnij, jaka jest MOJA wymarzona randka, na którą wciąż czekam?"},
    {"kto": "ON", "tekst": "Jak myślisz, co najbardziej mnie rozczula, kiedy na Ciebie patrzę podczas snu?"},
    {"kto": "ONA", "tekst": "Gdybym mogła ubrać Cię jutro rano w cokolwiek, co by to było?"},
    {"kto": "ON", "tekst": "Zgadnij, jaka pieszczota bez podtekstu seksualnego sprawia mi największą przyjemność?"},
    {"kto": "ONA", "tekst": "Co we mnie sprawia, że czuję się przy Tobie najbardziej kobieca?"},
    {"kto": "ON", "tekst": "Czy według mnie nasz pierwszy pocałunek był w 100% idealny, czy mogło być lepiej?"},
    {"kto": "ONA", "tekst": "Zgadnij, co uwielbiam w sposobie, w jaki do mnie mówisz, gdy jesteśmy sami?"},
    {"kto": "ON", "tekst": "Jak myślisz, o czym najczęściej marzę, kiedy wspólnie milczymy w samochodzie?"},
    {"kto": "ONA", "tekst": "Jakie Twoje jedno słowo potrafi sprawić, że natychmiast mam lepszy humor?"},
    {"kto": "ON", "tekst": "Zgadnij, która z Twoich sukienek lub spódnic najmocniej działa na moją wyobraźnię?"},
    {"kto": "ONA", "tekst": "Jak myślisz, czy wolę, gdy kupujesz mi kwiaty, czy gdy robisz mi kolację niespodziankę?"},
    {"kto": "ON", "tekst": "Zgadnij, o co jestem najbardziej zazdrosny, nawet jeśli tego głośno nie mówię?"},
    {"kto": "ONA", "tekst": "Czy według mnie częściej ja inicjuję czułości w ciągu dnia, czy Ty?"},
    {"kto": "ON", "tekst": "Jak myślisz, za jaki moment z ostatniego miesiąca jestem Ci najbardziej wdzięczny?"},
    {"kto": "ONA", "tekst": "Zgadnij, co najbardziej lubię w Twoich dłoniach?"},
    {"kto": "ON", "tekst": "Wybierz jedno: czy wolę zasypiać w Twoich ramionach, czy na własnej połowie łóżka?"},
    {"kto": "ONA", "tekst": "Zgadnij, jaki rodzaj mojego uśmiechu jest przeznaczony tylko i wyłącznie dla Ciebie?"},
    {"kto": "ON", "tekst": "Co według mnie jest najzabawniejszą rzeczą, jaką robisz, gdy jesteś zestresowana?"},
    {"kto": "ONA", "tekst": "Jak myślisz, czego najbardziej nie mogę się doczekać w naszej wspólnej przyszłości?"},
    {"kto": "ON", "tekst": "Zgadnij, z jakiej naszej wspólnej cechy jestem najbardziej dumny?"}
]

# --- POZIOM 2: Napięcie, flirt, dotyk i pierwsze iskry ---
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
    {"kto": "ON", "tekst": "Jak bardzo kręci MNIE, gdy chodzisz po domu tylko w mojej koszulce?"},
    {"kto": "ONA", "tekst": "Zgadnij: czy lubię, gdy podczas całowania lekko ciągniesz mnie za włosy?"},
    {"kto": "ON", "tekst": "Jak myślisz, w jakich momentach najbardziej uwielbiam łapać Cię za talię?"},
    {"kto": "ONA", "tekst": "Zgadnij, jaki rodzaj dotyku rąk w kinie/pod stołem preferuję: delikatny czy zdecydowany?"},
    {"kto": "ON", "tekst": "Czy według mnie gra wstępna powinna zaczynać się rano od słów, czy wieczorem od dotyku?"},
    {"kto": "ONA", "tekst": "Gdy wchodzimy do sypialni, wolę, żebyś zrzucił mnie na łóżko, czy powoli popchnął na ścianę?"},
    {"kto": "ON", "tekst": "Zgadnij, co sprawia mi większą trudność: powstrzymanie się przed dotknięciem Cię w sklepie, czy przy znajomych?"},
    {"kto": "ONA", "tekst": "Czy pociąga mnie, gdy niespodziewanie chwytasz moje ręce i przyciskasz je nad moją głową?"},
    {"kto": "ON", "tekst": "Jak myślisz, czy kręcą mnie malinki i ślady, czy preferuję dyskrecję na skórze?"},
    {"kto": "ONA", "tekst": "Zgadnij, z jakiego miejsca na moim ciele najchętniej zlizywałabym coś słodkiego?"},
    {"kto": "ON", "tekst": "Czy podnieca mnie, gdy nosisz pod ubraniem koronkę, o której nikt poza mną nie wie?"},
    {"kto": "ONA", "tekst": "Wolisz powolne, głębokie pocałunki, w których badamy się nawzajem, czy dzikie i szybkie?"},
    {"kto": "ON", "tekst": "Zgadnij, jakie jest MOJE ulubione miejsce na Twojej szyi do składania pocałunków?"},
    {"kto": "ONA", "tekst": "Jak reaguję w myślach, gdy powoli i celowo rozpinasz swoją koszulę w mojej obecności?"},
    {"kto": "ON", "tekst": "Co nakręca MNIE bardziej: Twój zapach po gorącej kąpieli, czy zapach Twojej potu po treningu?"},
    {"kto": "ONA", "tekst": "Zgadnij, jaki mój drobny jęk najbardziej mówi Ci, że trafiasz w dziesiątkę?"},
    {"kto": "ON", "tekst": "Czy wolę, gdy przejmujesz inicjatywę i zaczynasz mnie rozbierać, czy gdy to ja robię to Tobie?"},
    {"kto": "ONA", "tekst": "Jak myślisz, czy kręci mnie zasłanianie mi oczu w trakcie gry wstępnej?"},
    {"kto": "ON", "tekst": "Zgadnij, które Twoje spojrzenie natychmiast podnosi mi tętno?"},
    {"kto": "ONA", "tekst": "Czy wolałabym wziąć ze mną długi prysznic, czy dołączyć do Ciebie w wannie pełnej piany?"},
    {"kto": "ON", "tekst": "Co według mnie jest najseksowniejszym dźwiękiem, jaki wydajesz podczas pocałunku?"}
]

# --- POZIOM 3: Sypialnia, gadżety, techniki i orgazmy ---
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
    {"kto": "ON", "tekst": "Co najbardziej nakręca MNIE, gdy rozmawiamy niegrzecznie (dirty talk)?"},
    {"kto": "ONA", "tekst": "Zgadnij, jakie jedno słowo wypowiedziane przez Ciebie w łóżku działa na mnie jak zapalnik?"},
    {"kto": "ON", "tekst": "Czy wolałbym szybkiego 'numerka' przed samym wyjściem do pracy, czy długiej nocy bez snu?"},
    {"kto": "ONA", "tekst": "Jakie moje jęki podniecają MNIE samej u siebie najbardziej – te głośne, czy tłumione w poduszkę?"},
    {"kto": "ON", "tekst": "Co myślisz o nagrywaniu naszych zbliżeń na dyktafon? Czy według MNIE to podniecające?"},
    {"kto": "ONA", "tekst": "Czy kiedykolwiek w pełni marzyłam o tym, byś przejął absolutną kontrolę nad moim ciałem na całą noc?"},
    {"kto": "ON", "tekst": "Gdy dochodzisz, co lubię wtedy w Tobie najbardziej: Twoją twarz, ciało czy dźwięk, który wydajesz?"},
    {"kto": "ONA", "tekst": "Co sądzę o przesyłaniu mi pikantnych zdjęć z pracy, by nakręcić mnie na wieczór?"},
    {"kto": "ON", "tekst": "Jaka część gry wstępnej wydaje MI się czasami zbyt długa, gdy już płonę z pożądania?"},
    {"kto": "ONA", "tekst": "Czy wolałabym robić to w całkowitej ciszy, by nikt z sąsiadów nie usłyszał, czy przy głośnej muzyce?"},
    {"kto": "ON", "tekst": "Zgadnij, o czym najczęściej fantazjuję, kiedy dotykasz mnie sama?"},
    {"kto": "ONA", "tekst": "Jaki mam stosunek do ostrego seksu na zgodę po kłótni (tzw. make-up sex)?"},
    {"kto": "ON", "tekst": "Gdybym przyniósł do sypialni jedwabny sznur lub kajdanki, w jakiej roli wolałbym Cię widzieć?"},
    {"kto": "ONA", "tekst": "Zgadnij, co bym poczuła, gdybyś obudził mnie w środku nocy pieszcząc mnie ustami?"},
    {"kto": "ON", "tekst": "Ile razy z rzędu udało nam się to zrobić podczas naszego najlepszego maratonu według MOJEJ pamięci?"},
    {"kto": "ONA", "tekst": "W jakim nietypowym miejscu w domu jeszcze tego nie robiliśmy, a według mnie MUSIMY?"},
    {"kto": "ON", "tekst": "Co jest dla mnie absolutnie kluczowe u Ciebie: technika oralna czy idealne tempo ruchów?"},
    {"kto": "ONA", "tekst": "Zgadnij: czy kręci mnie, gdy specjalnie zwlekasz z pozwoleniem mi na dojście?"},
    {"kto": "ON", "tekst": "Jakie pozycje są dla mnie najbardziej fizycznie męczące, a z których czerpię najczystszą przyjemność?"},
    {"kto": "ONA", "tekst": "Co we mnie sprawia, że całkowicie tracę panowanie nad swoim własnym rytmem oddechu?"},
    {"kto": "ON", "tekst": "Zgadnij, po jakim MOIM sygnale wiesz z absolutną pewnością, że za chwilę osiągnę szczyt?"}
]

# --- POZIOM 4: Tabu, granice, ekstremalne fantazje i fetysze ---
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
    {"kto": "ON", "tekst": "Jakie jest najmocniejsze obelżywe/niegrzeczne słowo, jakim chciałbym, żebyś mnie nazwała w łóżku?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy kiedykolwiek wyobrażałam sobie, że uprawiamy seks na oczach ukrytej kamery?"},
    {"kto": "ON", "tekst": "Czy podnieca MNIE myśl o tym, że mógłbym całkowicie decydować o tym, kiedy i jak możesz mieć orgazm?"},
    {"kto": "ONA", "tekst": "Jak myślisz, z czym kojarzy MI się lekkie przyduszanie (choking) podczas szczytowania?"},
    {"kto": "ON", "tekst": "Zgadnij, jak bym zareagował, gdybyś zaproponowała mi seks w klubie ze striptizem?"},
    {"kto": "ONA", "tekst": "Czy podnieca mnie myśl o tym, że mógłbyś patrzeć, jak bawię się sama przy innych ludziach?"},
    {"kto": "ON", "tekst": "Co według mnie jest najgorętszym zastosowaniem lodu podczas naszego seksu?"},
    {"kto": "ONA", "tekst": "Jak zareagowałabym, gdybyś bez uprzedzenia zakneblował mi usta w trakcie szczytowania?"},
    {"kto": "ON", "tekst": "Zgadnij, czy intryguje mnie seks analny, czy omijam ten temat w swoich fantazjach?"},
    {"kto": "ONA", "tekst": "Gdybyśmy mieli wziąć udział w orgii i tylko na siebie patrzeć z daleka, czy kręciłoby to MNIE?"},
    {"kto": "ON", "tekst": "Co myślisz, że czuję, patrząc na to, jak zlizujesz moje nasienie z własnych palców?"},
    {"kto": "ONA", "tekst": "Zgadnij, jak bym się czuła, mając ubraną wibracyjną zabawkę z pilotem podczas eleganckiej kolacji?"},
    {"kto": "ON", "tekst": "Jak myślisz, jak bardzo kręci MNIE głębokie gardło (deepthroat) u Ciebie?"},
    {"kto": "ONA", "tekst": "Czy sprawia MI przyjemność myśl o byciu lekko spoliczkowaną podczas bardzo ostrego seksu?"},
    {"kto": "ON", "tekst": "Zgadnij, jaki z MOICH dziwnych fetyszy obawiam się jeszcze wprowadzić w życie?"},
    {"kto": "ONA", "tekst": "Co bym pomyślała, gdybyś kazał mi założyć lateksowy strój uległej do sprzątania domu?"},
    {"kto": "ON", "tekst": "Jakie upokarzające polecenie z moich ust podnieciłoby Cię według MNIE najbardziej?"},
    {"kto": "ONA", "tekst": "Zgadnij, co bym powiedziała, gdybyś kazał mi klęczeć nago u podnóża łóżka przez całą noc?"},
    {"kto": "ON", "tekst": "Czy według mnie seks pod gołym niebem jest bardziej podniecający niż w drogim hotelu?"},
    {"kto": "ONA", "tekst": "Zgadnij, czy podnieca MNIE bycie wykorzystywaną na blacie w kuchni, podczas gdy robię obiad?"},
    {"kto": "ON", "tekst": "Najostrzejsza, najbardziej bezwstydna rzecz, jaką chciałbym z Tobą zrobić na parkingu nocą to... Zgadnij!"}
]
kary_l1 = [
    "Splećcie dłonie, zamknijcie oczy i wymieńcie się najdłuższym, najdelikatniejszym pocałunkiem w usta.",
    "Pocałuj partnera w miejsce na ciele, którego jeszcze dzisiaj nie całowałeś/aś.",
    "Opuszkami palców przejedź powoli po linii szczęki, karku i ramionach partnera przez 60 sekund.",
    "Zdejmij partnerowi skarpetki/buty używając do tego tylko jednej ręki, patrząc mu w oczy.",
    "Przytul partnera mocno od tyłu, połóż brodę na jego ramieniu i oddychajcie w tym samym rytmie przez minutę.",
    "Szepnij partnerowi do ucha swoją najbardziej niegrzeczną myśl z dzisiejszego dnia.",
    "Wymasuj dłonie i wnętrza dłoni partnera – powoli, palec po palcu przez 2 minuty.",
    "Przesuwaj czubkiem nosa po policzkach i szyi partnera, ale nie pozwól mu/jej Cię pocałować.",
    "Usiądź tak blisko partnera, by Wasze uda i kolana mocno się stykały do końca tej rundy.",
    "Trzymając dłonie na policzkach partnera, patrz mu prosto w oczy przez pełne 60 sekund w ciszy.",
    "Złap partnera za kark i złóż na jego/jej czole długi, bardzo czuły pocałunek.",
    "Znajdź na ciele partnera pulsujące miejsce (np. nadgarstek, szyja) i przyłóż tam usta na 30 sekund.",
    "Usiądź za partnerem i zrób mu powolny, relaksujący masaż ramion przez 2 minuty.",
    "Niech partner zamknie oczy, a Ty wódź lekko paznokciami po jego/jej przedramionach.",
    "Oprzyjcie się czołami o siebie, zamknijcie oczy i trzymajcie się za ręce przez minutę.",
    "Podnieś dłoń partnera i złóż delikatne pocałunki na wewnętrznej stronie jego/jej nadgarstka.",
    "Poproś partnera, by zamknął oczy, a następnie zarysuj kształt serca na jego udzie palcem.",
    "Pocałuj partnera w oba policzki, czubek nosa i na koniec w szyję tuż za uchem.",
    "Spleć nogi z nogami partnera pod stołem/na kanapie i nie rozłączajcie ich przez najbliższe 3 pytania.",
    "Baw się powoli i delikatnie włosami partnera przez okrągłą minutę.",
    "Połóż dłoń dokładnie na sercu partnera, zamknij oczy i wsłuchuj się w jego bicie przez 30 sekund.",
    "Złóż mokry, wyraźny pocałunek tuż nad obojczykiem partnera.",
    "Przez najbliższą minutę możecie rozmawiać i odpowiadać tylko szeptem, bardzo blisko swoich ust.",
    "Pocałuj wewnętrzną stronę dłoni partnera, a następnie przyłóż ją do swojego policzka.",
    "Daj partnerowi najsłodszy, najbardziej niewinny buziak w usta, nie otwierając ich."
]

kary_l2 = [
    "Zdejmij jeden, dowolny element ubrania partnera, używając do tego tylko zębów i jednej ręki.",
    "Rozepnij spodnie lub bluzkę partnera, ale nic z nich nie zdejmuj. Zostaw tak na jedną rundę.",
    "Złóż serię gorących pocałunków na wewnętrznej stronie ud partnera, zatrzymując się tuż przed strefą intymną.",
    "Weź łyk napoju i przekaż go partnerowi ustami podczas głębokiego pocałunku.",
    "Usiądź okrakiem na kolanach partnera (w ubraniu) i pozostań w tej pozycji przez całą następną rundę.",
    "Przygryź delikatnie dolną wargę partnera i pociągnij ją lekko do siebie.",
    "Wsuń dłonie pod koszulkę partnera na plecach i przyciśnij go/ją mocno do swojej klatki piersiowej na minutę.",
    "Pocałuj partnera namiętnie z języczkiem, jednocześnie mocno przyszpilając jego/jej nadgarstki do kanapy/łóżka.",
    "Zawiąż oczy partnerowi szalikiem lub krawatem na najbliższe 2 rundy.",
    "Zdejmij ze mnie jeden element ubrania (swojego), robiąc to możliwie najwolniej i najbardziej uwodzicielsko.",
    "Złap partnera za włosy (z tyłu głowy), odchyl jego głowę do tyłu i namiętnie pocałuj w szyję.",
    "Przejedź językiem po płatku ucha partnera, a następnie lekko go zassij.",
    "Wymasuj uda i pośladki partnera przez ubranie, używając dość silnego chwytu przez minutę.",
    "Zliż kroplę drinka lub wody z szyi lub obojczyka partnera.",
    "Połóż dłoń płasko na klatce piersiowej/piersiach partnera (przez ubranie) i masuj powoli przez 30 sekund.",
    "Przejmij kontrolę: posadź partnera na krześle, powiedz 'nie ruszaj się' i dotykaj go/jej wszędzie przez minutę (poza strefą V).",
    "Pocałuj partnera najgłębiej jak potrafisz przez 30 sekund, nie używając w ogóle rąk.",
    "Zjedzcie coś małego (paluszek, winogrono, kostka czekolady) z dwóch stron jednocześnie, aż Wasze wargi się spotkają.",
    "Wsuń palce za pasek spodni partnera i przyciągnij go/ją gwałtownie do namiętnego pocałunku.",
    "Drażnij usta partnera swoimi ustami – muskajcie się, ale nie pozwól mu się naprawdę pocałować przez 30 sekund.",
    "Rozepnij swój stanik (lub koszulę) jedną ręką, patrząc partnerowi wyzywająco w oczy.",
    "Połóż dłoń mocno na udzie partnera – jak najwyżej się da – i zostaw ją tam na najbliższe 3 minuty gry.",
    "Obliż powoli i zmysłowo swój palec, wsuń go do ust partnera na kilka sekund.",
    "Ugryź partnera delikatnie w ramię lub kark – tak, by poczuł, ale nie zabolało.",
    "Przesuwaj paznokciami wzdłuż kręgosłupa partnera, od karku aż po kość ogonową, powtarzaj przez minutę."
]

kary_l3 = [
    "Zdejmij wszystko poza bielizną. Pozostajesz tak ubrany/a do samego końca tej fazy gry.",
    "Włóż dłoń pod bieliznę partnera/partnerki. Złap pewnie i nie poruszaj ręką przez okrągłą minutę.",
    "Zdejmij partnerowi górną część garderoby samymi zębami – bez pomagania sobie rękami.",
    "Zrób partnerowi 2-minutowy taniec (lap dance) na kolanach, ocierając się o jego czułe miejsca.",
    "Poprowadź mokry ślad językiem od pępka partnera, w górę prosto do jego ust.",
    "Rozsuń nogi partnera i całuj wnętrze ud tuż przy linii bielizny przez 60 sekund.",
    "Zwiąż z tyłu ręce partnera i przez 2 minuty całuj jego/jej szyję, brzuch i uszy.",
    "Zrób partnerowi 'malinkę' w miejscu, w którym nikt inny jej jutro nie zauważy.",
    "Rozepnij dolną część garderoby partnera, wyjmij jego/jej dłoń i połóż na sobie, mówiąc 'dotykaj'.",
    "Użyj kostki lodu: przejedź nią po ciele partnera od dekoltu do pępka, a potem zliż wodę.",
    "Zasymuluj pozycję na jeźdźca w ubraniach: usiądź na partnerze i poruszaj biodrami przez 60 sekund.",
    "Połóż się na plecach, a partner ma prawo przez minutę pieścić Cię językiem tam, gdzie tylko zechce (poza bielizną).",
    "Wypnij się (lub odwróć tyłem) przed partnerem. Ma prawo mocno i dźwięcznie klepnąć Cię 3 razy w pośladki.",
    "Będziesz uległy/a przez następne 3 minuty. Partner decyduje, jakiej pieszczoty i gdzie sobie życzy.",
    "Weź palec partnera do ust, ssij go zmysłowo przez 30 sekund, patrząc mu przy tym głęboko w oczy.",
    "Zliż odrobinę alkoholu prosto z brzucha lub piersi/klatki partnera.",
    "Wsuń dłoń do spodni/pod spódnicę partnera od tyłu i wymasuj nagie pośladki przez 60 sekund.",
    "Rozchyl delikatnie bieliznę partnera z przodu, pochyl się i po prostu tam dmuchaj delikatnie przez minutę.",
    "Zamknij oczy, oprzyj się o kanapę/ścianę z rękami do góry. Partner ma minutę na robienie z Tobą, co zechce.",
    "Wejdź w przestrzeń osobistą partnera, chwyć go za gardło (bardzo delikatnie!) i pocałuj agresywnie.",
    "Niech partner/partnerka nałoży na Twoje usta coś słodkiego (lub alkohol), a Ty musisz to wetrzeć w jego/jej usta pocałunkiem.",
    "Zdejmij jedną sztukę swojej bielizny (bez zdejmowania reszty ubrań) i rzuć ją w partnera.",
    "Przyłóż usta do ucha partnera i zacznij głośno i zmysłowo jęczeć przez 30 sekund.",
    "Przejmij kontrolę: ułóż partnera w dowolnej pozycji na kanapie/krześle i nie pozwól mu się ruszyć przez 2 minuty, samemu go dotykając.",
    "Ściągnij spodnie/spódnicę partnera aż do kolan. Grajcie tak do następnej wylosowanej kary."
]

kary_l4 = [
    "Zdejmij z siebie absolutnie wszystko. Do końca gry pozostajesz całkowicie nago.",
    "Zejdź w dół. Masz 2 pełne minuty (nastawcie stoper) na seks oralny, zrób to najlepiej jak potrafisz.",
    "Załóż opaskę na oczy partnera. Rozbierz go do naga i pieść rękami, nie dając mu dotknąć Ciebie.",
    "Seks manualny (użyj dłoni) z pełnym zaangażowaniem przez 3 minuty, powiedz partnerowi, by patrzył na Twoją twarz.",
    "Seks oralny przez 2 minuty, po czym musisz gwałtownie przestać i nie wolno Ci dokończyć przez 3 kolejne rundy.",
    "Połóż się na plecach. Partner siada na Twojej twarzy (w bieliźnie lub bez) na pełne 60 sekund.",
    "Jeśli macie w pobliżu gadżet (wibrator, żel), użyj go na partnerze lub na sobie przez 2 minuty na oczach partnera.",
    "Oprzyj partnera/partnerkę o ścianę, odsłoń, co trzeba i wejdź w niego/nią na co najmniej minutę, zanim wrócicie do gry.",
    "Wykonuj masturbację przed partnerem, każąc mu/jej komentować to, co właśnie robisz przez 2 minuty.",
    "Zwiąż ręce partnera. Doprowadź go/ją oralnie na sam skraj orgazmu (edging), po czym przerwij i zostaw go/ją tak na minutę.",
    "Wejdź pod stół/kanapę i zdejmij bieliznę partnera zębami, a potem 'podziękuj' mu/jej ustami przez minutę.",
    "Odwróć partnera od siebie (na pieska), zdejmij wszystko co blokuje dostęp, i zasymuluj maksymalnie ostry seks w powietrzu lub z penetracją na minutę.",
    "Zliż alkohol z najbardziej intymnego miejsca na ciele partnera.",
    "Zejdź na kolana przed partnerem i błagaj go, by pozwolił Ci zdjąć swoje majtki.",
    "Pozycja 69 przez pełne 3 minuty. Nastawcie stoper i nie ma taryfy ulgowej.",
    "Usiądź okrakiem na nagim partnerze i ocierajcie się (grinding) bez wchodzenia w siebie przez 2 minuty.",
    "Rozsuń nogi partnera na boki, zablokuj je swoimi udami i użyj języka tam, gdzie partner lubi najbardziej.",
    "Spoliczkuj delikatnie partnera (za zgodą), chwyć mocno za włosy i zacznij zaspokajać go/ją ustami.",
    "Krzyknij lub głośno wyjęcz imię partnera, tak jak robisz to tuż przed szczytowaniem.",
    "Podnieś nogę partnerki/partnera, oprzyj ją na swoim ramieniu i zacznij pieszczoty intymne na stojąco przez 2 minuty.",
    "Nakarm partnera w sypialni: nabierz sok/alkohol w usta i wlej mu/jej prosto do gardła, całując głęboko.",
    "Przyjmij w 100% uległą pozycję, a partner przez 3 minuty robi z Twoim ciałem to, na co tylko ma ochotę.",
    "Wsadź palce (swoje lub partnera) w swoje strefy intymne, a następnie daj partnerowi do oblizania.",
    "Wykonaj pełny striptiz. Kiedy będziesz już nago, usiądź na twarzy/kolanach partnera.",
    "Kary telewizyjne dobiegły końca. Telefon na bok. Idziecie do sypialni wykończyć się nawzajem. 😈"
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
        "phase": "intro",  
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
    if state["phase"] == "intro":
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
