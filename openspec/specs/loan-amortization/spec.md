# loan-amortization Specification

## Purpose
Zeigt für ein Annuitätendarlehen, wie sich die Raten über die Laufzeit auf Zinsen und Tilgung aufteilen und wie die Restschuld bis auf null sinkt.

## Requirements

### Requirement: Jährlicher Tilgungsplan
Nach der Zusammenfassung SHALL der Kreditrechner eine Tabelle mit einer Zeile je Laufzeitjahr ausgeben, mit den Spalten Jahr, Zinsen, Tilgung und Restschuld am Jahresende. Beträge erscheinen mit zwei Nachkommastellen.

#### Scenario: Zinsloser Kredit über zwei Jahre
- **WHEN** der Nutzer 10000 als Kreditbetrag, 0 als Zinssatz und 2 als Laufzeit in Jahren eingibt
- **THEN** zeigt der Plan zwei Zeilen: Jahr 1 mit Zinsen 0.00, Tilgung 5000.00, Restschuld 5000.00 und Jahr 2 mit Zinsen 0.00, Tilgung 5000.00, Restschuld 0.00

#### Scenario: Kredit mit Zinsen
- **WHEN** der Nutzer 10000 als Kreditbetrag, 5 als Zinssatz und 2 als Laufzeit in Jahren eingibt
- **THEN** sind die Zinsen in Jahr 1 höher als in Jahr 2 und die Tilgung in Jahr 1 niedriger als in Jahr 2

### Requirement: Plan geht vollständig auf
Die Summe der Zinsen im Plan MUST bis auf 0.01 den ausgegebenen Gesamtzinsen entsprechen, die Summe der Tilgung dem Kreditbetrag, und die Restschuld der letzten Zeile MUST als 0.00 erscheinen, nie als negativer Wert.

#### Scenario: Summen stimmen mit der Zusammenfassung überein
- **WHEN** der Nutzer 250000 als Kreditbetrag, 3.8 als Zinssatz und 25 als Laufzeit in Jahren eingibt
- **THEN** weicht die Summe der Zinsspalte um höchstens 0.01 von „Total interest“ ab, die Summe der Tilgungsspalte um höchstens 0.01 von 250000, und die letzte Restschuld lautet 0.00

### Requirement: Angebrochenes letztes Jahr
Ist die Laufzeit keine ganze Zahl von Jahren, SHALL die letzte Zeile nur die verbleibenden Monate umfassen.

#### Scenario: Laufzeit von anderthalb Jahren
- **WHEN** der Nutzer 1,5 Jahre Laufzeit eingibt (18 Monatsraten)
- **THEN** zeigt der Plan zwei Zeilen, wobei Jahr 2 die Monate 13 bis 18 umfasst und mit Restschuld 0.00 endet

### Requirement: Monatlicher Plan auf Wunsch
Mit der Option `--monthly` SHALL der Kreditrechner statt des jährlichen Plans eine Zeile je Monatsrate ausgeben, mit den Spalten Monat, Zinsen, Tilgung und Restschuld.

#### Scenario: Monatsplan
- **WHEN** der Nutzer den Rechner mit `--monthly` startet und 2 als Laufzeit in Jahren eingibt
- **THEN** zeigt der Plan 24 Zeilen, nummeriert von 1 bis 24

#### Scenario: Ohne Option
- **WHEN** der Nutzer den Rechner ohne Option startet
- **THEN** erscheint der jährliche Plan

### Requirement: Zusammenfassung bleibt unverändert
Monatsrate, Gesamtbetrag und Gesamtzinsen MUST in Text, Reihenfolge und Format wie bisher vor dem Tilgungsplan erscheinen.

#### Scenario: Bestehende Ausgabe
- **WHEN** der Nutzer 10000 als Kreditbetrag, 5 als Zinssatz und 2 als Laufzeit in Jahren eingibt
- **THEN** beginnt die Ausgabe nach den Eingaben wie bisher mit den Zeilen „Monthly payment“, „Total repaid“ und „Total interest“
