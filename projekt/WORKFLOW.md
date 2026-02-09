# AG-Team Workflow

## Übersicht

1.  **INBOX** (`projekt/00_inbox`)
    - Eingang für neue Anforderungen (`REQ-*.md`).
    - Status: `NEU`

2.  **PLANUNG** (`projekt/01_planung`)
    - Analyse, Architektur und Tasking.
    - Artefakte: `PLAN-*.md`, `TASK-*.md`.
    - Status: `GEPLANT`

3.  **ARBEIT** (`projekt/02_arbeit`)
    - Aktive Bearbeitung durch Worker.
    - Temporäre Dateien und Zwischenschritte.
    - Status: `IN ARBEIT`

4.  **ERGEBNIS** (`projekt/03_ergebnisse`)
    - Abgenommene, fertige Resultate.
    - Single Source of Truth für den Anwender.
    - Status: `FERTIG`

---

## Prozess

1.  **Anwender** legt `REQ-Titel.md` in `00_inbox` ab (nutze Template).
2.  **Moderator** prüft Inbox und weist Task an Architekt/Protokollagent.
3.  **Architekt** erstellt Plan in `01_planung`.
4.  **Worker** führt Task aus in `02_arbeit`.
5.  **Review** (durch Architekt/Anwender) verschiebt Ergebnis nach `03_ergebnisse`.
6.  **Aufräumen**: Quelldateien nach `04_archiv`.
