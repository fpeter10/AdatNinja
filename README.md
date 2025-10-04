# 🥷 AdatNinja
**AdatNinja** is a command-line tool that helps you handle data easily. It can merge tables, calculate different statistics, and reshape your data, and a lot more. It also catches errors and shows them in a colorful, easy-to-read way.

# 🥷 AdatNinja

**AdatNinja** egy sokoldalú, parancssoros adatkezelő eszköz, amely segít a táblázatos adatok (CSV, TSV) gyors és rugalmas átalakításában.  
Legyen szó szeparátor cseréről, oszlopok szétválasztásáról, táblák összefésüléséről vagy statisztikák számításáról — AdatNinja mindent elintéz, csendben, precízen, mint egy igazi ninja. 🥷

---

## ⚙️ Fő funkciók

- **Statisztikák számítása**  
  Minimum, maximum, átlag és szórás, medián és összeg gyorsan kiszámíthatók.

- **Wilcoxon és t-teszt statisztika teszt számítása**  
  Minden névre és minden csoportra kiszámítja, ha globálisan akarjuk, akkor none -t kell választani.

- **Szeparátor és tizedesjel módosítás**  
  Könnyedén átalakíthatod a fájlokat különböző elválasztókkal (`;`, `,`, `|`, `tab`).

- **Oszlopok szétválasztása**  
  Egy összetett oszlopot (pl. `A_B_C`) több külön oszlopra bonthatsz.

- **Táblák összefésülése**  
  Két táblát egy közös azonosító (`id_col`) alapján összekapcsolhatsz.

- **Adatok relatív normalizálása**  
  Csoportonként vagy globálisan számíthatsz arányokat vagy százalékokat.



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
