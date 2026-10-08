# Implementation Plan: Tilgungsplan im Kreditrechner

**Branch**: `sdd/10-speckit` | **Date**: 2026-10-08 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/001-loan-amortization-schedule/spec.md`

**Note**: This template is filled in by the `/speckit-plan` command; its definition describes the execution workflow.

## Summary

`loan_calculator.py` gibt nach der unveränderten Zusammenfassung einen Tilgungsplan aus: standardmäßig
je Laufzeitjahr, mit `--monthly` je Monat. Darunter steht eine Summenzeile mit Zinsen, Tilgung und
Gesamtzahlung.

Die Rechenlogik wird aus der bisherigen Druckfunktion in reine Funktionen herausgelöst
(Verfassung, Prinzip II). Gerechnet wird mit voller Float-Genauigkeit. Planwerte werden als
**kumulierte Summen auf Cent gerundet** und daraus pro Zeile die Differenzen gebildet; die letzte
Periode wird auf die Summenwerte der Zusammenfassung festgenagelt. Damit gelten die
Summengleichheit, die Restschuld-Kette und die Restschuld `0.00` per Konstruktion
(siehe [research.md](research.md), R1).

## Technical Context

**Language/Version**: Python 3 (lokal 3.14; Code bleibt kompatibel ab 3.9 wie das übrige Repo)

**Primary Dependencies**: nur Standardbibliothek (`argparse`, `typing.NamedTuple`)

**Storage**: N/A

**Testing**: pytest über `uv run --with pytest pytest` (Repository-Root)

**Target Platform**: jede Plattform mit Python 3, Terminal

**Project Type**: CLI (eigenständiges Skript)

**Performance Goals**: N/A. Höchstens wenige hundert Monatszeilen, Laufzeit vernachlässigbar.

**Constraints**: Bisherige Ausgabe zeichengleich, Planausgabe exakt nach Spec-Ausgabeformat,
keine Rundungsdifferenzen zwischen angezeigten Zeilen und Summen

**Scale/Scope**: eine Quelldatei (`loan_calculator.py`), eine neue Testdatei (`test_loan_calculator.py`)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Prinzip | Prüfung | Status vor Phase 0 | Status nach Phase 1 |
|---|---|---|---|
| I. Nur Standardbibliothek | Nur `argparse` und `typing` werden neu importiert, `requirements.txt` bleibt leer | ✅ | ✅ |
| II. Rechnen ≠ Ein-/Ausgabe | `calculate_monthly_payment` (rechnet + druckt) wird ersetzt durch reine Rechenfunktionen, reine Formatierfunktionen (liefern Zeilen als Strings) und `main()` als einzige Stelle mit `input`/`print` | ✅ (Bestandsverstoß wird hier behoben) | ✅ |
| III. Test je Anforderung | FR-001 bis FR-013 werden in `test_loan_calculator.py` per Kommentar-ID abgedeckt, Suite läuft mit `uv run --with pytest pytest` | ✅ | ✅ (Zuordnung in [quickstart.md](quickstart.md)) |
| IV. Zeichengleiche CLI-Ausgabe | Zusammenfassung unverändert (FR-001), Plan ist neue Ausgabe und in der Spec exakt beschrieben (FR-002, FR-012). Golden-Output-Test mit `capsys` | ✅ | ✅ |
| V. Code-Stil | Jede Funktion beginnt mit einem einzeiligen `#`-Kommentar, zwei Leerzeilen zwischen Top-Level-Funktionen | ✅ | ✅ |

Es gibt keine Verstöße, „Complexity Tracking“ bleibt leer.

## Project Structure

### Documentation (this feature)

```text
specs/001-loan-amortization-schedule/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output (/speckit-plan command)
├── data-model.md        # Phase 1 output (/speckit-plan command)
├── quickstart.md        # Phase 1 output (/speckit-plan command)
├── contracts/
│   └── cli.md           # Phase 1 output: Aufruf, Ein-/Ausgabe, Exit-Codes
└── tasks.md             # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code (repository root)

```text
loan_calculator.py         # geändert: reine Rechen- und Formatierfunktionen + main(argv)
test_loan_calculator.py    # neu: pytest-Tests für FR-001 … FR-013
retirement_calculator.py   # unberührt
test_retirement_calculator.py  # unberührt
```

**Structure Decision**: Die flache Struktur bleibt wie vorgegeben: eine Quelldatei und eine
Testdatei im Repository-Root. Es gibt keine Pakete und keine `src/`- oder `tests/`-Verzeichnisse.
Innerhalb von `loan_calculator.py` gibt es drei Schichten:

1. **Rechnen (rein)**: `monthly_payment`, `amortization_schedule`, `schedule_totals`
2. **Formatieren (rein, liefert `list[str]`)**: `format_summary`, `format_schedule`
3. **Ein-/Ausgabe**: `parse_args(argv)`, `main(argv=None)`. Nur `main` ruft `input` und `print` auf.

Die Signaturen stehen in [data-model.md](data-model.md), das Aufrufverhalten in
[contracts/cli.md](contracts/cli.md).

## Complexity Tracking

Keine Verstöße gegen die Verfassung, daher keine Einträge.
