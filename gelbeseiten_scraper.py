#!/usr/bin/env python3
"""
Gelbe Seiten Scraper - COMPLETE VERSION mit Website & Logo
Extracts ALL tax consultant data including emails, websites, and logos
"""

import requests
from bs4 import BeautifulSoup
import csv
import json
import time
import re
import base64
from typing import List, Dict
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GelbeSeitenScraperComplete:
    def __init__(self, search_term: str = "steuerberater"):
        self.base_url = "https://www.gelbeseiten.de"
        self.ajax_url = f"{self.base_url}/ajaxsuche"
        self.search_term = search_term
        self.session = requests.Session()
        
        # Set up headers to mimic a real browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
            'Origin': self.base_url,
            'Referer': f'{self.base_url}/',
            'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
        })
        
        self.results = []
        self.total_available = 0
        
    def initialize_session(self):
        """Initialize session by visiting the main page to get cookies"""
        try:
            logger.info(f"Initializing session for search term: '{self.search_term}'...")
            response = self.session.get(
                f"{self.base_url}/suche/{self.search_term}/bundesweit",
                timeout=30
            )
            logger.info(f"Session initialized. Status: {response.status_code}")
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error initializing session: {e}")
            return False
    
    def decode_base64(self, encoded_str: str) -> str:
        """Decode base64 encoded string"""
        try:
            decoded = base64.b64decode(encoded_str).decode('utf-8')
            return decoded
        except Exception as e:
            logger.debug(f"Failed to decode base64: {e}")
            return ""
    
    def fetch_page(self, position: int, anzahl: int = 10) -> Dict:
        """
        Fetch a page of results using the AJAX endpoint
        
        Args:
            position: Starting position (0-based, increments by anzahl)
            anzahl: Number of results per page
            
        Returns:
            Dictionary with response data
        """
        try:
            # Prepare multipart form data
            data = {
                'umkreis': '-1',
                'verwandt': 'false',
                'WAS': self.search_term,
                'position': str(position),
                'anzahl': str(anzahl),
                'sortierung': 'relevanz'
            }
            
            logger.info(f"Fetching results from position {position}...")
            
            response = self.session.post(
                self.ajax_url,
                data=data,
                timeout=30
            )
            
            if response.status_code == 200:
                logger.info(f"Successfully fetched page at position {position}")
                try:
                    return response.json()
                except:
                    return {'html': response.text}
            else:
                logger.error(f"Failed to fetch page. Status: {response.status_code}")
                return {}
                
        except Exception as e:
            logger.error(f"Error fetching page at position {position}: {e}")
            return {}
    
    def parse_results(self, response_data: Dict) -> List[Dict[str, str]]:
        """
        Parse JSON response and extract business data
        
        Args:
            response_data: JSON response from AJAX endpoint
            
        Returns:
            List of dictionaries containing business information
        """
        results = []
        
        if not response_data or 'html' not in response_data:
            return results
        
        html = response_data['html']
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find all business entries
        entries = soup.find_all('article', class_=re.compile(r'mod-Treffer'))
        
        logger.info(f"Found {len(entries)} entries in this page")
        
        for entry in entries:
            try:
                data = {
                    'name': '',
                    'address': '',
                    'city': '',
                    'postal_code': '',
                    'phone': '',
                    'website': '',
                    'email': '',
                    'logo_url': '',
                    'rating': '',
                    'review_count': '',
                    'specialties': '',
                    'description': '',
                    'detail_url': ''
                }
                
                # Extract name
                name_tag = entry.find('h2', class_='mod-Treffer__name')
                if name_tag:
                    data['name'] = name_tag.get_text(strip=True)
                
                # Extract detail URL
                detail_link = entry.find('a', href=re.compile(r'/gsbiz/'))
                if detail_link:
                    href = detail_link['href']
                    if href.startswith('http'):
                        data['detail_url'] = href
                    else:
                        data['detail_url'] = self.base_url + href
                
                # Extract LOGO URL
                logo_img = entry.find('img', class_='mod-Treffer__logo')
                if logo_img and logo_img.get('src'):
                    logo_src = logo_img['src']
                    # Check if it's not the placeholder pixel
                    if 'pixel.png' not in logo_src and logo_src not in ['1px', '']:
                        # Make sure it's a full URL
                        if logo_src.startswith('http'):
                            data['logo_url'] = logo_src
                        elif logo_src.startswith('/'):
                            data['logo_url'] = self.base_url + logo_src
                        else:
                            data['logo_url'] = logo_src
                
                # Extract address
                address_container = entry.find('address', class_='mod-AdresseKompakt')
                if address_container:
                    address_text_div = address_container.find('div', class_='mod-AdresseKompakt__adress-text')
                    if address_text_div:
                        # Get full text
                        full_text = address_text_div.get_text(strip=True)
                        
                        # Extract postal code and city
                        city_span = address_text_div.find('span', class_='mod-AdresseKompakt__adress__ort')
                        if city_span:
                            city_postal = city_span.get_text(strip=True)
                            # Split postal code and city (e.g., "20354 Hamburg")
                            parts = city_postal.split(None, 1)
                            if len(parts) == 2:
                                data['postal_code'] = parts[0]
                                data['city'] = parts[1]
                        
                        # Extract street address (everything before the postal code)
                        address_only = full_text
                        if city_postal:
                            address_only = full_text.split(city_postal)[0]
                        # Remove trailing comma and extra spaces
                        data['address'] = address_only.rstrip(', ').strip()
                
                # Extract phone
                phone_container = entry.find('div', class_='mod-TelefonnummerKompakt')
                if phone_container:
                    phone_link = phone_container.find('a', class_='mod-TelefonnummerKompakt__phoneNumber')
                    if phone_link:
                        data['phone'] = phone_link.get_text(strip=True)
                
                # Extract WEBSITE URL (base64 encoded)
                # Note: BeautifulSoup converts all HTML attributes to lowercase!
                website_container = entry.find('div', class_='mod-WebseiteKompakt')
                if website_container:
                    website_span = website_container.find('span', class_='mod-WebseiteKompakt__text')
                    if website_span:
                        # HTML attributes are lowercase in BeautifulSoup
                        encoded_url = website_span.get('data-webseitelink', '')
                        if encoded_url:
                            decoded = self.decode_base64(encoded_url)
                            if decoded and decoded.startswith('http'):
                                data['website'] = decoded
                
                # Extract email from chat button data
                chat_button = entry.find('button', id=re.compile(r'mod-Chat__button'))
                if chat_button and chat_button.get('data-parameters'):
                    try:
                        chat_data_str = chat_button['data-parameters']
                        chat_data = json.loads(chat_data_str)
                        if 'inboxConfig' in chat_data:
                            organization = chat_data['inboxConfig'].get('organizationQuery', {})
                            generic = organization.get('generic', {})
                            if 'email' in generic:
                                data['email'] = generic['email']
                    except Exception as e:
                        logger.debug(f"Error parsing chat data: {e}")
                
                # Extract rating
                rating_span = entry.find('span', class_=re.compile(r'mod-BewertungKompakt__number'))
                if rating_span:
                    data['rating'] = rating_span.get_text(strip=True)
                
                # Extract review count
                review_span = entry.find('span', class_=re.compile(r'mod-BewertungKompakt__text'))
                if review_span:
                    review_text = review_span.get_text(strip=True)
                    # Extract number (e.g., "122 Bewertungen" -> "122")
                    review_match = re.search(r'(\d+)', review_text)
                    if review_match:
                        data['review_count'] = review_match.group(1)
                
                # Extract specialties
                specialty_tag = entry.find('p', class_=re.compile(r'mod-Treffer--besteBranche'))
                if specialty_tag:
                    data['specialties'] = specialty_tag.get_text(strip=True)
                
                # Extract description
                desc_tag = entry.find('div', class_='mod-Treffer__freitext')
                if desc_tag:
                    data['description'] = desc_tag.get_text(strip=True)
                
                # Only add if we have at least a name
                if data['name']:
                    results.append(data)
                
            except Exception as e:
                logger.error(f"Error parsing entry: {e}")
                continue
        
        return results
    
    def save_progress(self, filename: str):
        """Save current results to CSV"""
        if not self.results:
            return
        
        try:
            fieldnames = [
                'name', 'address', 'postal_code', 'city', 'phone', 
                'email', 'website', 'logo_url', 'rating', 'review_count', 
                'specialties', 'description', 'detail_url'
            ]
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for result in self.results:
                    row = {field: result.get(field, '') for field in fieldnames}
                    writer.writerow(row)
            
            logger.info(f"Progress saved: {len(self.results)} results")
            
        except Exception as e:
            logger.error(f"Error saving progress: {e}")
    
    def scrape_all(self, max_results: int = None, results_per_page: int = 10, 
                   output_file: str = None) -> List[Dict[str, str]]:
        """
        Scrape all results with pagination
        
        Args:
            max_results: Maximum number of results to fetch (None for all available)
            results_per_page: Number of results per page
            output_file: CSV file to save results (saves every 100 results)
            
        Returns:
            List of all scraped results
        """
        if not self.initialize_session():
            logger.error("Failed to initialize session")
            return []
        
        position = 0
        total_scraped = 0
        consecutive_failures = 0
        
        while True:
            # Check if we've reached max_results
            if max_results and total_scraped >= max_results:
                logger.info(f"Reached max_results limit: {max_results}")
                break
            
            # Fetch page
            response_data = self.fetch_page(position, results_per_page)
            
            if not response_data:
                consecutive_failures += 1
                logger.warning(f"No data returned for position {position} (failure {consecutive_failures}/3)")
                if consecutive_failures >= 3:
                    logger.error("Too many consecutive failures, stopping.")
                    break
                time.sleep(2)
                continue
            
            consecutive_failures = 0  # Reset on success
            
            # Parse results
            page_results = self.parse_results(response_data)
            
            if not page_results:
                logger.info(f"No more results found at position {position}")
                break
            
            self.results.extend(page_results)
            total_scraped += len(page_results)
            
            # Log progress
            if self.total_available > 0:
                progress = (total_scraped / self.total_available) * 100
                logger.info(f"Progress: {total_scraped}/{self.total_available} ({progress:.1f}%)")
            else:
                logger.info(f"Total scraped so far: {total_scraped}")
            
            # Save progress every 100 results
            if output_file and total_scraped % 100 == 0:
                self.save_progress(output_file)
            
            # Move to next page
            position += results_per_page
            
            # Be respectful with rate limiting
            time.sleep(1)
        
        logger.info(f"Scraping complete. Total results: {len(self.results)}")
        return self.results
    
    def export_to_csv(self, filename: str = "gelbeseiten.csv"):
        """
        Export scraped results to CSV
        
        Args:
            filename: Output CSV filename
        """
        if not self.results:
            logger.warning("No results to export")
            return
        
        try:
            fieldnames = [
                'name', 'address', 'postal_code', 'city', 'phone', 
                'email', 'website', 'logo_url', 'rating', 'review_count', 
                'specialties', 'description', 'detail_url'
            ]
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for result in self.results:
                    row = {field: result.get(field, '') for field in fieldnames}
                    writer.writerow(row)
            
            logger.info(f"Successfully exported {len(self.results)} results to {filename}")
            
            # Print statistics
            emails_found = sum(1 for r in self.results if r.get('email'))
            websites_found = sum(1 for r in self.results if r.get('website'))
            logos_found = sum(1 for r in self.results if r.get('logo_url'))
            
            print(f"\n{'='*70}")
            print("SCRAPING STATISTICS")
            print(f"{'='*70}")
            print(f"Total entries scraped: {len(self.results)}")
            print(f"Entries with email: {emails_found} ({emails_found/len(self.results)*100:.1f}%)")
            print(f"Entries with website: {websites_found} ({websites_found/len(self.results)*100:.1f}%)")
            print(f"Entries with logo: {logos_found} ({logos_found/len(self.results)*100:.1f}%)")
            print(f"Output file: {filename}")
            print(f"{'='*70}\n")
            
        except Exception as e:
            logger.error(f"Error exporting to CSV: {e}")


def main():
    """Main execution function"""
    print("=" * 70)
    print("Gelbe Seiten Scraper - COMPLETE VERSION")
    print("Mit Website & Logo URLs!")
    print("=" * 70)
    print()
    
    # Ask for search term
    print("🔍 SUCHBEGRIFF:")
    print("-" * 70)
    search_term = input("Was möchtest du scrapen? [default: steuerberater]: ").strip() or "steuerberater"
    print(f"➜ Suche nach: '{search_term}'")
    print()
    
    # Ask user for mode
    print("📊 SCRAPING-MODUS:")
    print("-" * 70)
    print("1. Test mode (first 100 results)")
    print("2. Full scrape (ALL results - may take hours)")
    print("3. Custom amount")
    print()
    
    choice = input("Enter choice (1/2/3) [default: 1]: ").strip() or "1"
    
    max_results = None
    if choice == "1":
        max_results = 100
        print(f"\n➜ Test mode: Scraping first {max_results} results")
    elif choice == "2":
        print("\n➜ Full scrape mode: This will scrape ALL available results.")
        print("   This may take several hours. Progress will be saved every 100 results.")
        confirm = input("   Continue? (yes/no) [no]: ").strip().lower()
        if confirm != "yes":
            print("Cancelled.")
            return
        max_results = None
    elif choice == "3":
        max_results = int(input("Enter number of results to scrape: ").strip())
        print(f"\n➜ Custom mode: Scraping {max_results} results")
    
    print()
    
    # Create scraper instance with search term
    scraper = GelbeSeitenScraperComplete(search_term=search_term)
    
    # Output file (with search term in filename)
    safe_search_term = search_term.replace(" ", "_").replace("/", "_")
    output_file = f"gelbeseiten_{safe_search_term}.csv"
    
    # Start scraping
    print("Starting scraper...")
    print()
    
    results = scraper.scrape_all(
        max_results=max_results, 
        results_per_page=10,
        output_file=output_file
    )
    
    # Export to CSV
    if results:
        scraper.export_to_csv(output_file)
        print(f"✓ Done! Results saved to: {output_file}")
    else:
        print("✗ No results were scraped")


if __name__ == "__main__":
    main()

