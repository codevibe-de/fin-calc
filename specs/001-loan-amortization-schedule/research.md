# Research: Tilgungsplan im Kreditrechner

Im Technical Context waren keine Punkte als NEEDS CLARIFICATION offen. Die Entscheidungen unten
betreffen die zwei technisch heiklen Stellen: Rundung und CLI-Anbindung.

## R1 – Rundung: Wie bleiben Zeilen, Summen und Zusammenfassung auf den Cent konsistent?

**Decision**: Gerechnet wird mit Float in voller Genauigkeit. Zusätzlich werden pro Monat die
**kumulierten** Zinsen und die **kumulierte** Tilgung mitgeführt. An jedem Periodenende
(Jahresende, letzter Monat bzw. jeder Monat) werden diese kumulierten Werte auf ganze Cent
(`int`) gerundet. Die Zeilenwerte sind die Differenzen aufeinanderfolgender kumulierter
Cent-Werte. In der letzten Periode werden die kumulierten Werte festgesetzt:

- kumulierte Zinsen := `Cent(Rate · n − Kreditbetrag)`, derselbe Ausdruck wie „Total interest“
- kumulierte Tilgung := `Cent(Kreditbetrag)`
- Restschuld je Zeile := `Cent(Kreditbetrag) − kumulierte Tilgung`

`Cent(v)` rundet über dieselbe `.2f`-Formatierung wie die Zusammenfassung:
`round(float(f"{v:.2f}") * 100)`. So zeigen Plan und Zusammenfassung garantiert dieselben Ziffern.

**Rationale**:
- FR-007 (keine Rundungsdifferenz): Die Zeilenwerte sind Differenzen einer Teleskopsumme,
  ihre Summe ist exakt der letzte kumulierte Wert.
- FR-008 (Restschuld-Kette) und FR-009 (letzte Restschuld `0.00`) gelten per Konstruktion.
  Da Cent-Werte `int` sind, kann `-0.00` nicht entstehen.
- FR-006: Die Zinssumme ist exakt „Total interest“. Für Beträge mit höchstens 2 Nachkommastellen
  gilt außerdem Zinssumme + Tilgungssumme = „Total repaid“.
- FR-010: Jahres- und Monatsplan nutzen dieselbe kumulierte Reihe. Die Restschuld nach Jahr *j*
  ist also identisch mit der nach Monat 12·*j*.
- Die Werte im Beispiel der Spec werden exakt reproduziert (Jahr 2: `4048.00` / `2101.02`).
- Der Prototyp wurde über 588 Kombinationen geprüft (7 Beträge × 7 Zinssätze inkl. 0 % ×
  6 Laufzeiten inkl. 0.5, 1.55, 2.5 Jahre × jährlich/monatlich). Alle Invarianten hielten, und es
  gab keine negativen Werte.

**Alternatives considered**:
- *Jede Monatszeile einzeln runden (Bankpraxis), letzte Rate anpassen*: Die Zinssumme weicht dann
  um einige Cent von „Total interest“ ab, die unverändert bleiben muss. Verletzt FR-006.
- *Kumulierte Zahlungen statt kumulierter Tilgung runden* (Tilgung = Zahlung − Zinsen): Die
  Invarianten hielten zwar, aber das Spec-Beispiel ergab abweichende Werte
  (Jahr 2: `4048.01` / `2101.01`). Verworfen, weil die Spec das Beispiel festlegt.
- *`decimal.Decimal` durchgängig*: Ändert die Rechenbasis gegenüber der Zusammenfassung (Float)
  und riskiert damit Abweichungen in genau den Werten, die zeichengleich bleiben müssen. Für den
  Zweck unnötig aufwendig.

**Known limit**: Bei Beträgen mit mehr als 2 Nachkommastellen (z. B. `1000.005`) ist die
Tilgungssumme der auf Cent gerundete Betrag. Die Gleichung Zinsen + Tilgung = „Total repaid“ kann
dann um 0.01 abweichen, weil die Zusammenfassung beide Werte unabhängig rundet. Die Spec schließt
Eingabevalidierung aus, die Abweichung wird hingenommen.

## R2 – CLI: Wie wird `--monthly` eingeführt, ohne die bestehende Ausgabe zu verändern?

**Decision**: `argparse.ArgumentParser` mit genau einer Option `--monthly` (`store_true`).
`main(argv=None)` ruft `parse_args(argv)` **vor** der Titelzeile auf. Die Eingaben bleiben
interaktiv per `input()` mit unveränderten Prompts.

**Rationale**: argparse ist Standardbibliothek (Prinzip I). Bei einer unbekannten Option schreibt
argparse Usage und Fehler auf stderr und beendet mit Exit-Code 2, noch bevor etwas auf stdout
erscheint (FR-011). Durch den Parameter `argv` lässt sich `main` in Tests ohne `sys.argv`-Patching
aufrufen.

**Alternatives considered**:
- *`sys.argv` von Hand prüfen*: weniger Code, aber ohne Usage-Text und ohne `--help`. Fehler
  müsste man selbst behandeln.
- *Interaktive Frage „monthly? (y/n)“*: Verändert die Eingabefolge, und die Spec fordert eine
  Option.

## R3 – Testansatz für zeichengleiche Ausgabe

**Decision**: Golden-Output-Tests rufen `main([...])` auf, setzen `input` per `monkeypatch`
(Folge von Antworten) und vergleichen die stdout-Ausgabe aus `capsys` **vollständig** mit dem
erwarteten Text. Die Rechen-Invarianten werden zusätzlich als parametrisierte Tests über ein
Raster von Kreditfällen geprüft.

**Rationale**: Prinzip IV verlangt den exakten Nachweis. Die Raster-Tests sichern FR-006 bis
FR-010 über mehr als nur das Spec-Beispiel ab.

**Alternatives considered**: Subprozess-Aufruf des Skripts mit stdin-Pipe. Das ist realistischer,
aber langsamer und schwerer zu debuggen. Nur für FR-011 (Exit-Code) sinnvoll, dort genügt
`pytest.raises(SystemExit)`.
