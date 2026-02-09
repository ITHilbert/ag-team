# Struktur des Agenten-Systems
> **Hinweis**: Alle Pfade befinden sich relativ im Ordner `ag-team/`.

## Agenten
- agenten/
  - 00_agenten.md (Globale Regeln)
  - 01_administrator.md
  - 02_moderator.md
  - 02_Produktmanager.md
  - 03_Systemarchitekt.md
  - 04_Frontend-Engineer.md
  - 05_worker.md (Generic)
  - 05_Backend-Engineer.md
  - 05_worker_db.md
  - 06_QA-Engineer.md
  
## Tools & Scripts
- start_aider.bat (Nutzt D:\Aider)
- start_orchestrator.bat (Nutzt D:\Aider)
- python/
  - agent_orchestrator.py

## Initialisierung
- 01_init_agenten.md
- README.md (Einführung & Setup)

## User Projekt
- projekt/
  - 00_inbox/      # Eingang für neue Anforderungen
  - 01_planung/    # Tasks und Pläne
  - 02_arbeit/     # Aktive Arbeitsverzeichnisse
  - 03_ergebnisse/ # Fertige Resultate (Single Source of Truth)
  - 04_archiv/     # Abgeschlossene Tasks und Logs
  - WORKFLOW.md    # Prozessdefinition
