# Feature Specification: Tilgungsplan im Kreditrechner

**Feature Branch**: `sdd/10-speckit`

**Created**: 2026-10-08

**Status**: Draft

**Input**: User description: "Der Kreditrechner (loan_calculator.py) soll nach der bisherigen
Zusammenfassung einen Tilgungsplan ausgeben: je Laufzeitjahr die gezahlten Zinsen, die Tilgung und
die Restschuld am Jahresende. Mit der Option --monthly erscheint der Plan Monat für Monat. Die
Summen müssen zur Zusammenfassung passen, die letzte Restschuld ist 0.00, ein angebrochenes letztes
Jahr enthält nur die restlichen Monate. Die bisherige Zusammenfassung bleibt unverändert."

## Clarifications

### Session 2026-10-08

- Q: Soll unter dem Tilgungsplan eine sichtbare Summenzeile stehen, oder genügt es, dass die Zeilen
  rechnerisch zur Zusammenfassung passen? → A: Sichtbare Summenzeile `Total` mit drei Werten:
  Zinssumme, Tilgungssumme und Gesamtzahlung (= „Total repaid“).
- Q: In welcher Sprache sollen die Spaltenüberschriften und das Wort „Total“ im Tilgungsplan
  stehen? → A: Englisch (`Year`/`Month`, `Interest`, `Principal`, `Balance`, `Total`), passend
  zur bestehenden englischen Ausgabe.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Jährlicher Tilgungsplan (Priority: P1)

Eine Person rechnet einen Kredit durch und sieht nach der gewohnten Zusammenfassung (Monatsrate,
Gesamtrückzahlung, Gesamtzinsen) zusätzlich, wie sich Zinsen, Tilgung und Restschuld über die
Laufzeitjahre entwickeln. So erkennt sie z. B., wie viel Restschuld nach zwei Jahren noch offen ist
und dass in den ersten Jahren der Zinsanteil am höchsten ist.

**Why this priority**: Das ist der Kern des Features. Ohne den Jahresplan gibt es keinen Mehrwert;
er funktioniert ohne jede neue Option.

**Independent Test**: Kreditrechner ohne Option starten, Betrag, Zinssatz und Laufzeit eingeben
und prüfen, dass die Zusammenfassung unverändert ist und darauf ein Jahresplan folgt, dessen
Summen zur Zusammenfassung passen.

**Acceptance Scenarios**:

1. **Given** Kreditbetrag 10000, Zinssatz 5 %, Laufzeit 2.5 Jahre, **When** der Kreditrechner
   ohne Option läuft, **Then** erscheint zuerst die bisherige Zusammenfassung zeichengleich und
   danach ein Plan mit genau 3 Jahreszeilen, wobei Jahr 3 nur die Monate 25–30 umfasst
   (exakte Ausgabe siehe „Ausgabeformat“).
2. **Given** Kreditbetrag 10000, Zinssatz 5 %, Laufzeit 2 Jahre, **When** der Kreditrechner
   läuft, **Then** zeigt der Plan genau 2 Jahreszeilen und die Restschuld der letzten Zeile ist
   `0.00`.
3. **Given** ein beliebiger Kredit, **When** der Plan ausgegeben wird, **Then** ist die
   Zinssumme gleich dem Wert „Total interest“ der Zusammenfassung, die Tilgungssumme gleich
   dem Kreditbetrag und die Gesamtzahlung gleich „Total repaid“, jeweils auf den Cent.

---

### User Story 2 - Monatlicher Tilgungsplan mit `--monthly` (Priority: P2)

Wer es genauer wissen will, startet den Kreditrechner mit der Option `--monthly` und bekommt
denselben Plan Monat für Monat statt Jahr für Jahr.

**Why this priority**: Nützliche Detailansicht, baut aber auf derselben Rechnung wie der
Jahresplan auf und ist ohne ihn verzichtbar.

**Independent Test**: Kreditrechner mit `--monthly` starten und prüfen, dass der Plan eine Zeile
pro Monat enthält, die Summen zur Zusammenfassung passen und die letzte Restschuld `0.00` ist.

**Acceptance Scenarios**:

1. **Given** Kreditbetrag 10000, Zinssatz 5 %, Laufzeit 2.5 Jahre, **When** der Kreditrechner
   mit `--monthly` läuft, **Then** zeigt der Plan genau 30 Monatszeilen (1 bis 30) und keine
   Jahreszeilen.
2. **Given** derselbe Kredit, **When** man die Restschuld von Monat 12 im Monatsplan mit der
   Restschuld von Jahr 1 im Jahresplan vergleicht, **Then** sind beide Werte gleich (`6149.02`).
3. **Given** der Kreditrechner wird mit `--monthly` gestartet, **When** die Zusammenfassung
   ausgegeben wird, **Then** ist sie zeichengleich mit der Ausgabe ohne Option.

---

### Edge Cases

- **Zinssatz 0 %**: Alle Zinswerte sind `0.00`, die Tilgung verteilt sich gleichmäßig, die letzte
  Restschuld ist `0.00`.
- **Laufzeit kürzer als ein Jahr** (z. B. 0.5 Jahre = 6 Monate): Der Jahresplan hat genau eine
  Zeile, die nur diese 6 Monate umfasst.
- **Laufzeit ganzzahlig in Jahren**: Kein angebrochenes Jahr; die letzte Jahreszeile umfasst
  volle 12 Monate.
- **Laufzeit ergibt keine ganze Monatszahl** (z. B. 1.55 Jahre): Die Monatszahl wird wie bisher
  in der Zusammenfassung abgerundet (hier 18 Monate); der Plan verwendet dieselbe Monatszahl.
- **Rundung**: Durch Rundung auf Cent darf nie `-0.00` erscheinen; die letzte Restschuld ist
  immer genau `0.00`.
- **Unbekannte Kommandozeilenoption**: Das Programm bricht vor der ersten Eingabeaufforderung mit
  einem Hinweis zur korrekten Verwendung und einem Fehler-Exit-Code ab.
- **Ungültige Eingaben** (Laufzeit unter einem Monat, nicht-numerische Werte): Verhalten bleibt
  wie bisher; dieses Feature ändert daran nichts.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Die bisherige Ausgabe (Titelzeile, Eingabeaufforderungen und die drei Zeilen der
  Zusammenfassung) MUSS zeichengleich erhalten bleiben – mit und ohne `--monthly`.
- **FR-002**: Unmittelbar nach der Zusammenfassung MUSS ein Tilgungsplan ausgegeben werden. Diese
  Erweiterung der Gesamtausgabe ist durch diese Spec ausdrücklich gefordert (Verfassung, Prinzip IV).
- **FR-003**: Ohne Option MUSS der Plan eine Zeile je Laufzeitjahr enthalten, nummeriert ab 1,
  mit den in diesem Jahr gezahlten Zinsen, der in diesem Jahr geleisteten Tilgung und der
  Restschuld am Ende dieses Jahres.
- **FR-004**: Ist die Laufzeit kein Vielfaches von 12 Monaten, MUSS die letzte Jahreszeile nur
  die verbleibenden Monate umfassen.
- **FR-005**: Mit der Option `--monthly` MUSS der Plan statt der Jahreszeilen eine Zeile je Monat
  enthalten, nummeriert ab 1, mit Zinsen, Tilgung und Restschuld am Monatsende.
- **FR-006**: Unter den Planzeilen MUSS eine Summenzeile `Total` mit drei Werten stehen:
  Zinssumme, Tilgungssumme und Gesamtzahlung. Auf den Cent MUSS gelten: Zinssumme = „Total
  interest“, Tilgungssumme = Kreditbetrag, Gesamtzahlung = „Total repaid“ der Zusammenfassung
  = Zinssumme + Tilgungssumme.
- **FR-007**: Die angezeigten (auf Cent gerundeten) Zeilenwerte MÜSSEN sich exakt zu den
  angezeigten Summen addieren; es darf keine Rundungsdifferenz geben.
- **FR-008**: Für jede Zeile MUSS gelten: angezeigte Restschuld = angezeigte Restschuld der
  Vorzeile (bzw. Kreditbetrag bei der ersten Zeile) − angezeigte Tilgung dieser Zeile.
- **FR-009**: Die Restschuld der letzten Zeile MUSS `0.00` sein; `-0.00` darf nirgends erscheinen.
- **FR-010**: Jahres- und Monatsplan MÜSSEN konsistent sein: Die Restschuld am Ende von Jahr *j*
  ist gleich der Restschuld am Ende von Monat 12·*j* (bzw. des letzten Monats).
- **FR-011**: Eine unbekannte Kommandozeilenoption MUSS vor der ersten Eingabeaufforderung zu
  einem Verwendungshinweis und einem Exit-Code ungleich 0 führen.
- **FR-012**: Der Plan MUSS exakt dem unten beschriebenen Ausgabeformat folgen.
- **FR-013**: Spaltenüberschriften und Summenzeile MÜSSEN englisch sein (`Year` bzw. `Month`,
  `Interest`, `Principal`, `Balance`, `Total`), passend zur bestehenden Ausgabe.

### Ausgabeformat

Nach der letzten Zeile der Zusammenfassung folgt eine Leerzeile, dann der Plan. Spaltenbreiten:
Periodenspalte 5 Zeichen, jede Betragsspalte 12 Zeichen; Beträge rechtsbündig mit zwei
Nachkommastellen, ohne Tausendertrennzeichen (wie in der Zusammenfassung). Periodennummern sind
rechtsbündig, das Wort `Total` steht linksbündig. In der Summenzeile steht in der dritten
Betragsspalte (unter `Balance`) statt einer Restschuld die Gesamtzahlung.

Beispiel Jahresplan (10000, 5 %, 2.5 Jahre) – vollständige Ausgabe nach den Eingaben:

```text

Monthly payment:      355.29
Total repaid:       10658.81
Total interest:       658.81

 Year    Interest   Principal     Balance
    1      412.54     3850.98     6149.02
    2      215.52     4048.00     2101.02
    3       30.75     2101.02        0.00
Total      658.81    10000.00    10658.81
```

Beispiel Monatsplan (derselbe Kredit, `--monthly`), Auszug:

```text

Month    Interest   Principal     Balance
    1       41.67      313.63     9686.37
    2       40.36      314.93     9371.44
  ...
   12       26.99      328.30     6149.02
  ...
   29        2.95      352.35      353.82
   30        1.47      353.82        0.00
Total      658.81    10000.00    10658.81
```

### Key Entities

- **Kredit**: Kreditbetrag, Jahreszinssatz in Prozent, Laufzeit in Monaten (aus der Laufzeit in
  Jahren abgeleitet, wie bisher abgerundet), konstante Monatsrate.
- **Planzeile**: Periodennummer (Jahr oder Monat), in der Periode gezahlte Zinsen, in der Periode
  geleistete Tilgung, Restschuld am Periodenende.
- **Summenzeile**: Summe der Zinsen, Summe der Tilgung und Gesamtzahlung (Zinsen + Tilgung) über
  alle Planzeilen.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Bei 100 % der getesteten Kredite (inkl. 0 % Zins, Laufzeiten < 1 Jahr, ganzzahlig
  und angebrochen) ist die Zusammenfassung zeichengleich zur bisherigen Ausgabe.
- **SC-002**: Bei 100 % der getesteten Kredite stimmen Zinssumme, Tilgungssumme und Gesamtzahlung
  des Plans auf den Cent mit „Total interest“, dem Kreditbetrag bzw. „Total repaid“ überein, und
  die letzte Restschuld ist `0.00`.
- **SC-003**: Bei einer Laufzeit von *n* Monaten enthält der Jahresplan genau ⌈*n*/12⌉ Zeilen
  und der Monatsplan genau *n* Zeilen.
- **SC-004**: Eine Person kann die Restschuld zu jedem Jahresende direkt aus dem Plan ablesen,
  ohne selbst zu rechnen.

## Assumptions

- „Laufzeitjahr“ meint Jahre ab Kreditbeginn (Monate 1–12, 13–24, …), nicht Kalenderjahre.
- Die Eingabe von Betrag, Zinssatz und Laufzeit bleibt interaktiv wie bisher; `--monthly` ist die
  einzige neue Option und wird beim Programmstart übergeben.
- Rechnerisch wird mit voller Genauigkeit gearbeitet und erst für die Anzeige auf Cent gerundet;
  Rundungsdifferenzen werden so verteilt, dass FR-007 bis FR-009 gelten. Dass in einer einzelnen
  Monatszeile Zinsen + Tilgung um einen Cent von der angezeigten Monatsrate abweichen können,
  ist zulässig.
- Bei sehr großen Beträgen (mehr als 12 Zeichen) darf die Spaltenausrichtung verrutschen;
  die Werte selbst bleiben korrekt.
- Validierung ungültiger Eingaben ist nicht Teil dieses Features.
