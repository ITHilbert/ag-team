# Anforderungen (aus idee.md & README.md)

**1. Vision & Gameplay-Ziele**
*   **Setting:** Industrielle Revolution.
*   **Format:** Webbasierte Anwendung als MVP/Testballon für ein späteres Brettspiel.
*   **Kernmechanik:** Spieler agieren als Investoren, gründen und übernehmen Firmen.
*   **Spielziel:** Aufbau von Vermögen durch Aktienbesitz und Dividenden/Firmenwert.

**2. Wirtschafts-System**
*   **Firmen-Struktur:**
    *   **Anteile:** Jede Firma hat genau 10 Aktien.
    *   **Kontrolle:** Der Spieler mit den meisten Anteilen steuert die Firma (CEO). Bei Gleichstand behält der aktuelle CEO die Kontrolle.
    *   **Gründung/Aktivierung:** 
        *   (Konflikt: idee.md sagt 3 Anteile, README sagt 6 Anteile. Bitte klären oder konfigurierbar machen.)
    *   **Vermögen:** Trennung zwischen Privatvermögen und Firmenkapital.

*   **Ressourcen & Produktion:**
    *   **Rohstoffe (Tier 1):** Stein, Kohle, Eisen, Holz.
        *   4 Vorkommen je Rohstoff.
        *   Preisstaffelung: 50, 100, 150, 200 GE.
        *   Limit: Max 10 Einheiten Abbau pro Ort.
    *   **Zwischenprodukte (Tier 2):** 
        *   Waffen (Werkzeug + Eisen)
        *   Werkzeug (Holz + Eisen)
        *   Dampfmaschinen (Werkzeug + Eisen)
        *   2 Standorte je Produkt.
    *   **Endprodukte (Tier 3):**
        *   Eisenbahn (Dampfmaschine + 2x Eisen)
        *   Kolonialgüter (2x Waffen)
        *   1 Standort je Produkt.

*   **Logistik:**
    *   Firmen können "transportNeeded" sein.
    *   Bedingung: Mindestens eine aktive Transportfirma im Spiel.
    *   Strafe: Doppelte Unterhaltskosten bei Fehlen.

**3. Spielablauf**
1.  **Aktienphase:** Aktien kaufen/verkaufen.
2.  **Firmenphase:**
    *   Mitarbeiter einstellen/entlassen.
    *   Rohstoffe einkaufen.
    *   Produzieren.
    *   Investieren.
    *   Produkte verkaufen.
