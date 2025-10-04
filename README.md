# 🥷 AdatNinja
**AdatNinja** is a command-line tool that helps you handle data easily. It can merge tables, calculate different statistics, and reshape your data, and a lot more. It also catches errors and shows them in a colorful, easy-to-read way.

# 🥷 AdatNinja

**AdatNinja** egy sokoldalú, parancssoros adatkezelő eszköz, amely segít a táblázatos adatok (CSV, TSV) gyors és rugalmas átalakításában.  
Legyen szó szeparátor cseréről, oszlopok szétválasztásáról, táblák összefésüléséről vagy statisztikák számításáról — AdatNinja mindent elintéz, csendben, precízen, mint egy igazi ninja. 🥷

## Segítség a használatához
---
- Add meg a neved a program indításakor, hogy a Ninja tudjon üdvözölni a napszaknak megfelelően.
- Minden adatot egy mappába kell rakni, a program indításakor lehet mappát választani.
- Válassz egy parancsot amit végre szeretnél hajtani! A program addig fog kérdezni, amíg minden paraméter nem megfelelő.
- A ***programs*** paranccsal az elérhető programok nevét írhatod ki.
- A ***list*** paranccsal az elérhatő egyéb funkciókat lehet listázni.
- A ***help*** paranccsal a súgót lehet előhívni. Ha sikerült megtudni az infót a ***main*** pancssal lehet visszatérni.
- A fő menüből a kiválasztott mappa ***wd*** paranccsal kiíratható.
- Ha nem megfelelő a mappa ***change wd*** parancssal lehet mappát váltani.
- A tabulátor a barátunk a program használata során, lenyomva mutatja a javaslatokat.
- Többszörös választás esetén a második szótól kezdjük el írni, és kapjuk a lehetőségeket.
- Bármikor ki lehet lépni a programból az ***exit*** paranccsal, illetve a ***main*** paranccssal visszatérni a fő menübe.
- Az ***info*** paranccsal ki tudod íratni, hogy melyik programot hányszor használtad.
---

## ⚙️ Fő funkciók
---
- **Statisztikák számítása**  
      ***stat*** Minimum, maximum, átlag és szórás, medián és összeg gyorsan kiszámíthatók.
  
- **Wilcoxon és t-teszt statisztika teszt számítása**  
      ***wilcoxon és ttest*** Minden névre és minden csoportra kiszámítja a statisztikát, ha globálisan akarjuk (minde névre, minden csoportra egybe), akkor none -t kell választani
  
- **Normális eloszlás teszt**  
      ***normality*** Derítsd ki, hogy az adott minta csoport normális eloszlást mutat e!
  
- **Táblák összefésülése**  
      ***merge*** Két táblát a azonosító ('id') alapján összekapcsolhatsz, illetve válassz más kapcsolódás módok közül.
  
- **Adatok relatívizálása**  
     ***relative*** Csoportonként vagy globálisan számíthatsz arányokat vagy százalékot.
  
- **Adatok összegzése**  
     ***summarize*** Minden névre és minden csoportra kiszámítja az átlagot, összeget, min, max értéket.

- **Oszlopok szétválasztása**  
      ***split_columns*** Egy összetett oszlopot (pl. `A_B_C`) több külön oszlopra bonthatsz.

- **Oszlopok egyesítése egy komplex oszloppá**  
      ***merge_columns*** Az önálló oszlopokat (pl. 'A' 'B' 'C') egyesíti egyetlen oszloppá a kiválasztott elválasztóval (pl. 'A_B_C')

- **Hosszú formátummá alakítás**  
      ***long_format*** A Ninja csak hosszú formátumú adatot tud feldolgozni. Így mindig érdemes átalakítani az ember által olvashatót, a programnak megfelelő alakúvá.

- **Szélés formátummá vissza alakítás**  
      ***wide_format*** A táblázatot vissza alakítja normál széles formátummá. Fontos, hogy válaszd ki az összes oszlopot amire szükség van.
  
- **Szeparátor és tizedesjel módosítás**  
      ***change sep***Könnyedén átalakíthatod a fájlokat különböző elválasztókkal, illetve lehet választani tízedes pont, vagy vessző közül.
  
- **Tábla kiíratása**  
      ***print_table*** Ha nem tudod pontosan hogy néz ki a tábla, írasd ki, és kapsz infót az oszlopok típusáról is


## Színes hibakezelés: A hibák, figyelmeztetések színesen jelennek meg a terminálban ha bármilyen nem megfelelő értéket adtál meg. Ezután lehetőséged van javítani a megfelelőre.
---
- Zöld színű üzenet: minden rendben a program lefutott.
- Piros színű üzenet: Hibás fájl, oszlop, érték, válassz megfelelőt!
- Sárga színű üzenet: Infó.
- A kódokat világoskékkel.
- A táblázatokat sötétkékkel írja ki.
---

## Korábbi parancsok újra felhasználása
---
- A ***load*** paranccsal lehet az előző futtatásokat előhívni.
- A ***load last_code*** az előző 5-öt automatikusan, míg a ***load code*** az általunk mentet parancsokat lehet előhíni.
- Ezután kiválasztjuk a sorszámát, például ***load last_code 1*** a legutolsó, ez kilépés után is megmarad.
- Ezután kiválasztjuk mit szerenénk csinálni.
- ***check*** csak kiíratja ellenörzésre a továbbiakhoz.
- ***run*** újra futtatja
- ***modify*** módosítani lehet, minden paramétert végigkérdez, ami maradhat ott enter-t kell nyomni, egyébként át lehet írni.
- ***save*** elmenti a ***load code*** adatbázisba, amihez egy üzenetet is írharunk.
---
  
## 🚀 Használat

### 1. Telepítés

Telepítsd a legjabb python-t https://www.python.org/downloads/

Majd töltsd le a programot

https://github.com/fpeter10/AdatNinja.git

Nyiss meg egy parancssort a CMD paranccsal. Az összes szükséges csomagot automatikusan letölti, illetve hetente ellenőrzi, hogy nincs e frissítés.
A legegyszerűbb indítás a **start_program** ikonra kattintással lehetséges.

```bash

cd AdatNinja-main

python AdatNinja.py
