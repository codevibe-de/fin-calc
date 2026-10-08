---

description: "Task list for feature implementation: Tilgungsplan im Kreditrechner"
---

# Tasks: Tilgungsplan im Kreditrechner

**Input**: Design documents from `/specs/001-loan-amortization-schedule/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/cli.md, quickstart.md

**Tests**: Pflicht nach Verfassung, Prinzip III: Jede Anforderung (FR-001 … FR-013) hat einen
pytest-Test, gekennzeichnet per Kommentar mit der FR-ID. Die Tests werden zuerst geschrieben und
müssen vor der Implementierung fehlschlagen.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2)
- Include exact file paths in descriptions

## Path Conventions

Flache Struktur laut plan.md: `loan_calculator.py` und `test_loan_calculator.py` im
Repository-Root. Keine `src/`- oder `tests/`-Verzeichnisse.

**Gilt für jede Task, die Python-Code schreibt** (`.claude/rules/python-style.md`, Prinzip V):
Jede Funktion, auch jede Testfunktion, beginnt mit einem einzeiligen `#`-Kommentar als erster
Body-Zeile. Zwischen Top-Level-Funktionen stehen genau zwei Leerzeilen. Es werden nur Module der
Standardbibliothek importiert (Prinzip I); einzige Ausnahme ist `pytest` in der Testdatei.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Bisheriges Verhalten als Referenz sichern und Testgerüst anlegen

- [ ] T001 Referenzausgabe der **unveränderten** Version erfassen, solange `loan_calculator.py` noch nicht geändert ist: Für jeden Fall `printf '<betrag>\n<zins>\n<jahre>\n' | python3 loan_calculator.py` ausführen, für (10000, 5, 2.5), (1200, 0, 1.5), (1234.56, 3.75, 0.5) und (10000, 5, 2). Die stdout-Texte exakt als Dict-Konstante `LEGACY_OUTPUTS` (Schlüssel: Tupel der drei Eingabestrings) in der neuen Datei `test_loan_calculator.py` ablegen. Hinweis: Prompts erscheinen ohne Zeilenumbruch, z. B. `"=== Loan Calculator ===\n\nLoan amount: Annual interest rate (%): Duration (years): \nMonthly payment:      355.29\n..."`.
- [ ] T002 In `test_loan_calculator.py` die Hilfsfunktion `run_main(monkeypatch, capsys, answers, argv)` anlegen. Sie ersetzt `builtins.input` per `monkeypatch` durch eine Funktion, die den Prompt mit `print(prompt, end="")` ausgibt (wie das echte `input` ohne Terminal) und die nächste Antwort aus `answers` liefert. Dann ruft sie `loan_calculator.main(argv)` auf und gibt `capsys.readouterr().out` zurück.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Rechnen von Ein-/Ausgabe trennen (Prinzip II), ohne die Ausgabe zu verändern. Gleichzeitig `main(argv)` testbar machen.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T003 Test FR-001 (Basis) in `test_loan_calculator.py`: Für jeden Fall aus `LEGACY_OUTPUTS` muss `run_main(..., argv=[])` mit `LEGACY_OUTPUTS[fall]` **beginnen** (`startswith`). Kommentar `# FR-001`. Muss jetzt fehlschlagen, weil `main` noch kein `argv` annimmt.
- [ ] T004 [P] Unit-Tests in `test_loan_calculator.py` für `monthly_payment` und `_to_cents`: `f"{monthly_payment(10000, 5, 30):.2f}" == "355.29"`, `monthly_payment(1200, 0, 18) == 1200 / 18`, `_to_cents(658.81) == 65881`, `_to_cents(0.0) == 0`, `_to_cents(2.675) == 267` (Rundung wie `f"{2.675:.2f}"`).
- [ ] T005 [P] In `loan_calculator.py` die reinen Funktionen `monthly_payment(principal: float, annual_rate: float, months: int) -> float` (Formel und 0 %-Sonderfall exakt wie bisher in `calculate_monthly_payment`) und `_to_cents(amount: float) -> int` als `round(float(f"{amount:.2f}") * 100)` anlegen (research.md R1).
- [ ] T006 In `loan_calculator.py` die reine Funktion `format_summary(payment: float, months: int, principal: float) -> list[str]` anlegen. Sie liefert `["", f"Monthly payment:  {x:>10.2f}", f"Total repaid:     {x * n:>10.2f}", f"Total interest:   {x * n - p:>10.2f}"]` mit exakt den bisherigen Ausdrücken. Das führende `""` ersetzt das bisherige `"\n"` am Anfang.
- [ ] T007 In `loan_calculator.py` die Funktion `parse_args(argv: list[str] | None) -> argparse.Namespace` mit einem `argparse.ArgumentParser` (noch ohne Optionen) anlegen. `main()` zu `main(argv: list[str] | None = None) -> None` umbauen: Zuerst `parse_args(argv)`, dann Titel, die drei `input`-Aufrufe (Prompts unverändert), `months = int(years * 12)`, `monthly_payment(...)`, jede Zeile aus `format_summary(...)` per `print`. `calculate_monthly_payment` löschen. Danach sind T003 und T004 grün.

**Checkpoint**: Ausgabe identisch zur Referenz, Rechenlogik rein. Mit `uv run --with pytest pytest` sind alle Tests grün.

---

## Phase 3: User Story 1 - Jährlicher Tilgungsplan (Priority: P1) 🎯 MVP

**Goal**: Nach der unveränderten Zusammenfassung erscheint ein Jahresplan mit Summenzeile.

**Independent Test**: `printf '10000\n5\n2.5\n' | python3 loan_calculator.py` gibt exakt das Jahresplan-Beispiel aus spec.md › Ausgabeformat aus. Zinssumme, Tilgungssumme und Gesamtzahlung stimmen auf den Cent mit der Zusammenfassung überein.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T008 [P] [US1] Golden-Test in `test_loan_calculator.py` (Kommentar `# FR-002, FR-012, FR-013`): `run_main(..., ["10000", "5", "2.5"], [])` ist **exakt gleich** `LEGACY_OUTPUTS[("10000", "5", "2.5")]` + `"\n Year    Interest   Principal     Balance\n    1      412.54     3850.98     6149.02\n    2      215.52     4048.00     2101.02\n    3       30.75     2101.02        0.00\nTotal      658.81    10000.00    10658.81\n"`.
- [ ] T009 [US1] Tests für `amortization_schedule(principal, annual_rate, months, 12)` in `test_loan_calculator.py` (Kommentar `# FR-003, FR-004`):
  - Zeilenzahl gleich `ceil(months / 12)` für 30, 24, 6 und 18 Monate (18 ergibt sich aus 1.55 Jahren).
  - Perioden `1 … k`, lückenlos.
  - Für (10000, 5, 30) exakt `[ScheduleRow(1, 41254, 385098, 614902), ScheduleRow(2, 21552, 404800, 210102), ScheduleRow(3, 3075, 210102, 0)]`.
  - Für (1200, 0, 18) exakt `[ScheduleRow(1, 0, 80000, 40000), ScheduleRow(2, 0, 40000, 0)]`.
- [ ] T010 [US1] Parametrisierter Raster-Test in `test_loan_calculator.py` (Kommentar `# FR-006, FR-007, FR-008, FR-009`).
  - Raster: Beträge `[1000, 1234.56, 10000, 250000, 99999.99]` × Zinssätze `[0, 0.5, 3.75, 5, 12, 25]` × Jahre `[0.5, 1, 1.55, 2.5, 10, 30]` × `period_months` `[12, 1]`, mit `months = int(years * 12)`.
  - Geprüft wird:
    - `f"{totals.interest_cents / 100:.2f}" == f"{x * n - p:.2f}"`, `totals.principal_cents == _to_cents(p)` und `f"{totals.payment_cents / 100:.2f}" == f"{x * n:.2f}"`
    - Σ Zeilenwerte == Summenwerte
    - `rows[i].balance_cents == prev_balance − rows[i].principal_cents` mit `prev_balance = _to_cents(principal)` für i = 0
    - `rows[-1].balance_cents == 0`, alle Werte `>= 0`
    - `"-0.00"` kommt in `format_schedule(...)` nicht vor.

### Implementation for User Story 1

- [ ] T011 [P] [US1] In `loan_calculator.py` die beiden `typing.NamedTuple`-Klassen anlegen (data-model.md): `ScheduleRow(period: int, interest_cents: int, principal_cents: int, balance_cents: int)` und `ScheduleTotals(interest_cents: int, principal_cents: int, payment_cents: int)`.
- [ ] T012 [US1] In `loan_calculator.py` die Funktion `amortization_schedule(principal: float, annual_rate: float, months: int, period_months: int) -> list[ScheduleRow]` nach research.md R1 implementieren:
  1. `x = monthly_payment(...)`, `m = annual_rate / 100 / 12`, `balance = principal`, kumulierte Floats `cum_i = cum_p = 0.0`, `total_p = _to_cents(principal)`.
  2. Für k = 1 … months: `i = balance * m`, `pr = x - i`, `balance -= pr`, `cum_i += i`, `cum_p += pr`.
  3. Periodenende ist, wenn `k % period_months == 0` oder `k == months`. Dort gilt:
     - `ci = _to_cents(x * months - principal) if k == months else _to_cents(cum_i)`
     - `cp = total_p if k == months else _to_cents(cum_p)`
     - Zeile `ScheduleRow((k - 1) // period_months + 1, ci - prev_ci, cp - prev_cp, total_p - cp)` anhängen, dann `prev_ci, prev_cp = ci, cp`.
  4. Die Invarianten aus data-model.md müssen gelten: „`rows[-1].balance_cents == 0`“, „alle Werte `>= 0`“.
- [ ] T013 [US1] In `loan_calculator.py` die Funktion `schedule_totals(rows: list[ScheduleRow]) -> ScheduleTotals` implementieren: Summe der Zinsen, Summe der Tilgung, `payment_cents = interest_cents + principal_cents`.
- [ ] T014 [US1] In `loan_calculator.py` die Funktion `format_schedule(rows: list[ScheduleRow], totals: ScheduleTotals, period_label: str) -> list[str]` implementieren, exakt nach contracts/cli.md:
  - `""`
  - `f"{period_label:>5}{'Interest':>12}{'Principal':>12}{'Balance':>12}"`
  - je Zeile `f"{period:>5}{interest/100:>12.2f}{principal/100:>12.2f}{balance/100:>12.2f}"`
  - `f"{'Total':<5}{interest/100:>12.2f}{principal/100:>12.2f}{payment/100:>12.2f}"`
- [ ] T015 [US1] In `main()` in `loan_calculator.py` nach der Zusammenfassung `rows = amortization_schedule(principal, rate, months, 12)` berechnen und jede Zeile aus `format_schedule(rows, schedule_totals(rows), "Year")` per `print` ausgeben. Danach sind T008 bis T010 und T003 grün.

**Checkpoint**: User Story 1 ist vollständig und unabhängig testbar (MVP).

---

## Phase 4: User Story 2 - Monatlicher Tilgungsplan mit `--monthly` (Priority: P2)

**Goal**: Mit `--monthly` erscheint der Plan Monat für Monat statt Jahr für Jahr.

**Independent Test**: `printf '10000\n5\n2.5\n' | python3 loan_calculator.py --monthly` gibt 30 Monatszeilen aus, Monat 12 mit der Restschuld `6149.02`, Monat 30 mit `0.00`, dazu dieselbe Summenzeile. `python3 loan_calculator.py --bogus` endet mit Exit 2 ohne Prompt.

### Tests for User Story 2 ⚠️

- [ ] T016 [P] [US2] Test in `test_loan_calculator.py` (Kommentar `# FR-001, FR-005`) für `run_main(..., ["10000", "5", "2.5"], ["--monthly"])`:
  - Die Ausgabe beginnt mit `LEGACY_OUTPUTS[...]`.
  - Die nächste Zeile ist leer, danach folgt `"Month    Interest   Principal     Balance"`.
  - Es folgen 30 Planzeilen mit den Perioden 1 … 30, die Zeile für Monat 1 lautet exakt `"    1       41.67      313.63     9686.37"`.
  - Die Zeile für Monat 12 endet auf `"6149.02"`, die für Monat 30 auf `"0.00"`.
  - Die letzte Zeile ist `"Total      658.81    10000.00    10658.81"`.
  - Keine Zeile beginnt mit `" Year"`.
- [ ] T017 [US2] Raster-Test in `test_loan_calculator.py` (Kommentar `# FR-010`), gleiches Raster wie T010. Für jede Jahreszeile *j* gilt `yearly[j-1].balance_cents == monthly[min(12*j, months) - 1].balance_cents`. Zinssumme und Tilgungssumme sind in beiden Plänen gleich.
- [ ] T018 [US2] Test in `test_loan_calculator.py` (Kommentar `# FR-011`): `main(["--bogus"])` löst `SystemExit` mit `code == 2` aus. `capsys.readouterr().out == ""`, `input` wird nicht aufgerufen (der gepatchte `input` wirft `AssertionError`).

### Implementation for User Story 2

- [ ] T019 [US2] In `parse_args` in `loan_calculator.py` die Option `parser.add_argument("--monthly", action="store_true", help="print the amortization schedule month by month")` ergänzen. In `main()` gilt dann `period_months, label = (1, "Month") if args.monthly else (12, "Year")`, beide Werte gehen an `amortization_schedule` und `format_schedule`. Danach sind T016 bis T018 grün.

**Checkpoint**: Beide User Stories funktionieren. Die Jahresausgabe ohne Option ist unverändert (T008 bleibt grün).

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Verfassungsprüfung und Abnahme

- [ ] T020 Stilprüfung gegen `.claude/rules/python-style.md` für `loan_calculator.py` und `test_loan_calculator.py`: Jede Funktion beginnt mit einem einzeiligen `#`-Kommentar, zwischen Top-Level-Funktionen stehen genau zwei Leerzeilen.
- [ ] T021 Importe in `loan_calculator.py` prüfen: nur `argparse` und `typing` (Standardbibliothek). `requirements.txt` ist unverändert.
- [ ] T022 Gesamte Suite mit `uv run --with pytest pytest` aus dem Repository-Root ausführen. Alle Tests müssen grün sein, auch `test_retirement_calculator.py`.
- [ ] T023 Die manuellen Prüfungen aus `specs/001-loan-amortization-schedule/quickstart.md` durchführen (Jahresplan, `--monthly`, `--bogus` mit `exit=2`).

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: T001 muss **vor jeder Änderung** an `loan_calculator.py` laufen, sonst ist die Referenz verfälscht. T002 hängt von T001 ab (gleiche Datei).
- **Foundational (Phase 2)**: hängt von Setup ab und blockiert beide User Stories.
- **US1 (Phase 3)**: hängt von Phase 2 ab.
- **US2 (Phase 4)**: hängt von Phase 2 **und US1** ab. Der Monatsplan nutzt `amortization_schedule`, `schedule_totals` und `format_schedule` aus T011 bis T014 mit `period_months = 1`, deshalb ist US2 nicht unabhängig von US1 umsetzbar.
- **Polish (Phase 5)**: hängt von allen gewünschten Stories ab.

### Within Each Phase

- Tests vor Implementierung. Tests müssen zuerst fehlschlagen.
- `test_loan_calculator.py`: T003 → T004 → T008 → T009 → T010 → T016 → T017 → T018 (gleiche Datei, sequenziell)
- `loan_calculator.py`: T005 → T006 → T007 → T011 → T012 → T013 → T014 → T015 → T019 (gleiche Datei, sequenziell)

### Parallel Opportunities

Da es nur zwei Dateien gibt, ist Parallelität nur **zwischen** Test- und Quelldatei möglich:

- T004 (Tests) ∥ T005 (Rechenfunktionen)
- T008 bis T010 (US1-Tests) ∥ T011 bis T014 (US1-Implementierung)
- T016 bis T018 (US2-Tests) ∥ T019 (US2-Implementierung), wobei T019 erst nach T015 startet

---

## Parallel Example: User Story 1

```bash
# Strang A – Tests (test_loan_calculator.py), nacheinander:
Task: "T008 Golden-Test Jahresplan 10000/5/2.5"
Task: "T009 Tests amortization_schedule jährlich"
Task: "T010 Raster-Test Summen/Restschuld"

# Strang B – Implementierung (loan_calculator.py), parallel zu Strang A, nacheinander:
Task: "T011 ScheduleRow / ScheduleTotals"
Task: "T012 amortization_schedule"
Task: "T013 schedule_totals"
Task: "T014 format_schedule"
# danach T015 (Einbindung in main), dann Tests ausführen
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Phase 1: Referenz sichern (T001), Testgerüst (T002)
2. Phase 2: Refactoring ohne Verhaltensänderung, Checkpoint „Ausgabe identisch“
3. Phase 3: Jahresplan
4. **STOP and VALIDATE**: `uv run --with pytest pytest` und Jahresplan-Beispiel aus quickstart.md
5. Kann bereits so ausgeliefert werden

### Incremental Delivery

1. Setup und Foundational: refaktorierte, verhaltensgleiche Basis
2. US1: Jahresplan (MVP)
3. US2: `--monthly` und Fehlerbehandlung unbekannter Optionen
4. Polish: Stil, Importe, Gesamtsuite, Quickstart

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Jede FR-ID kommt in mindestens einem Test-Kommentar vor (Zuordnung siehe quickstart.md)
- Nach jeder Phase committen
- Avoid: Änderungen an der Zusammenfassung, neue Abhängigkeiten, `print`/`input` außerhalb von `main()`
