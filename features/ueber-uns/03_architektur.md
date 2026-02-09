# Architektur: Über Uns Seite

## Übersicht
Implementierung einer statischen HTML-Seite zur Vorstellung des AG-Teams.
Der Fokus liegt auf sauberem HTML5, semantischer Struktur und modernem CSS-Design.

## Technologie-Stack
- **HTML5**: Semantisches Markup.
- **CSS3**: Vanilla CSS (keine Frameworks wie Bootstrap/Tailwind, außer global definiert).
- **Assets**: Ggf. Platzhalter-Bilder für Agenten (oder FontAwesome Icons).

## Dateistruktur
- `projekt/03_ergebnisse/ueber-uns.html` (Finales Ergebnis)
- `projekt/02_arbeit/ueber-uns/` (Arbeitsverzeichnis)
  - `index.html`
  - `style.css`

## Kapselung & Design
- **Single Page Design**: Alles auf einer Seite.
- **Responsive**: Grid-Layout für Desktop (Nebeneinander), Stack für Mobile (Untereinander).
- **Design-System**:
  - Farben: Dunkles Theme (Dark Mode) bevorzugt, akzentuiert mit Neon-Farben (Cyberpunk/Tech-Look) oder cleanes Modern UI.
  - Typografie: Lesbare Sans-Serif Fonts (z.B. Inter, Roboto).

## Komponenten
1.  **Header**: Navigation (Startseite, Über Uns).
2.  **Hero Section**: Titel "Das AG-Team", kurzer Einleitungstext ("Wir sind die KI-Agenten...").
3.  **Team Grid**: Container für die Agenten-Karten.
    - **Agent Card**:
      - Name (z.B. "Moderator")
      - Rolle (z.B. "Orchestrierung")
      - Beschreibungstext
      - (Optional) Icon/Avatar
4.  **Footer**: Copyright.

## Schnittstellen
- Keine externen Datenquellen. Hardcoded Content aus `02_spec.md`.

## Tasks für Worker (Frontend-Engineer)
1.  [ ] Arbeitsverzeichnis `projekt/02_arbeit/ueber-uns/` anlegen.
2.  [ ] `index.html` Gerüst erstellen.
3.  [ ] `style.css` erstellen und einbinden.
4.  [ ] Header und Hero Section implementieren.
5.  [ ] Team Grid mit 5 Cards (Moderator, PM, Architekt, Worker, Admin) implementieren.
6.  [ ] Inhalte aus Spec einfügen.
7.  [ ] Styling finalisieren (Responsive Check).
