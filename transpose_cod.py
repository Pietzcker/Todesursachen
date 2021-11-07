"""Übernimmt den CSV-Export der Seiten https://www-genesis.destatis.de/genesis//online?operation=table&code=23211-0004 und
https://www-genesis.destatis.de/genesis//online?operation=table&code=12411-0008 und generiert daraus eine einfache, 
normalisierte Tabelle mit den Spalten Jahr, Kategorie, Altersgruppe, Geschlecht, Anzahl Todesfälle (absolut bzw. pro 100.000),
die somit zum Erstellung von Pivot-Tabellen geeignet ist."""

import csv

with open("23211-0004.csv", encoding="cp1252") as infile:
    reader = csv.reader(infile, delimiter=";")
    for line in reader:
        if line[0] == "" and line[2] == "Geschlecht":
            geschlecht = next(reader)[2:]                                   # enthält "männlich", wenn darunter Zahlen für Männer stehen, sonst "weiblich"
        if line[0] == "" and line[2] == "Altersgruppen":                    # warten, bis die Zeile mit den Spaltenüberschriften erreicht ist
            altersgruppen = next(reader)[2:]                                # Spaltenüberschriften setzen 
            for index, eintrag in enumerate(altersgruppen):                 # Einträge "unter 1 Jahr" umbenennen in "0 Jahre", damit Excel korrekt sortieren kann
                if eintrag == "unter 1 Jahr":
                    altersgruppen[index] = "0 Jahre"
            break
    todesursachen = list(reader)

jahre = set()
for line in todesursachen:
    try:
        jahr = int(line[0])
        jahre.add(jahr)
    except ValueError:
        pass

altersgrenzen = [1, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85]
kohorten = ["0 Jahre"]
for pos in range(len(altersgrenzen)-1):                                     # Liste der relevanten Kohorten generieren
    kohorten.append(f"{altersgrenzen[pos]} bis unter {altersgrenzen[pos+1]} Jahre")
kohorten.append(f"{altersgrenzen[-1]} Jahre und mehr")

bevölkerung = {}

for jahr in jahre:                                                          # Bevölkerungszähler für die in der Datei verwendeten Jahre
    bevölkerung[jahr] = {}                                                  # und Kohorten vorbereiten (männlich/weiblich, Zähler auf 0)
    for kohorte in kohorten:
        bevölkerung[jahr][kohorte] = {"männlich": 0, "weiblich": 0}

with open("12411-0008.csv", encoding="cp1252") as infile:
    reader = csv.reader(infile, delimiter=";")
    for line in reader:
        if line[0] == "" and line[2] == "Deutsche":
            geschlecht_ag = next(reader)[2:]                                # enthält "männlich", wenn darunter Zahlen für Männer stehen, sonst "weiblich"
            break
    next(reader)                                                            # nächste Zeile enthält Familienstand, ist irrelevant, also überspringen

    for eintrag in reader:
        try:
            jahr = int(eintrag[0][-4:])                                     # extrahiert "2000" aus "31.12.2000"
        except ValueError:                                                  # Falls kein Datum in der ersten Zelle steht, überspringen
            continue
        if jahr not in jahre:                                               # Falls das Jahr nicht in unserem Datensatz vorkommt, überspringen
            continue
        altersgruppe = eintrag[1]                                           # passende Alterskohorte finden
        if altersgruppe == "unter 1 Jahr":
            ag_pos = 0
        elif altersgruppe.endswith("-Jährige"):                             # eines der Jahre innerhalb einer definierten Kohorte
            alter = int(altersgruppe.split("-")[0])
            for pos in range(len(altersgrenzen)-1):
                if altersgrenzen[pos] <= alter < altersgrenzen[pos+1]:
                    ag_pos = pos+1
                    break
        elif altersgruppe.endswith("Jahre und mehr"):                       # das höchste erfasste Alter oder darüber
            if not altersgruppe == kohorten[-1]:                            # sollte aktuell "85 Jahre und mehr" sein; falls sich das seitens
                raise ValueError                                            # Destatis ändert, wird dieser Fehler ausgelöst
            ag_pos = len(kohorten)-1
        else:
            raise ValueError                                                # Das sollte nicht passieren...

        for index, anzahl in enumerate(eintrag[2:]):                        # Jetzt die Zahlenwerte der aktuellen Zeile durchgehen
            if anzahl == "-":
                anzahl = 0
            else:
                anzahl = int(anzahl)
            bevölkerung[jahr][kohorten[ag_pos]][geschlecht_ag[index]] += anzahl # Addiere die aktuelle Zahl zur richtigen Kohorte

with open(f"Todesursachen Einzelwerte {min(jahre)}-{max(jahre)}.csv", "w", newline="", encoding="cp1252") as outfile:
    writer = csv.writer(outfile, delimiter = ";")               # Semikolon als Trennzeichen (wie von Excel erwartet)
    writer.writerow(["Jahr", "Kategorie", "Altersgruppe", "Geschlecht", "Todesfälle absolut", "Todesfälle pro 100.000"])
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
                if data == "-":
                    data = 0
                else:
                    data = int(data)
                data_100k = str(100000 * data / bevölkerung[jahr][altersgruppen[index]][geschlecht[index]]).replace(".", ",")
                writer.writerow([jahr, kategorie, altersgruppen[index], geschlecht[index], data, data_100k])