# CLI Contract: `loan_calculator.py`

## Aufruf

```text
python3 loan_calculator.py [--monthly]
python3 loan_calculator.py -h | --help
```

| Option | Wirkung |
|---|---|
| *(keine)* | Tilgungsplan je Laufzeitjahr (FR-003) |
| `--monthly` | Tilgungsplan je Monat statt je Jahr (FR-005) |
| `-h`, `--help` | Usage-Text von argparse, Exit 0, keine Prompts |
| unbekannte Option | Usage + Fehlermeldung auf **stderr**, Exit **2**, keine Ausgabe auf stdout (FR-011) |

## Eingabe (stdin, interaktiv, unverändert)

```text
=== Loan Calculator ===

Loan amount: <float>
Annual interest rate (%): <float>
Duration (years): <float>
```

## Ausgabe (stdout)

Reihenfolge:
1. Titel, Prompts und Zusammenfassung, **zeichengleich** zur bisherigen Version (FR-001)
2. Leerzeile
3. Kopfzeile: `f"{label:>5}{'Interest':>12}{'Principal':>12}{'Balance':>12}"` mit
   `label = "Year"` bzw. `"Month"`
4. je Planzeile: `f"{period:>5}{interest:>12.2f}{principal:>12.2f}{balance:>12.2f}"`
5. Summenzeile: `f"{'Total':<5}{interest:>12.2f}{principal:>12.2f}{payment:>12.2f}"`

Beträge werden aus Cent (`int`) als `cents / 100` formatiert. Es gibt keine Tausendertrennzeichen
und keine abschließende Leerzeile nach der Summenzeile.

Die Referenzausgabe für 10000 / 5 / 2.5 steht in der [Spec, Abschnitt „Ausgabeformat“](../spec.md#ausgabeformat).

## Exit-Codes

| Code | Fall |
|---|---|
| 0 | normaler Lauf, `--help` |
| 2 | unbekannte oder fehlerhafte Option (argparse) |
| ≠ 0 | ungültige Eingaben (z. B. Text statt Zahl, Laufzeit < 1 Monat): Verhalten wie bisher, nicht Teil dieses Features |
