# AG-Team – Prozessablauf (Aider + Ollama/Mistral)

## Feature-Dateistandard
Für alle neuen Features gilt der verbindliche **[Feature-Dateistandard](./FEATURE_STANDARD.md)**.
Bitte beachte die dort definierten Templates und Gate-Kriterien für jede Phase.

## Rollen-Gesamtfluss

Der Moderator ist die einzige steuernde Instanz.
Alle anderen Rollen arbeiten ausschließlich auf klaren Arbeitsaufträgen des Moderators.

---

## 1. Intake / Klärung
Rolle: Moderator

Artefakt:
- features/<feature>/01_intake.md

Gate:
- Ziel klar
- Nicht-Ziele dokumentiert
- offene Fragen markiert

---

## 2. Anforderungsdefinition
Rolle: Produktmanager

Artefakt:
- features/<feature>/02_spec.md

Gate:
- User Stories vorhanden
- Akzeptanzkriterien testbar
- Abhängigkeiten dokumentiert

---

## 3. Architektur & Design
Rolle: Systemarchitekt

Artefakt:
- features/<feature>/03_architektur.md

Gate:
- Entscheidung dokumentiert
- Schnittstellen definiert
- Datenmodelle beschrieben

---

## 4. Implementierung (Aider Loop)
Rollen:
- Backend Engineer
- Frontend Engineer

Regeln:
- nur zugewiesene Dateien ändern
- immer Tests mitliefern
- kleine Commits

Gate:
- Build erfolgreich
- Tests grün

---

## 5. Qualitätssicherung
Rolle: QA Engineer

Artefakt:
- features/<feature>/04_qa.md

Gate:
- alle ACs geprüft
- bekannte Fehler dokumentiert

---

## 6. Security Review (optional / vor Release Pflicht bei externen Schnittstellen)
Rolle: Security Reviewer

Artefakt:
- features/<feature>/05_security.md

Gate:
- keine offenen High-Risks

---

## 7. Release & Automatisierung
Rolle: DevOps Engineer

Artefakt:
- features/<feature>/06_release.md

Gate:
- Build reproduzierbar
- Release-Checkliste erfüllt

---

## 8. Freigabe
Rolle: Moderator

Artefakt:
- features/<feature>/07_freigabe.md

Gate:
- Freigabe oder Rückführung in vorherige Phase
