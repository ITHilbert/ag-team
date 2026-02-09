# AG-Team Workflow

## Übersicht

1.  **PLANUNG** (`projekt/01_planung`)
    - Analyse, Architektur und Tasking.
    - Artefakte: `PLAN-*.md`, `TASK-*.md`.
    - Status: `GEPLANT`

2.  **ARBEIT** (`projekt/02_arbeit`)
    - Aktive Bearbeitung durch Worker.
    - Temporäre Dateien und Zwischenschritte.
    - Status: `IN ARBEIT`

4.  **ERGEBNIS** (`projekt/03_ergebnisse`)
    - Abgenommene, fertige Resultate.
    - Single Source of Truth für den Anwender.
    - Status: `FERTIG`

---

## Prozess

1.  **Diskussion & Idee**:
    - Anwender diskutiert mit Moderator.
    - Anwender gibt explizite Anweisung: "Gib das als Idee weiter".
    - Moderator leitet Idee an **Produktmanager** weiter.

2.  **Entscheidung & Planung (Produktmanager)**:
    - Produktmanager prüft Idee (Machbarkeit, Sinn).
    - Produktmanager erstellt/aktualisiert Specs in `01_planung` (Features).
    - Produktmanager beauftragt Systemarchitekt.

3.  **Architektur & Tasking (Systemarchitekt)**:
    - Architekt erstellt technischen Plan.
    - Architekt initiiert Worker.

4.  **Umsetzung (Worker)**:
    - Worker setzen Tasks in `02_arbeit` um.

5.  **Abnahme**:
    - Ergebnisse werden geprüft und landen in `03_ergebnisse`.
