# AG-Team: AI-Agenten Orchestrator - Installationsanleitung

Dieses System orchestriert spezialisierte AI-Agenten (Produktmanager, Architekt, Frontend-Engineer) zur automatisierten Softwareentwicklung. Es nutzt lokale LLMs via Ollama.

---

## 1. Hardware-Anforderungen

Die Wahl des KI-Modells hängt stark von Ihrer Hardware ab:

| Modell | VRAM/RAM Bedarf | Empfehlung | Status |
| :--- | :--- | :--- | :--- |
| **`llama3.1:latest` (8b)** | ~6 GB | ✅ **Standard** | **Empfohlen.** Stabil, schnell, gut für Logik & Code. |
| `mixtral:latest` (8x7b) | ~26 GB | ⚠️ High-End | Gut für komplexe Aufgaben, benötigt viel RAM. |
| `llama3.1:70b` | ~42 GB | ❌ **Nicht empfohlen** | Führt auf den meisten Systemen zu Abstürzen (CUDA OOM). |
| `qwen2.5-coder` | ~5 GB | ❌ **Nicht empfohlen** | Neigt zu Endlosschleifen und destruktivem Code-Verhalten. |

---

## 2. Software-Voraussetzungen

Stellen Sie sicher, dass folgende Tools installiert sind:

### A. Ollama (KI-Server)
*   **Download:** [ollama.com](https://ollama.com)
*   **Wichtig:** Wenn Sie Modelle auf Laufwerk D: speichern wollen (z.B. `D:\Ollama\Models`), setzen Sie eine **System-Umgebungsvariable**:
    *   Name: `OLLAMA_MODELS`
    *   Wert: `D:\Ollama\Models`
*   **Test:** Öffnen Sie ein Terminal und tippen Sie `ollama --version`.

### B. Python (Laufzeitumgebung)
*   **Version:** 3.12 oder neuer.
*   **Download:** [python.org](https://www.python.org/downloads/)
*   **Wichtig:** Haken bei "Add Python to PATH" während der Installation setzen!

### C. Git (Versionsverwaltung)
*   **Download:** [git-scm.com](https://git-scm.com/downloads)

---

## 3. Installation & Einrichtung

### Schritt 1: Repository klonen
```bash
cd d:\Projekte\Test
git clone https://github.com/ITHilbert/ag-team.git
cd ag-team
```

### Schritt 2: Abhängigkeiten installieren
```bash
pip install -r python/requirements.txt
pip install aider-chat  # Optional, falls Aider genutzt wird
```

### Schritt 3: Modelle herunterladen
Laden Sie das stabile Standard-Modell:
```bash
ollama pull llama3.1:latest
```

### Schritt 4: Konfiguration (.env)
Erstellen Sie eine Datei namens `.env` im Ordner `ag-team/` mit folgendem Inhalt:
```ini
PROJECT_ROOT=d:\Projekte\Test
OLLAMA_MODEL=llama3.1:latest
```
*Anpassung:* Ändern Sie `PROJECT_ROOT` auf Ihren absoluten Projektpfad.

---

## 4. System Starten

1.  Stellen Sie sicher, dass **Ollama läuft** (Icon im Tray).
2.  Starten Sie den Orchestrator:
    *   Doppelklick auf **`start_orchestrator.bat`**
    *   *Oder via Terminal:* `python python/agent_orchestrator.py`

---

## 5. Troubleshooting

*   **Fehler: `CUDA error` / Absturz beim Laden:**
    *   Das gewählte Modell ist zu groß für Ihre Grafikkarte.
    *   Lösung: Wechseln Sie in der `.env` Datei auf `OLLAMA_MODEL=llama3.1:latest`.

*   **Agenten hängen in Schleifen ("Gib mir Anweisungen..."):**
    *   Das Modell (z.B. Qwen) versteht den Kontext nicht.
    *   Lösung: Nutzen Sie `llama3.1:latest`.

*   **Ollama findet Modelle nicht:**
    *   Prüfen Sie die Umgebungsvariable `OLLAMA_MODELS`. Starten Sie Ollama nach Änderungen neu (`Task Kill` & Neustart).

---

## 6. Entwickler-Infos (Rollen-Optimierung)

Für den **Frontend-Engineer** (`04_Frontend-Engineer.md`) gelten spezielle Regeln für sauberen Code:
*   **Vollständigkeit:** Muss CSS/JS korrekt verlinken.
*   **Platzhalter:** Muss Bild-Platzhalter (z.B. `placehold.co`) nutzen statt leerer `src=""`.
*   **Atomarität:** Erst Struktur (HTML), dann Design (CSS), dann Logik (JS).
