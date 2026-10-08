# Proposal

## Why

Der Kreditrechner nennt nur Monatsrate, Gesamtbetrag und Gesamtzinsen. Wer einen Kredit vergleicht, will aber sehen, wie sich die Raten über die Laufzeit auf Zinsen und Tilgung verteilen und wie schnell die Restschuld sinkt — genau das zeigt ein Tilgungsplan.

## What Changes

- Der Kreditrechner gibt nach der bisherigen Zusammenfassung einen jährlichen Tilgungsplan aus: je Jahr gezahlte Zinsen, Tilgung und Restschuld am Jahresende.
- Mit der Option `--monthly` erscheint der Plan stattdessen Monat für Monat.
- Die bisherige Zusammenfassung (Monatsrate, Gesamtbetrag, Gesamtzinsen) bleibt unverändert.
- Die Berechnung wird von der Ausgabe getrennt, damit sie testbar ist; dazu kommen die ersten Tests für den Kreditrechner.

## Capabilities

### New Capabilities

- `loan-amortization`: Tilgungsplan eines Annuitätendarlehens — Aufteilung der Raten in Zinsen und Tilgung und Verlauf der Restschuld, jährlich oder monatlich.

### Modified Capabilities

## Impact

- `loan_calculator.py`: neue Ausgabe, neue Option `--monthly`, Berechnung als eigene Funktionen.
- Neu: `test_loan_calculator.py`.
- Keine neuen Abhängigkeiten; `retirement_calculator.py` ist nicht betroffen.
