#!/usr/bin/env python3
"""
Test Script für Gelbe Seiten Scraper - Steuerberater
Testet den Scraper automatisch und zeigt Ergebnisse
"""

import sys
from gelbeseiten_scraper import GelbeSeitenScraperComplete
import csv

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(text)
    print("=" * 80 + "\n")

def print_section(text):
    """Print formatted section"""
    print("\n" + "-" * 80)
    print(text)
    print("-" * 80)

def test_scraper():
    """Test the scraper with Steuerberater"""
    
    print_header("🧪 GELBE SEITEN SCRAPER - STEUERBERATER TEST")
    
    # Configuration
    search_term = "steuerberater"
    test_amount = 50  # Schneller Test mit 50 Einträgen
    output_file = "test_steuerberater.csv"
    
    print(f"📋 TEST-KONFIGURATION:")
    print(f"   Suchbegriff: {search_term}")
    print(f"   Anzahl: {test_amount} Einträge")
    print(f"   Output: test_steuerberater.csv")
    
    # Create scraper
    print_section("🚀 PHASE 1: Scraper initialisieren")
    scraper = GelbeSeitenScraperComplete(search_term=search_term)
    print("✓ Scraper erstellt")
    
    # Start scraping
    print_section("🔄 PHASE 2: Daten scrapen")
    print(f"Starte Scraping von {test_amount} Steuerberater-Einträgen...\n")
    
    results = scraper.scrape_all(
        max_results=test_amount,
        results_per_page=10,
        output_file=output_file
    )
    
    if not results:
        print("❌ FEHLER: Keine Ergebnisse!")
        return False
    
    print(f"\n✓ Scraping abgeschlossen: {len(results)} Einträge")
    
    # Export to CSV
    print_section("💾 PHASE 3: CSV Export")
    scraper.export_to_csv(output_file)
    print(f"✓ CSV gespeichert: {output_file}")
    
    # Validate data
    print_section("✅ PHASE 4: Daten-Validierung")
    
    with open(output_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        csv_data = list(reader)
    
    # Count various fields
    stats = {
        'total': len(csv_data),
        'with_name': sum(1 for r in csv_data if r['name']),
        'with_address': sum(1 for r in csv_data if r['address']),
        'with_postal': sum(1 for r in csv_data if r['postal_code']),
        'with_city': sum(1 for r in csv_data if r['city']),
        'with_phone': sum(1 for r in csv_data if r['phone']),
        'with_email': sum(1 for r in csv_data if r['email']),
        'with_website': sum(1 for r in csv_data if r['website']),
        'with_logo': sum(1 for r in csv_data if r['logo_url']),
        'with_rating': sum(1 for r in csv_data if r['rating']),
        'complete': sum(1 for r in csv_data if r['email'] and r['website'] and r['logo_url']),
    }
    
    print(f"Validierungs-Ergebnisse:")
    print(f"   Total Einträge:        {stats['total']}")
    print(f"   Mit Name:              {stats['with_name']:3d} / {stats['total']} ({stats['with_name']/stats['total']*100:5.1f}%) {'✅' if stats['with_name'] == stats['total'] else '❌'}")
    print(f"   Mit Adresse:           {stats['with_address']:3d} / {stats['total']} ({stats['with_address']/stats['total']*100:5.1f}%) {'✅' if stats['with_address'] > stats['total']*0.95 else '⚠️'}")
    print(f"   Mit PLZ:               {stats['with_postal']:3d} / {stats['total']} ({stats['with_postal']/stats['total']*100:5.1f}%) {'✅' if stats['with_postal'] > stats['total']*0.95 else '⚠️'}")
    print(f"   Mit Stadt:             {stats['with_city']:3d} / {stats['total']} ({stats['with_city']/stats['total']*100:5.1f}%) {'✅' if stats['with_city'] > stats['total']*0.95 else '⚠️'}")
    print(f"   Mit Telefon:           {stats['with_phone']:3d} / {stats['total']} ({stats['with_phone']/stats['total']*100:5.1f}%) {'✅' if stats['with_phone'] > stats['total']*0.95 else '⚠️'}")
    print(f"   Mit E-Mail:            {stats['with_email']:3d} / {stats['total']} ({stats['with_email']/stats['total']*100:5.1f}%) {'✅' if stats['with_email'] > 0 else '❌'}")
    print(f"   Mit Website:           {stats['with_website']:3d} / {stats['total']} ({stats['with_website']/stats['total']*100:5.1f}%) {'✅' if stats['with_website'] > stats['total']*0.80 else '⚠️'}")
    print(f"   Mit Logo:              {stats['with_logo']:3d} / {stats['total']} ({stats['with_logo']/stats['total']*100:5.1f}%) {'✅' if stats['with_logo'] > stats['total']*0.70 else '⚠️'}")
    print(f"   Mit Bewertung:         {stats['with_rating']:3d} / {stats['total']} ({stats['with_rating']/stats['total']*100:5.1f}%)")
    print(f"   KOMPLETT (E+W+L):      {stats['complete']:3d} / {stats['total']} ({stats['complete']/stats['total']*100:5.1f}%) {'✅' if stats['complete'] > 0 else '❌'}")
    
    # Show sample entries
    print_section("📋 BEISPIEL-EINTRÄGE")
    
    # Find entries with complete data
    complete_entries = [r for r in csv_data if r['email'] and r['website'] and r['logo_url']]
    
    if complete_entries:
        print(f"Zeige erste 3 KOMPLETTE Einträge (mit E-Mail, Website & Logo):\n")
        for i, entry in enumerate(complete_entries[:3], 1):
            print(f"{i}. {entry['name']}")
            print(f"   📍 {entry['address']}, {entry['postal_code']} {entry['city']}")
            print(f"   📞 {entry['phone']}")
            print(f"   📧 {entry['email']}")
            print(f"   🌐 {entry['website'][:60]}...")
            print(f"   🖼️  {entry['logo_url'][:60]}...")
            if entry['rating']:
                print(f"   ⭐ {entry['rating']} ({entry['review_count']} Bewertungen)")
            print()
    else:
        print("⚠️ Keine kompletten Einträge gefunden")
        # Show any entries
        if csv_data:
            print("\nErste 3 Einträge (teilweise Daten):\n")
            for i, entry in enumerate(csv_data[:3], 1):
                print(f"{i}. {entry['name']}")
                print(f"   📍 {entry['address']}, {entry['postal_code']} {entry['city']}")
                print(f"   📞 {entry['phone']}")
                if entry['email']:
                    print(f"   📧 {entry['email']}")
                if entry['website']:
                    print(f"   🌐 {entry['website'][:60]}")
                print()
    
    # Test result
    print_section("🎯 TEST-ERGEBNIS")
    
    # Check if test passed
    test_passed = (
        stats['with_name'] == stats['total'] and
        stats['with_phone'] > stats['total'] * 0.95 and
        stats['with_email'] > 0 and
        stats['with_website'] > stats['total'] * 0.80 and
        stats['with_logo'] > stats['total'] * 0.70
    )
    
    if test_passed:
        print("✅ TEST BESTANDEN!")
        print("   Alle kritischen Datenfelder werden korrekt extrahiert.")
        print(f"   Der Scraper ist bereit für den produktiven Einsatz.")
    else:
        print("⚠️ TEST TEILWEISE BESTANDEN")
        print("   Einige Felder haben niedrigere Quoten als erwartet.")
        print("   Der Scraper funktioniert aber grundsätzlich.")
    
    print()
    print(f"📁 Test-Datei: {output_file}")
    print(f"🔍 Getesteter Suchbegriff: {search_term}")
    print(f"📊 Einträge: {stats['total']}")
    
    print_header("✨ TEST ABGESCHLOSSEN")
    
    return test_passed


if __name__ == "__main__":
    try:
        success = test_scraper()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Test abgebrochen durch Benutzer")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ FEHLER: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

