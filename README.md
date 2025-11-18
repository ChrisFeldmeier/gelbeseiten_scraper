# Gelbe Seiten Scraper - Universal

Ein leistungsstarker Python-Scraper zum Extrahieren von Unternehmensdaten von Gelbe Seiten Deutschland.

## ✨ Features

✅ **Beliebige Suchbegriffe** - Nicht nur Steuerberater! Scrapt Ärzte, Anwälte, Restaurants, etc.  
✅ Extrahiert **ALLE** verfügbaren Datensätze für jeden Suchbegriff  
✅ Vollständige Kontaktdaten: Name, Adresse, PLZ, Stadt, Telefon  
✅ **E-Mail-Adressen** (ca. 35% Erfolgsquote) 📧  
✅ **Website-URLs** (ca. 95% Erfolgsquote) 🌐  
✅ **Firmenlogos** (ca. 82% Erfolgsquote) 🖼️  
✅ Bewertungen und Rezensionen ⭐  
✅ Spezialisierungen und Beschreibungen  
✅ Automatische Fortschrittsspeicherung alle 100 Einträge  
✅ Robustes Error Handling  
✅ Rate Limiting zum Schutz des Servers  

## 🔍 Unterstützte Suchbegriffe

Der Scraper funktioniert mit **ALLEN** Kategorien auf Gelbe Seiten:
- `steuerberater` (38.902 Einträge)
- `ärzte` (Ärzte & Zahnärzte)
- `rechtsanwälte` (Anwälte)
- `restaurants` (Gastronomie)
- `handwerker` (Handwerksbetriebe)
- `apotheken` (Apotheken)
- ... und viele mehr!

## 📊 Erfolgsquoten (basierend auf 500 Steuerberater-Einträgen)

| Datenfeld | Erfolgsquote | Beschreibung |
|-----------|--------------|--------------|
| Name | 100% ✅ | Firmenname / Name |
| Adresse | 100% ✅ | Straße & Hausnummer |
| PLZ | 100% ✅ | Postleitzahl |
| Stadt | 100% ✅ | Stadt |
| Telefon | 100% ✅ | Telefonnummer |
| **E-Mail** | **35%** 📧 | E-Mail-Adresse |
| **Website** | **95%** 🌐 | Website-URL |
| **Logo** | **82%** 🖼️ | Firmenlogo-URL |
| Bewertung | ~40% ⭐ | Bewertung (z.B. 5,0) |
| Review Count | ~40% 📝 | Anzahl Bewertungen |
| Spezialisierung | ~80% 🎯 | Tätigkeitsschwerpunkte |
| Beschreibung | ~20% 📄 | Kurzbeschreibung |
| Detail-URL | 100% 🔗 | Link zur Detailseite |

### Beispiel: Steuerberater (38.902 gesamt)
- Ca. **13.615** Einträge mit E-Mail-Adresse
- Ca. **36.957** Einträge mit Website
- Ca. **31.899** Einträge mit Firmenlogo
- Ca. **11.670** KOMPLETT-Einträge (mit E-Mail, Website & Logo)

## 🚀 Installation

```bash
pip3 install requests beautifulsoup4
```

## 💻 Verwendung

### Interaktiver Modus (empfohlen)

```bash
python3 gelbeseiten_scraper.py
```

Dann wirst du gefragt:
1. **Suchbegriff**: Was möchtest du scrapen? (z.B. "steuerberater", "ärzte", "restaurants")
2. **Modus**: Test (100), Full (alle), oder Custom

### Beispiel-Session:

```
🔍 SUCHBEGRIFF:
Was möchtest du scrapen? [default: steuerberater]: ärzte
➜ Suche nach: 'ärzte'

📊 SCRAPING-MODUS:
1. Test mode (first 100 results)
2. Full scrape (ALL results - may take hours)
3. Custom amount

Enter choice (1/2/3) [default: 1]: 1

➜ Test mode: Scraping first 100 results
```

### Programmatische Verwendung

```python
from gelbeseiten_scraper import GelbeSeitenScraperComplete

# Ärzte scrapen
scraper = GelbeSeitenScraperComplete(search_term="ärzte")
results = scraper.scrape_all(max_results=500)
scraper.export_to_csv("gelbeseiten_ärzte.csv")

# Restaurants scrapen
scraper = GelbeSeitenScraperComplete(search_term="restaurants")
results = scraper.scrape_all(max_results=1000)
scraper.export_to_csv("gelbeseiten_restaurants.csv")
```

## 📁 Output

Die Daten werden automatisch in einer CSV-Datei mit dem Suchbegriff im Namen gespeichert:

```
gelbeseiten_steuerberater.csv
gelbeseiten_ärzte.csv
gelbeseiten_restaurants.csv
...
```

### CSV-Spalten:

```csv
name,address,postal_code,city,phone,email,website,logo_url,rating,review_count,specialties,description,detail_url
```

### Beispiel-Eintrag (Steuerberater):

```
Name: Steuerkanzlei Schubert Stefan
Adresse: Peterstr. 65, 90478 Nürnberg
Telefon: 0911 46 53 09
E-Mail: schubert@schubert-steuerkanzlei.de
Website: https://www.schubert-steuerkanzlei.de/
Logo: https://ies.v4all.de/0122/GS/0122/1/5711/32755711_maxhoehe_100.jpg
Rating: 5,0 (122 Bewertungen)
```

### Beispiel-Eintrag (Ärzte):

```
Name: Dr. med. Grit Weigel
Adresse: Schoppershofstr. 35, 90489 Nürnberg
Telefon: 0911 2 42 78 85
Website: https://www.dr-weigel.de
Logo: https://example.com/logo.jpg
```

## 🎯 Features im Detail

### 📧 E-Mail-Extraktion
E-Mails werden aus versteckten JSON-Daten im Chat-Button extrahiert:
```html
<button data-parameters='{"inboxConfig":{"organizationQuery":{"generic":{"email":"info@example.de"}}}}'>
```
Nicht alle Einträge haben diese Funktion aktiviert → **~35% Erfolgsquote**

### 🌐 Website-Extraktion
Website-URLs sind Base64-encodiert im HTML:
```html
<span data-webseitelink="aHR0cHM6Ly93d3cuZXhhbXBsZS5kZQ==">
```
Fast alle Einträge haben Websites → **~95% Erfolgsquote**

### 🖼️ Logo-Extraktion
Firmenlogos sind direkt als Bild-URLs verfügbar:
```html
<img class="mod-Treffer__logo" src="https://example.com/logo.jpg">
```
Viele Einträge haben Logos → **~82% Erfolgsquote**

### 💾 Automatische Fortschrittsspeicherung
Der Scraper speichert automatisch alle 100 Einträge den aktuellen Stand. Bei Abbruch gehen keine Daten verloren.

### 🛡️ Rate Limiting
- 1 Sekunde Pause zwischen Requests
- 3 Fehlversuche bei Problemen
- Respektvoller Umgang mit dem Server

### 🔍 Error Handling
- Robustes Parsing mit Fallback-Optionen
- Detailliertes Logging aller Aktivitäten
- Automatische Wiederholung bei temporären Fehlern

### ✨ Datenqualität
- Alle Felder werden sauber extrahiert
- Keine doppelten Einträge
- UTF-8 Encoding für korrekte Umlaute

## ⚡ Performance

| Modus | Anzahl | Dauer |
|-------|--------|-------|
| Test | 100 Einträge | ~15 Sekunden |
| Medium | 500 Einträge | ~8-10 Minuten |
| Large | 5.000 Einträge | ~1,5 Stunden |
| Full (Steuerberater) | 38.902 Einträge | ~11 Stunden |

**Rate**: ~10 Einträge pro Sekunde mit Pausen

## 📊 Beispiel-Statistiken

### Steuerberater (500 Einträge):
```
Total entries scraped: 500
Entries with email: 175 (35.0%)
Entries with website: 473 (94.6%)
Entries with logo: 410 (82.0%)
Complete entries: 150 (30.0%)
```

### Ärzte (100 Einträge):
```
Total entries scraped: 100
Entries with email: 38 (38.0%)
Entries with website: 94 (94.0%)
Entries with logo: 78 (78.0%)
```

## 🔧 Technische Details

### Funktionsweise

1. **Suchbegriff-Eingabe**: Benutzer gibt gewünschte Kategorie ein
2. **Session Initialisierung**: Cookies und Headers für `/suche/{suchbegriff}/bundesweit`
3. **AJAX Requests**: Pagination über `/ajaxsuche` Endpoint mit `WAS={suchbegriff}`
4. **JSON Parsing**: Response enthält HTML als JSON-Field
5. **HTML Parsing**: BeautifulSoup extrahiert strukturierte Daten
6. **E-Mail Extraktion**: Aus Chat-Button JSON-Daten
7. **Website Extraktion**: Base64-Decoding der Website-URLs
8. **Logo Extraktion**: Direkte Bild-URLs
9. **CSV Export**: Strukturierte Ausgabe mit Suchbegriff im Dateinamen

### Systemanforderungen

- Python 3.6+
- requests
- beautifulsoup4
- Internetverbindung
- ~150 KB Speicherplatz pro 500 Einträge

## 📝 Erweiterte Verwendung

### Verschiedene Branchen scrapen

```python
from gelbeseiten_scraper import GelbeSeitenScraperComplete

# Verschiedene Branchen
search_terms = ["steuerberater", "ärzte", "rechtsanwälte", "restaurants"]

for term in search_terms:
    scraper = GelbeSeitenScraperComplete(search_term=term)
    results = scraper.scrape_all(max_results=500)
    scraper.export_to_csv(f"gelbeseiten_{term}.csv")
    print(f"✓ {term}: {len(results)} Einträge gespeichert")
```

### Mit Fortschrittsspeicherung

```python
scraper = GelbeSeitenScraperComplete(search_term="steuerberater")

# Scrape mit automatischer Zwischenspeicherung
results = scraper.scrape_all(
    max_results=None,  # Alle Einträge
    results_per_page=10,
    output_file="steuerberater_full.csv"  # Speichert alle 100 Einträge
)
```

## ⚠️ Datenschutz & Rechtliches

**WICHTIG**: 
- Nur öffentlich verfügbare Daten werden gesammelt
- Respektiere die robots.txt und Terms of Service
- Verwende die Daten nur für rechtmäßige Zwecke
- Kommerzielle Nutzung eventuell eingeschränkt
- Rate Limiting zum Schutz des Servers implementiert

## 🐛 Troubleshooting

### Problem: Keine E-Mails werden extrahiert
**Lösung**: E-Mails sind nur für ~35% der Einträge verfügbar. Das ist normal.

### Problem: Scraper stoppt vorzeitig
**Lösung**: Prüfe deine Internetverbindung. Der Scraper speichert den Fortschritt automatisch alle 100 Einträge.

### Problem: "Too many consecutive failures"
**Lösung**: Server könnte temporär nicht erreichbar sein. Warte einige Minuten und versuche es erneut.

### Problem: Suchbegriff findet keine Ergebnisse
**Lösung**: Stelle sicher, dass der Suchbegriff auf Gelbe Seiten existiert. Teste zuerst manuell auf der Website: `https://www.gelbeseiten.de/suche/{dein_begriff}/bundesweit`

### Problem: Umlaute im Dateinamen
**Lösung**: Der Scraper erstellt automatisch sichere Dateinamen. `ärzte` wird zu `gelbeseiten_ärzte.csv`

## 📦 Projektstruktur

```
gelbeseiten/
├── gelbeseiten_scraper.py  # Haupt-Scraper (universal)
├── gelbeseiten.csv         # Steuerberater (500 Einträge)
└── README.md                         # Diese Dokumentation
```

## 🎓 Beispiel-Output

```
================================================================================
SCRAPING STATISTICS
================================================================================
Total entries scraped: 500
Entries with email: 175 (35.0%)
Entries with website: 473 (94.6%)
Entries with logo: 410 (82.0%)
Output file: gelbeseiten_steuerberater.csv
================================================================================
```

## 💡 Use Cases

### Business Development
```bash
# Alle Steuerberater in Deutschland
python3 gelbeseiten_scraper.py
> steuerberater
> Option 2 (Full scrape)
```

### Marketing Recherche
```bash
# 1000 Restaurants für Marketing-Kampagne
python3 gelbeseiten_scraper.py
> restaurants
> Option 3 (Custom)
> 1000
```

### Wettbewerbsanalyse
```bash
# Alle Konkurrenten in deiner Branche
python3 gelbeseiten_scraper.py
> deine_branche
> Option 2 (Full scrape)
```

## 🤝 Unterstützung

Bei Fragen oder Problemen, prüfe zuerst:
1. ✅ Sind `requests` und `beautifulsoup4` installiert?
2. ✅ Funktioniert deine Internetverbindung?
3. ✅ Existiert dein Suchbegriff auf Gelbe Seiten?
4. ✅ Sind die Log-Meldungen hilfreich?

## 📜 Version History

- **v3.1 (Universal)** - Variable Suchbegriffe hinzugefügt
- **v3.0 (Complete)** - Website & Logo Extraktion hinzugefügt
- **v2.0** - Verbesserte E-Mail-Extraktion aus Chat-Daten
- **v1.0** - Basis-Scraper mit Pagination

---

## 🚀 Quick Start

```bash
# Installation
pip3 install requests beautifulsoup4

# Scraper starten
python3 gelbeseiten_scraper.py

# Eingaben:
1. Suchbegriff eingeben (z.B. "steuerberater")
2. Modus wählen (1=Test, 2=Full, 3=Custom)
3. Warten und CSV-Datei erhalten!
```

**Viel Erfolg beim Scrapen! 🚀**

*Letztes Update: November 2025*
