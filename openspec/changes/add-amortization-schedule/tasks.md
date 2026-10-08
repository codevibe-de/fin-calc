# Tasks

## 1. Berechnung von der Ausgabe trennen

- [ ] 1.1 `monthly_payment(principal, annual_rate_pct, months)` in `loan_calculator.py` einführen und `calculate_monthly_payment` darauf umstellen; prüfen, dass die Zusammenfassung für 10000 / 5 / 2 zeichengleich bleibt
- [ ] 1.2 `test_loan_calculator.py` mit Tests für `monthly_payment` anlegen (Zinssatz 0 und Zinssatz 5); `pytest` ist grün

## 2. Tilgungsplan berechnen

- [ ] 2.1 `Row` und `amortization_schedule(principal, annual_rate_pct, months)` implementieren, letzte Restschuld auf 0.0; Tests für den zinslosen Fall, die Summen bei 250000 / 3.8 / 25 und „keine negative Restschuld“ sind grün
- [ ] 2.2 `yearly(rows)` implementieren, inklusive angebrochenem letztem Jahr; Tests für 2 Jahre und für 18 Monate sind grün

## 3. Ausgabe und Option

- [ ] 3.1 Tabellenausgabe des Plans nach der Zusammenfassung ergänzen; Test über `capsys` prüft Kopfzeile und letzte Zeile mit 0.00
- [ ] 3.2 Option `--monthly` mit `argparse` ergänzen; Test prüft 24 Zeilen bei 2 Jahren mit `--monthly` und den Jahresplan ohne Option
- [ ] 3.3 Kreditrechner in `README.md` kurz beschreiben (Aufruf, Option `--monthly`) und den dokumentierten Aufruf einmal ausführen

## Workflow follow-up

- Change archivieren, wenn alle Aufgaben erledigt sind: `/opsx:archive`
