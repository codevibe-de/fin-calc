# Design

## Context

`loan_calculator.py` ist absichtlich unaufgeräumt: `calculate_monthly_payment(p, r, n)` rechnet und druckt in einem, gibt nichts zurück und hat keine Tests. Der Zinssatz kommt in Prozent, die Laufzeit in Jahren und wird zu Monaten gerundet (`int(y * 12)`). Für den Code gelten die Regeln in `.claude/rules/python-style.md`.

## Goals / Non-Goals

**Goals:**

- Rechnen und Ausgeben trennen, damit Rate und Tilgungsplan ohne Eingabe-Mocking testbar sind.
- Jährlicher Plan als Verdichtung des monatlichen Plans, damit beide dieselben Zahlen liefern.

**Non-Goals:**

- Sondertilgungen, Zinsbindung, variable Zinsen.
- CSV- oder Datei-Export.
- Umbau der Eingabe-Prompts oder Übersetzung der Ausgabe.

## Decisions

- **Reine Funktionen statt Klasse.** `monthly_payment(principal, annual_rate_pct, months) -> float` und `amortization_schedule(principal, annual_rate_pct, months) -> list[Row]` mit `Row` als `NamedTuple(period, interest, principal, balance)`. Passt zum funktionalen Stil von `retirement_calculator.py`; eine Klasse brächte hier nichts.
- **Jahresplan durch Verdichtung.** `yearly(rows)` fasst je zwölf Monatszeilen zusammen; das letzte, angebrochene Jahr bekommt nur die übrigen Monate. Alternative: Jahreswerte mit eigener Formel rechnen — verworfen, weil die Summen dann von der Monatsrechnung abweichen können.
- **Restschuld der letzten Rate auf null setzen.** Fließkomma lässt nach der letzten Rate einen Rest im Bereich 1e-9; die letzte Zeile setzt die Restschuld auf 0.0 und schlägt den Rest der Tilgung zu, damit nie „-0.00“ erscheint.
- **`argparse` für `--monthly`.** Wie `--currency` in `retirement_calculator.py`; die Eingaben bleiben interaktiv.
- **`calculate_monthly_payment` bleibt als Druckfunktion erhalten**, nutzt aber `monthly_payment` — so bleibt die Zusammenfassung zeichengleich.

## Risks / Trade-offs

- [Rundung: Summe gerundeter Zeilen ≠ gerundete Gesamtsumme] → Test mit Toleranz 0.01, wie in der Spec gefordert.
- [Lange Ausgabe bei `--monthly` und 30 Jahren: 360 Zeilen] → bewusst so; der Jahresplan ist der Standard.
