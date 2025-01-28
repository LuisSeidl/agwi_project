# SmartFarm

SmartFarm ist ein Tool für die Unterstützung von Landwirten. Die Primäre Funktion von SmartFarm ist das Management von Arbeitsaufträgen, damit der Landwirt immer den Überblick darüber hat was aktuell gemacht werden muss. Sekundär kann man mit SmartFarm auch seine Mitarbeiter, seinen Fuhrpark und seine Felder/Arbeitsplätze managen.

## Klassendiagramm
Die Klassen Auftrag, Mitarbeiter/Angestellter, Fahrzeug, Feld und Arbeitsart sind in der Datenbank gespeichert, wobei Arbeitsart wie ein Enum behandelt wird (kein Hinzufügen/löschen auf der Website möglich, nur direkt durch die MySQL Console). Die Restlichen klassen wurden in der Website berücksichtigt aber nicht vollständig implementiert.

![Klassendiagramm](Diagramme/Klassendiagramm_Smartfarm_final%20(2).png)

## Anwendungsdiagramm
Die auf der Website funktionierenden Anwendungsfälle sind: 
1. Auftrag hinzufügen
2. Auftrag bearbeiten
3. Auftragsstatus bearbeiten
4. Auftrag löschen
5. Fahrzeug hinzufügen
6. Fahrzeug löschen
7. Mitarbeiter hinzufügen
8. Mitarbeiter löschen
9. Feld hinzufügen
10. Feld löschen

![Anwendungsdiagramm](Diagramme/Anwendungsfalldiagramm_final.png)

## Skizze des Website-Layouts

![Website-Layout](Diagramme/IMG_1096.jpeg)

