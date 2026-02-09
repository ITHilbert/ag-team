# AG-Team Installationsanleitung (INSTALL.md)

Dieses System nutzt eine Kombination aus lokalen KI-Modellen (Ollama), Python-Scripting und dem Coding-Tool Aider. Hier sind die Schritte, um es auf einem neuen Windows-System einzurichten.

## 1. Voraussetzungen (Software)

Folgende Tools müssen installiert sein (bitte Standard-Pfade nutzen oder PATH-Variable anpassen):

### Git
- **Zweck**: Versionskontrolle.
- **Download**: [git-scm.com](https://git-scm.com/downloads)
- **Check**: `git --version` im Terminal.

### Python
- **Zweck**: Ausführung des Orchestrator-Skripts (`agent_orchestrator.py`).
- **Download**: [python.org](https://www.python.org/downloads/) (Version 3.10 oder neuer empfohlen).
- **Wichtig**: Bei Installation "Add Python to PATH" anhaken!
- **Check**: `python --version` im Terminal.

### Ollama
- **Zweck**: Lokaler KI-Server für die Agenten (Mistral).
- **Download**: [ollama.com](https://ollama.com/)
- **Check**: `ollama --version` im Terminal.
- **Model Pull**: Führe einmalig `ollama pull mistral` aus.

### Aider (Optional/Empfohlen für Coding)
- **Zweck**: Das Tool, das den Code tatsächlich schreibt.
- **Installation**:
  ```bash
  pip install aider-chat
  ```
- **Check**: `aider --version`.

---

## 2. Projekt-Setup

### Repository klonen
```bash
git clone https://github.com/ITHilbert/ag-team.git
cd ag-team
```

### Python-Abhängigkeiten installieren
Das Projekt benötigt spezielle Python-Pakete (z.B. den Ollama-Client).
```bash
cd python
pip install -r requirements.txt
```

---

## 3. Systemstart

1.  **Ollama starten**: Stelle sicher, dass Ollama im Hintergrund läuft (Taskleiste).
2.  **Orchestrator starten**:
    - Navigiere ins Hauptverzeichnis `ag-team`.
    - Führe `start_orchestrator.bat` aus (oder `python python/agent_orchestrator.py`).
3.  **Moderator-Chat**:
    - Das Skript öffnet ein Menü.
    - Wähle den `Moderator` (oder starte direkt die Interaktion).

---

## Fehlersuche

- **"Module not found: ollama"**: Du hast `pip install -r requirements.txt` vergessen.
- **"Connection refused"**: Ollama läuft nicht. Starte die Ollama-App.
- **Aider öffnet sich nicht**: Prüfe den Pfad in `start_aider.bat`. Ggf. musst du den Pfad zu deiner Aider-Installation anpassen.
