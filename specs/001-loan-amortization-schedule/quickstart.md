# Quickstart: Tilgungsplan validieren

## Voraussetzungen

- Python 3 und `uv` installiert
- Arbeitsverzeichnis: Repository-Root `fin-calc/`

## 1. Automatische Tests

```bash
uv run --with pytest pytest
```

Erwartet: Alle Tests grün, auch die bestehenden in `test_retirement_calculator.py`.

### Zuordnung Anforderung → Test (`test_loan_calculator.py`)

| Anforderung | Was geprüft wird |
|---|---|
| FR-001 | Ausgabe bis einschließlich „Total interest“ ist identisch zur bisherigen Ausgabe, mit und ohne `--monthly` |
| FR-002, FR-012, FR-013 | vollständige stdout-Ausgabe für 10000 / 5 / 2.5 entspricht exakt dem Spec-Beispiel |
| FR-003, FR-004 | Zeilenanzahl ⌈n/12⌉, letzte Jahreszeile umfasst nur die Restmonate (2.5 und 0.5 Jahre) |
| FR-005 | `--monthly` liefert n Zeilen, nummeriert 1 … n, keine Jahreszeilen |
| FR-006, FR-007 | Raster-Test: Summen gleich „Total interest“, Betrag und „Total repaid“, Zeilen addieren sich exakt |
| FR-008, FR-009 | Raster-Test: Restschuld-Kette stimmt, letzte Restschuld 0, kein `-0.00` in der Ausgabe |
| FR-010 | Restschuld Jahr *j* = Restschuld Monat 12·*j* |
| FR-011 | `main(["--bogus"])` → `SystemExit` mit Code 2, stdout leer |

Die Raster-Tests decken auch die Randfälle aus der Spec ab: 0 % Zins, Laufzeit unter einem Jahr,
ganzzahlige und angebrochene Laufzeit sowie 1.55 Jahre (→ 18 Monate).

## 2. Manuelle Prüfung

Jahresplan:

```bash
printf '10000\n5\n2.5\n' | python3 loan_calculator.py
```

Erwartet: Ausgabe wie im Spec-Beispiel ([spec.md › Ausgabeformat](spec.md#ausgabeformat)) mit
drei Jahreszeilen und der Summenzeile `Total      658.81    10000.00    10658.81`.

Monatsplan:

```bash
printf '10000\n5\n2.5\n' | python3 loan_calculator.py --monthly
```

Erwartet: 30 Monatszeilen. Monat 12 hat die Restschuld `6149.02`, Monat 30 die Restschuld `0.00`.
Die Summenzeile ist dieselbe wie oben.

Unbekannte Option:

```bash
python3 loan_calculator.py --bogus; echo "exit=$?"
```

Erwartet: Usage und Fehlermeldung auf stderr, kein Prompt, `exit=2`.

Hinweis: Beim Pipen per `printf` erscheinen die Prompts ohne Zeilenumbruch hintereinander. Das
war schon vor diesem Feature so und ist kein Fehler.
