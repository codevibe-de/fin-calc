<!--
Sync Impact Report
==================
Version change: (unbefüllte Vorlage) → 1.0.0
Begründung: Erstfassung – alle Platzhalter erstmals mit Projektinhalten befüllt.

Geänderte Prinzipien (Vorlagen-Platzhalter → neuer Titel):
  - [PRINCIPLE_1_NAME] → I. Nur Python-Standardbibliothek
  - [PRINCIPLE_2_NAME] → II. Rechnen getrennt von Ein-/Ausgabe
  - [PRINCIPLE_3_NAME] → III. Jede Anforderung hat einen pytest-Test
  - [PRINCIPLE_4_NAME] → IV. Zeichengleiche CLI-Ausgaben
  - [PRINCIPLE_5_NAME] → V. Verbindlicher Code-Stil

Hinzugefügte Abschnitte:
  - Technische Rahmenbedingungen (aus [SECTION_2_NAME])
  - Entwicklungsablauf & Qualitätstore (aus [SECTION_3_NAME])
  - Governance (befüllt)

Entfernte Abschnitte: keine

Bekannte Abweichungen im Bestand (kein TODO der Verfassung, nur Hinweis):
  - loan_calculator.py: calculate_monthly_payment rechnet und druckt in einer Funktion
    (verstößt gegen Prinzip II) – wird bei der nächsten Änderung dieser Datei bereinigt.

Offene TODOs: keine
-->

# fin-calc Constitution

## Core Principles

### I. Nur Python-Standardbibliothek

- Produktivcode DARF ausschließlich Module der Python-Standardbibliothek importieren.
- Es DÜRFEN keine neuen Laufzeitabhängigkeiten eingeführt werden; `requirements.txt` bleibt
  frei von Laufzeitpaketen.
- Einzige Ausnahme ist `pytest` als reines Testwerkzeug; es wird nicht installiert, sondern
  bei Bedarf über `uv run --with pytest` bereitgestellt.

**Begründung**: fin-calc soll auf jeder Python-Installation ohne Setup laufen. Jede
Abhängigkeit kostet Wartung und Vertrauen, ohne für einfache Finanzrechnungen nötig zu sein.

### II. Rechnen getrennt von Ein-/Ausgabe

- Berechnungen MÜSSEN als reine Funktionen umgesetzt sein: Ergebnis hängt nur von den
  Argumenten ab, Rückgabe per `return`, keine Seiteneffekte.
- Rechenfunktionen DÜRFEN weder `print`, `input`, Dateizugriffe noch `argparse` verwenden.
- Ein-/Ausgabe (Argumente parsen, Eingaben lesen, Ergebnisse formatieren und ausgeben)
  liegt in eigenen Funktionen bzw. in `main()` und ruft die Rechenfunktionen nur auf.
- Bestehender Code, der dagegen verstößt, MUSS bereinigt werden, sobald er geändert wird.

**Begründung**: Reine Funktionen sind direkt testbar und wiederverwendbar; die Trennung
verhindert, dass Formatierungsänderungen die Rechenlogik berühren und umgekehrt.

### III. Jede Anforderung hat einen pytest-Test

- Jede funktionale Anforderung einer Spec MUSS durch mindestens einen pytest-Test abgedeckt
  sein, der auf die Anforderung rückführbar ist (z. B. per Kommentar mit Anforderungs-ID).
- Die gesamte Testsuite MUSS mit `uv run --with pytest pytest` aus dem Repository-Root
  ohne weitere Vorbereitung laufen und grün sein.
- Eine Änderung gilt erst als fertig, wenn die Suite vollständig besteht.

**Begründung**: Finanzrechnungen sind fehleranfällig in Randfällen (Zins 0, Laufzeiten,
Rundung). Nur ein Test pro Anforderung macht Korrektheit nachweisbar und Regressionen sichtbar.

### IV. Zeichengleiche CLI-Ausgaben

- Bestehende CLI-Ausgaben (Texte, Beschriftungen, Zahlenformate, Ausrichtung, Leerzeichen,
  Leerzeilen) MÜSSEN zeichengleich erhalten bleiben.
- Eine Ausgabe DARF nur geändert werden, wenn eine Spec diese Änderung ausdrücklich fordert;
  die Spec beschreibt dann die neue Ausgabe exakt.
- Für jede Ausgabe, die eine Änderung berührt, SOLL ein Test die exakte Ausgabe prüfen
  (z. B. über `capsys`), damit unbeabsichtigte Abweichungen auffallen.

**Begründung**: Nutzer und Skripte verlassen sich auf die bestehende Ausgabe. Schon ein
verschobenes Leerzeichen kann nachgelagerte Auswertungen oder Gewohnheiten brechen.

### V. Verbindlicher Code-Stil

- Jeder Python-Code MUSS den Regeln in `.claude/rules/python-style.md` folgen.
- Diese Datei ist die einzige Quelle der Stilregeln; die Verfassung dupliziert sie nicht.
  Änderungen an den Stilregeln erfolgen dort.

**Begründung**: Ein einheitlicher, an einer Stelle definierter Stil hält den Code lesbar und
macht Reviews schnell und eindeutig.

## Technische Rahmenbedingungen

- Sprache: Python 3 (Standardbibliothek). Python-Werkzeuge werden über `uv` ausgeführt,
  nie über `pip install`.
- Form: eigenständige Kommandozeilenprogramme (z. B. `loan_calculator.py`,
  `retirement_calculator.py`) mit je einer `main()`-Funktion als Einstiegspunkt.
- Tests liegen als `test_*.py` im Repository und werden von pytest automatisch gefunden.

## Entwicklungsablauf & Qualitätstore

- Neue Funktionen und Änderungen durchlaufen den Spec-Kit-Ablauf (Spec → Plan → Tasks →
  Umsetzung); der Plan MUSS einen „Constitution Check“ gegen die Prinzipien I–V enthalten.
- Vor dem Abschluss einer Änderung MÜSSEN folgende Tore bestanden sein:
  1. Keine neuen Nicht-Standardbibliotheks-Importe im Produktivcode (I).
  2. Neue oder geänderte Rechenlogik liegt in reinen Funktionen (II).
  3. Jede Anforderung der Spec ist einem Test zugeordnet; `uv run --with pytest pytest`
     ist grün (III).
  4. CLI-Ausgaben sind unverändert oder die Änderung ist in der Spec ausdrücklich gefordert (IV).
  5. Code entspricht `.claude/rules/python-style.md` (V).

## Governance

- Diese Verfassung hat Vorrang vor allen anderen Praktiken im Projekt. Konflikte mit Specs,
  Plänen oder Tasks werden zugunsten der Verfassung aufgelöst.
- Änderungen erfolgen ausschließlich über `/speckit-constitution`, werden mit Begründung
  dokumentiert und als eigener Commit festgehalten.
- Versionierung nach Semantic Versioning:
  - MAJOR: Prinzip entfernt oder inhaltlich unvereinbar umdefiniert.
  - MINOR: neues Prinzip oder neuer Abschnitt bzw. wesentlich erweiterte Vorgaben.
  - PATCH: Klarstellungen, Formulierungen, Tippfehler.
- Jedes Review und jeder `/speckit-plan`-Lauf prüft die Einhaltung. Abweichungen sind nur
  zulässig, wenn sie im Plan unter „Complexity Tracking“ begründet und freigegeben sind.

**Version**: 1.0.0 | **Ratified**: 2026-10-08 | **Last Amended**: 2026-10-08
