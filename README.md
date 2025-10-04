# 🥷 AdatNinja
**AdatNinja** is a command-line tool that helps you handle data easily. It can merge tables, calculate different statistics, and reshape your data, and a lot more. It also catches errors and shows them in a colorful, easy-to-read way.

# 🥷 AdatNinja

**AdatNinja** egy sokoldalú, parancssoros adatkezelő eszköz, amely segít a táblázatos adatok (CSV, TSV) gyors és rugalmas átalakításában.  
Legyen szó szeparátor cseréről, oszlopok szétválasztásáról, táblák összefésüléséről vagy statisztikák számításáról — AdatNinja mindent elintéz, csendben, precízen, mint egy igazi ninja. 🥷

---
- Minden adatot egy mappába kell rakni, a program indításakor lehet mappát választani.
- Ha nem megfelelő a **change wd** parancssal lehet mappát váltani.
- A tabulátor a barátunk a program használata során, lenyomva mutatja a javaslatokat. 
- Bármikor ki lehet lépni az exit paranccsal, illetve a main paranccssal visszatérni a fő menübe.
- Add meg a neved a program indításakor, hogy a Ninja tudjon üdvözölni.
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
  
- **Szeparátor és tizedesjel módosítás**  
      ***change sep***Könnyedén átalakíthatod a fájlokat különböző elválasztókkal, illetve lehet választani tízedes pont, vagy vessző közül.
  
- **Tábla kiíratása**  
      ***print_table*** Ha nem tudod pontosan hogy néz ki a tábla, írasd ki, és kapsz infót az oszlopok típusáról is


## Színes hibakezelés  
  Hibák, figyelmeztetések színesen jelennek meg a terminálban ha bármilyen nem megfelelő értéket adtál meg. Ezután lehetőséged van javítani a megfelelőre.
  
## 
  Hibák, figyelmeztetések színesen jelennek meg a terminálban ha bármilyen nem megfelelő értéket adtál meg. Ezután lehetőséged van javítani a megfelelőre.
---

## 🚀 Használat

### 1. Telepítés

Telepítsd a legjabb python-t https://www.python.org/downloads/

Majd töltsd le a programot

https://github.com/fpeter10/AdatNinja.git

Nyiss meg egy parancssort a CMD paranccsal.

```bash

cd AdatNinja-main

python AdatNinja.py
