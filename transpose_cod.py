"""Übernimmt den CSV-Export der Seite https://www-genesis.destatis.de/genesis//online?operation=table&code=23211-0004 
und formt die mehrdimensionale Tabelle in eine einfache Tabelle mit den Spalten Jahr, Kategorie, Altersgruppe, Geschlecht, Anzahl Todesfälle um,
die somit zum Erstellung von Pivot-Tabellen geeignet ist."""

import csv

with open("23211-0004.csv", encoding="cp1252") as infile:
    read_header = csv.reader(infile, delimiter=";")
    for line in read_header:
        if line[0] == "" and line[2] == "Geschlecht":
            geschlecht = next(read_header)[2:]                                  # enthält "männlich", wenn darunter Zahlen für Männer stehen, sonst "weiblich"
        if line[0] == "" and line[2] == "Altersgruppen":                        # warten, bis die Zeile mit den Spaltenüberschriften erreicht ist
            altersgruppen = next(read_header)[2:]                                     # Spaltenüberschriften setzen 
            for index, eintrag in enumerate(altersgruppen):                           # Einträge "unter 1 Jahr" umbenennen in "0 Jahre", damit Excel korrekt sortieren kann
                if eintrag == "unter 1 Jahr":
                    altersgruppen[index] = "0 Jahre"
            break
    reader = csv.reader(infile, delimiter=";")
    todesursachen = list(reader)

jahre = set()
for line in todesursachen:
    try:
        jahr = int(line[0])
        jahre.add(jahr)
    except ValueError:
        pass

with open(f"Todesursachen Einzelwerte {min(jahre)}-{max(jahre)}.csv", "w", newline="", encoding="cp1252") as outfile:
    writer = csv.writer(outfile, delimiter = ";")               # Semikolon als Trennzeichen (wie von Excel erwartet)
    writer.writerow(["Jahr", "Kategorie", "Altersgruppe", "Geschlecht", "Todesfälle"])
    for eintrag in todesursachen:
        try:
            jahr = int(eintrag[0])                                        # Nur Zeilen aufnehmen, die auch Daten enthalten
        except ValueError:
            continue
        kategorie = eintrag[1]
        if kategorie == "Insgesamt":                              # Gesamtzahl der Sterbefälle nicht übernehmen
            continue
        for index, data in enumerate(eintrag[2:]):
            if altersgruppen[index] not in ("Insgesamt", "Alter unbekannt"): # nur Spalten mit definierter Altersgruppe übernehmen
                writer.writerow([jahr, kategorie, altersgruppen[index], geschlecht[index], data if data!="-" else "0"])