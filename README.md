# Todesursachen
Dieses Skript liest die Daten der amtlichen Todesursachenstatistik (23211-0004, https://www-genesis.destatis.de/genesis//online?operation=table&code=23211-0004) und der Bevölkerungsstatistik (12411-0008, https://www-genesis.destatis.de/genesis//online?operation=table&code=12411-0008) und erstellt daraus eine CSV-Datei mit Einzeldaten für eine Analyse z. B. mit Hilfe eines Excel-Pivot-Charts.

Es werden sowohl die absoluten Todesfallzahlen als auch die Anzahl Todesfälle pro 100.000 in der jeweiligen Geschlechts- und Alterskategorie ausgegeben.

Bei der Auswahl der Daten aus 12411-0008 ist darauf zu achten, dass alle Jahre eingeschlossen sind, die in der Abfrage 23211-0004 verwendet werden. In den Datensätzen für 1993 und 1994 sind Lücken auf Destatis, daher ist es sinnvoll, Daten erst ab 1995 abzurufen.

Was die zu berücksichtigenden Diagnosen angeht, können beliebige Auswahlen bei 23211-0004 getroffen werden. Es sollte aber beachtet werden, dass die Gruppen teils Untermengen von einander darstellen und so bei Vollauswahl zahlreiche Todesfälle mehrmals gezählt werden. Um sicherzustellen, dass jeder Todesfall nur einmal gewertet wird, eignet sich die Auswahl der Gruppen

- Bestimmte infektiöse und parasitäre Krankheiten
- Neubildungen
- Krankheiten des Blutes u. der blutbildenden Organe
- Endokrine, Ernährungs- u. Stoffwechselkrankheiten
- Psychische und Verhaltensstörungen
- Krankheiten d. Nervensystems u. d. Sinnesorgane
- Krankheiten des Kreislaufsystems
- Krankheiten des Atmungssystems
- Krankheiten des Verdauungssystems
- Krankheiten der Haut und der Unterhaut
- Krankh. des Muskel-Skelett-Systems u. Bindegewebes
- Krankheiten des Urogenitalsystems
- Schwangerschaft, Geburt und Wochenbett
- Best.Zustände mit Ursprung in der Perinatalperiode
- Angeb. Fehlbildungen,Deformitäten,Chromosomenanom.
- Symptome und abnorme klinische und Laborbefunde
- Äußere Ursachen von Morbidität und Mortalität

Die Summe der Fälle dieser Gruppen zusammengenommen entspricht genau der Anzahl der Gesamt-Todesfälle für den jeweiligen Datensatz.
