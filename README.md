# 🥷 AdatNinja
**AdatNinja** is a command-line tool that helps you handle data easily. It can merge tables, calculate different statistics, and reshape your data, and a lot more. It also catches errors and shows them in a colorful, easy-to-read way.

# 🥷 AdatNinja

**AdatNinja** egy sokoldalú, parancssoros adatkezelő eszköz, amely segít a táblázatos adatok (CSV, TSV) gyors és rugalmas átalakításában.  
Legyen szó szeparátor cseréről, oszlopok szétválasztásáról, táblák összefésüléséről vagy statisztikák számításáról — AdatNinja mindent elintéz, csendben, precízen, mint egy igazi ninja. 🥷

---

## ⚙️ Fő funkciók

- **Statisztikák számítása**  
     ***stat***  Minimum, maximum, átlag és szórás, medián és összeg gyorsan kiszámíthatók.

- **Wilcoxon és t-teszt statisztika teszt számítása**
     ***wilcoxon*** és ***ttest*** Minden névre és minden csoportra kiszámítja a statisztikát, ha globálisan akarjuk (minde névre, minden csoportra egybe), akkor none -t kell választani
  
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
  Könnyedén átalakíthatod a fájlokat különböző elválasztókkal (`;`, `,`, `|`, `tab`).









- **Színes hibakezelés**  
  Hibák, figyelmeztetések és visszajelzések színesen jelennek meg a terminálban (`colorama`).

---

## 🚀 Használat

### 1. Telepítés

Győződj meg róla, hogy a Python (3.9+) telepítve van, majd klónozd a repót:

```bash
git clone https://github.com/fpeti/AdatNinja.git
cd AdatNinja
pip install -r requirements.txt
