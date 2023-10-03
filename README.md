# shopware6BestandsUpdate

Updated den Bestand von Shopware 6 Artikeln ausgehend von einer .csv-Datei

Ausgehend von diesem Forumsbeitrag im Shopware 6 Forum: https://forum.shopware.com/t/lagerbestand-csv-import/68521

**Das Problem:**

Updaten des Bestandes von Artikeln in Shopware 6 setzt zwingend voraus dass man die ProductID ermittelt um dann mit dem Datei-Import arbeiten zu können.

Die .csv-Datei muss wie folgt aufgebaut sein:
(Trennzeichen: ",")

| ARTIKELNUMMER | BESTAND |
|---------------|---------|
| ART0815 | 12 |
| GUMMIENTE | 14 |
| WASSER_1_l | 23 |
| 150007 | 4 |

**ACHTUNG: Die .csv-Datei darf KEINE Überschrift beinhalten - einfach nur Artikelnummer und Bestand in jeder Zeile!**

**Beispieldatei:**
```
ART0815,12
GUMMIENTE,14
WASSER_1_l,23
```
[artikel.csv](artikel.csv)

Der Aufruf erfolgt nun wie folgt:
```
shopwareUpdater --url=https://www.meinshop.de --username=admin --passwort=geheim --datei=artikel.csv
```

Eine entsprechende .exe-Datei kann man unter [Releases](https://github.com/ThomasChr/shopware6BestandsUpdate/releases) runterladen
