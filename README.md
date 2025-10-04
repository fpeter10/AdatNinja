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
```

# 🥷 AdatNinja

**AdatNinja** is a versatile, command-line data handling tool that helps you quickly and flexibly manipulate tabular data (CSV, TSV).  
Whether it's changing separators, splitting columns, merging tables, or calculating statistics — AdatNinja handles everything quietly and precisely, like a real ninja. 🥷

---

## How to Use
---
- Enter your name when the program starts so the Ninja can greet you based on the time of day.
- Place all your data in a folder; you can select the folder when starting the program.
- Choose the command you want to run. The program will keep asking until all parameters are valid.
- Use the ***programs*** command to list all available programs.
- Use the ***list*** command to list additional available functions.
- Use the ***help*** command to view help. Once done, return to the main menu with the ***main*** command.
- From the main menu, the selected folder can be displayed with the ***wd*** command.
- Change the folder with the ***change wd*** command if needed.
- Tab is your friend — pressing it shows suggestions while typing commands.
- For multiple-choice options, start typing the second word to see suggestions.
- Exit anytime with the ***exit*** command, or return to the main menu with ***main***.
- Use the ***info*** command to see how many times you have used each program.
---

## ⚙️ Main Features
---
- **Calculate Statistics**  
    ***stat***  Quickly calculate minimum, maximum, average, standard deviation, median, and sum.
  
- **Wilcoxon and t-test Statistics**  
    ***wilcoxon and ttest***  Calculates statistics for all names and groups. For global calculation (all names and groups together), select `none`.
  
- **Normality Test**  
    ***normality***  Check if a given sample group follows a normal distribution.
  
- **Merge Tables**  
    ***merge***  Merge two tables based on a common identifier (`id`) or choose other join methods.
  
- **Relative Normalization**  
    ***relative***  Calculate ratios or percentages by group or globally.
  
- **Summarize Data**  
    ***summarize***  Calculate average, sum, min, and max for all names and groups.

- **Split Columns**  
    ***split_columns***  Split a complex column (e.g., `A_B_C`) into multiple separate columns.

- **Merge Columns**  
    ***merge_columns***  Combine separate columns (e.g., 'A', 'B', 'C') into one column with a chosen separator (e.g., `A_B_C`).

- **Convert to Long Format**  
    ***long_format***  AdatNinja processes only long-format data, so convert wide-format tables to long-format for processing.

- **Convert to Wide Format**  
    ***wide_format***  Convert a table back to standard wide format. Make sure to select all required columns.

- **Change Separator and Decimal**  
    ***change sep***  Easily change the file separator and choose the decimal mark (point or comma).

- **Print Table**  
    ***print_table***  Preview the table, including column types.

---

## Colorful Error Handling
---
Errors, warnings, and messages appear in color in the terminal if invalid values are entered.  
You can then correct the inputs and continue.

- **Green message**: everything ran successfully.  
- **Red message**: invalid file, column, or value — choose a correct one!  
- **Yellow message**: informational.  
- **Light blue**: code snippets.  
- **Dark blue**: tables.

---

## Reusing Previous Commands
---
- Use ***load*** to retrieve previous runs.  
- ***load last_code*** automatically shows the last 5 commands, while ***load code*** lets you access saved commands.  
- Select a command by number, e.g., ***load last_code 1*** for the most recent one — it persists even after exiting.  
- Then select what you want to do.  
- ***check*** prints the command for verification.  
- ***run*** executes the command again.  
- ***modify*** lets you edit all parameters interactively; press enter to keep the current value.  
- ***save*** stores it in the ***load code*** database with an optional note.

---

## 🚀 Usage

### 1. Installation

Install the latest Python version: [https://www.python.org/downloads/](https://www.python.org/downloads/)  

Then download the program:  
[https://github.com/fpeter10/AdatNinja.git](https://github.com/fpeter10/AdatNinja.git)

Open a command prompt (CMD). All required packages will be installed automatically, and updates are checked weekly.  
The easiest way to start is by clicking the **start_program** icon.

```bash
cd AdatNinja-main
python AdatNinja.py
