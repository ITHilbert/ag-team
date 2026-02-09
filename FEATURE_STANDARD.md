# Feature-Dateistandard

Diese Datei beschreibt den verbindlichen Standard für die Erstellung, Dokumentation und Freigabe von Features in diesem Repository. Ziel ist es, für lokale Modelle und Aider eine verlässliche Kontext-Basis zu schaffen.

## Ordnerstruktur

Alle Features befinden sich im Ordner `features/`.

### Namenskonvention
Jedes Feature erhält einen eigenen Unterordner nach folgendem Schema:
`features/<YYYY-MM-DD>_<kurzer-slug>/`

Beispiel:
`features/2026-02-09_login-mit-ollama/`

### Dateistruktur je Feature
In jedem Feature-Ordner müssen die folgenden Dateien in der angegebenen Reihenfolge erstellt und bearbeitet werden. Templates befinden sich unter `templates/features/`.

1.  `01_intake.md` (Initialisierung)
2.  `02_spec.md` (Anforderung)
3.  `03_architektur.md` (Design)
4.  `04_qa.md` (Qualitätssicherung)
5.  `05_security.md` (Sicherheit)
6.  `06_release.md` (Release-Vorbereitung)
7.  `07_freigabe.md` (Abschluss)

---

## Phasen & Gates

### 1. Intake
*   **Datei**: `01_intake.md`
*   **Verantwortlich**: Moderator
*   **Inhalt**: Ziel, Kontext, Nicht-Ziele, Risiken.
*   **Gate / Done**: Ziel ist klar definiert, Status ist "READY".

### 2. Spezifikation
*   **Datei**: `02_spec.md`
*   **Verantwortlich**: Produktmanager
*   **Inhalt**: User Stories, Akzeptanzkriterien, Inputs/Outputs.
*   **Gate / Done**: Akzeptanzkriterien sind testbar, Status ist "READY".

### 3. Architektur
*   **Datei**: `03_architektur.md`
*   **Verantwortlich**: Architekt
*   **Inhalt**: Entscheidungen, Schnittstellen, Datenmodell.
*   **Gate / Done**: Technische Machbarkeit bestätigt, Status ist "READY".

### 4. Implementierung & QA
*   **Datei**: `04_qa.md`
*   **Verantwortlich**: QA / Implementierung
*   **Inhalt**: Teststrategie, Testfälle, Automatisierung, Findings.
*   **Gate / Done**: Alle Tests erfolgreich (PASS), keine kritischen Bugs.

### 5. Security (Optional)
*   **Datei**: `05_security.md`
*   **Verantwortlich**: Security / DevOps
*   **Inhalt**: Bedrohungsmodell, Secrets, Maßnahmen.
*   **Gate / Done**: Sicherheitsstatus "PASS" oder "NOT REQUIRED".

### 6. Release & Freigabe
*   **Dateien**: `06_release.md`, `07_freigabe.md`
*   **Verantwortlich**: DevOps / Moderator
*   **Inhalt**: Build-Steps, Checkliste, Finale Entscheidung.
*   **Gate / Done**: Release ist "READY", Freigabe ist "APPROVED".

---

## Aider-Workflow

Für die Arbeit mit Aider sollten immer die relevanten Kontext-Dateien geladen werden.

**Beispiel-Prompt für Aider:**
"Implementiere User Story 1 aus `features/2024-03-20_mein-feature/02_spec.md`. Beachte die Architekturvorgaben in `03_architektur.md`."

**Regeln für Aider:**
*   Kleine, atomare Commits.
*   Jede Änderung muss durch einen Test verifiziert werden.
*   Nur Dateien bearbeiten, die für das Feature relevant sind.
