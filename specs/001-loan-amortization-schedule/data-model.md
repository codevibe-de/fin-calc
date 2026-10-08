# Data Model: Tilgungsplan im Kreditrechner

Alle Planbeträge sind **ganze Cent (`int`)**, siehe [research.md](research.md), R1. Eingabegrößen
und Monatsrate bleiben `float`, wie bisher in der Zusammenfassung.

## Eingabe: Kredit

| Feld | Typ | Herkunft | Regel |
|---|---|---|---|
| `principal` | `float` | Prompt „Loan amount: “ | unverändert übernommen |
| `annual_rate` | `float` | Prompt „Annual interest rate (%): “ | Prozent, z. B. `5` für 5 % |
| `months` | `int` | `int(years * 12)` aus Prompt „Duration (years): “ | abgerundet wie bisher |

Die Eingaben werden nicht validiert (außerhalb des Scopes, siehe Spec).

## ScheduleRow (`typing.NamedTuple`)

Eine Zeile des Tilgungsplans.

| Feld | Typ | Bedeutung |
|---|---|---|
| `period` | `int` | Jahr bzw. Monat, ab 1 |
| `interest_cents` | `int` | in der Periode gezahlte Zinsen |
| `principal_cents` | `int` | in der Periode geleistete Tilgung |
| `balance_cents` | `int` | Restschuld am Periodenende |

**Invarianten** (gelten für jede erzeugte Liste `rows`):
- `rows[0].period == 1`, Perioden lückenlos aufsteigend (FR-003, FR-005)
- `len(rows) == ceil(months / period_months)` (SC-003); die letzte Zeile umfasst nur die
  restlichen Monate (FR-004)
- `rows[i].balance_cents == prev_balance − rows[i].principal_cents`, wobei `prev_balance` für
  `i = 0` gleich `Cent(principal)` ist (FR-008)
- `rows[-1].balance_cents == 0` (FR-009)
- alle Werte `>= 0`

## ScheduleTotals (`typing.NamedTuple`)

Die Summenzeile.

| Feld | Typ | Bedeutung |
|---|---|---|
| `interest_cents` | `int` | Σ `interest_cents`, entspricht „Total interest“ (FR-006) |
| `principal_cents` | `int` | Σ `principal_cents`, entspricht `Cent(principal)` (FR-006) |
| `payment_cents` | `int` | `interest_cents + principal_cents`, entspricht „Total repaid“ (FR-006) |

## Funktionen in `loan_calculator.py`

| Funktion | Schicht | Signatur | Zweck |
|---|---|---|---|
| `monthly_payment` | Rechnen | `(principal: float, annual_rate: float, months: int) -> float` | Monatsrate wie bisher (inkl. 0 %-Sonderfall) |
| `amortization_schedule` | Rechnen | `(principal: float, annual_rate: float, months: int, period_months: int) -> list[ScheduleRow]` | Plan mit `period_months = 12` (jährlich) oder `1` (monatlich) |
| `schedule_totals` | Rechnen | `(rows: list[ScheduleRow]) -> ScheduleTotals` | Summenzeile |
| `_to_cents` | Rechnen (Hilfsfunktion) | `(amount: float) -> int` | Rundung identisch zur `.2f`-Anzeige |
| `format_summary` | Formatieren | `(payment: float, months: int, principal: float) -> list[str]` | die bisherigen Zeilen der Zusammenfassung, zeichengleich |
| `format_schedule` | Formatieren | `(rows: list[ScheduleRow], totals: ScheduleTotals, period_label: str) -> list[str]` | Leerzeile, Kopfzeile, Planzeilen, Summenzeile |
| `parse_args` | Ein-/Ausgabe | `(argv: list[str] \| None) -> argparse.Namespace` | `--monthly` |
| `main` | Ein-/Ausgabe | `(argv: list[str] \| None = None) -> None` | Einstiegspunkt; einzige Stelle mit `input`/`print` |

`calculate_monthly_payment` entfällt. Es hat keine weiteren Aufrufer im Repository.

## Ablauf

```text
main(argv)
 ├─ parse_args(argv)                 # unbekannte Option → Exit 2, noch keine Ausgabe
 ├─ print Titel, input × 3           # unverändert
 ├─ months = int(years * 12)
 ├─ payment = monthly_payment(...)
 ├─ print format_summary(...)        # zeichengleich zu bisher
 ├─ rows = amortization_schedule(..., 1 if monthly else 12)
 └─ print format_schedule(rows, schedule_totals(rows), "Month" | "Year")
```
