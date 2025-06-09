import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

class EcommerceScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        self.price_bands = {
            'Band 1': (50000, 69999),
            'Band 2': (70000, 99999),
            'Band 3': (100000, float('inf'))
        }

    def clean_price(self, price_str):
        """Extract numeric price from string"""
        try:
            return float(''.join(filter(str.isdigit, price_str)))
        except:
            return 0

    def get_price_band(self, price):
        """Determine price band for a given price"""
        for band, (min_price, max_price) in self.price_bands.items():
            if min_price <= price <= max_price:
                return band
        return 'Other'  # Default band for prices that don't fit in defined ranges

    def scrape_amazon(self, search_term):
      base_url = f"https://www.amazon.in/s?k={search_term}&rh=n%3A1805560031"
      products = []
      
      try:
          response = requests.get(base_url, headers=self.headers, timeout=10)
          
          if response.status_code != 200:
              print(f"Error fetching Amazon page, status code: {response.status_code}")
              return []

          soup = BeautifulSoup(response.content, 'html.parser')
          
          # Debugging: print the response content to see what is being returned
          # print(soup.prettify())
          
          items = soup.find_all('div', {'data-component-type': 's-search-result'})
          
          if not items:
              print("No products found on Amazon page!")
          
          for item in items:
              try:
                  title = item.find('span', class_='a-text-normal')
                  price_elem = item.find('span', class_='a-price-whole')
                  
                  if title and price_elem:
                      title = title.text.strip()
                      price = self.clean_price(price_elem.text)
                      
                      if price >= 50000:  # Only include products in our price bands
                          price_band = self.get_price_band(price)
                          specs = self.extract_amazon_specs(item)
                          products.append({
                              'Platform': 'Amazon',
                              'Title': title,
                              'Price': price,
                              'Price_Band': price_band,
                              'Specifications': specs
                          })
              except Exception as e:
                  print(f"Error processing an item: {e}")
                  continue
                  
          time.sleep(random.uniform(1, 2))
          return products
      
      except Exception as e:
          print(f"Error scraping Amazon: {e}")
          return []


    def scrape_flipkart(self, search_term):
        """Scrape product details from Flipkart"""
        base_url = f"https://www.flipkart.com/search?q={search_term}&otracker=search&otracker1=search"
        products = []
        
        try:
            response = requests.get(base_url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            items = soup.find_all('div', {'class': 'tUxRFH'})
            
            for item in items:
                try:
                    title_elem = item.find('div', {'class': 'KzDlHZ'})
                    price_elem = item.find('div', {'class': 'Nx9bqj _4b5DiR'})
                    
                    if title_elem and price_elem:
                        title = title_elem.text.strip()
                        price = self.clean_price(price_elem.text)
                        
                        if price >= 50000:  # Only include products in our price bands
                            price_band = self.get_price_band(price)
                            specs = self.extract_flipkart_specs(item)
                            products.append({
                                'Platform': 'Flipkart',
                                'Title': title,
                                'Price': price,
                                'Price_Band': price_band,
                                'Specifications': specs
                            })
                except Exception as e:
                    continue
                    
            time.sleep(random.uniform(1, 2))
            return products
            
        except Exception as e:
            print(f"Error scraping Flipkart: {e}")
            return []

    def extract_amazon_specs(self, item):
        """Extract specifications from Amazon product"""
        specs = {}
        try:
            specs_elem = item.find('div', {'class': 'a-section a-spacing-none'})
            if specs_elem:
                # Common specifications to look for
                spec_keys = ['Display', 'RAM', 'Storage', 'Camera', 'Battery']
                for key in spec_keys:
                    spec = specs_elem.find(text=lambda t: t and key in t)
                    if spec:
                        specs[key] = spec.strip()
        except Exception:
            pass
        return specs

    def extract_flipkart_specs(self, item):
        """Extract specifications from Flipkart product"""
        specs = {}
        try:
            specs_elem = item.find('ul', {'class': '_1xgFaf'})
            if specs_elem:
                spec_items = specs_elem.find_all('li')
                for spec in spec_items:
                    parts = spec.text.split('|')
                    for part in parts:
                        if ':' in part:
                            key, value = part.split(':', 1)
                            specs[key.strip()] = value.strip()
        except Exception:
            pass
        return specs

    def compare_prices(self, search_terms):
        """Compare prices across platforms for given search terms"""
        all_products = []
        
        for term in search_terms:
            print(f"Scraping data for {term}...")
            # Use ThreadPoolExecutor to scrape both sites concurrently
            with ThreadPoolExecutor(max_workers=2) as executor:
                amazon_future = executor.submit(self.scrape_amazon, term)
                flipkart_future = executor.submit(self.scrape_flipkart, term)
                
                amazon_products = amazon_future.result()
                flipkart_products = flipkart_future.result()
                
                all_products.extend(amazon_products)
                all_products.extend(flipkart_products)
        
        # Convert to DataFrame
        if not all_products:
            print("No products found!")
            return {}
            
        df = pd.DataFrame(all_products)
        
        # Create separate DataFrames for each price band
        band_dfs = {}
        for band in set(df['Price_Band'].unique()):  # Use actual bands found in data
            band_df = df[df['Price_Band'] == band].copy()
            if not band_df.empty:
                band_dfs[band] = band_df
        
        return band_dfs

    def print_report(self, search_terms):
        print("Scraping prices for:", ', '.join(search_terms))
        band_dfs = self.compare_prices(search_terms)
        
        if not band_dfs:
            print("No data to generate report!")
            return
        
        # Print results for each price band
        for band, df in band_dfs.items():
            print(f"\n--- Price Band: {band} ---")
            print(f"{'Platform':<15} {'Title':<50} {'Price':<12} {'Specifications'}")
            print("-" * 100)
            
            for idx, row in df.iterrows():
                platform = row['Platform']
                title = row['Title']
                price = f"₹{row['Price']:,.2f}"
                specs = row['Specifications']
                
                # Format specs as a string
                if isinstance(specs, dict):
                    specs = ', '.join([f"{key}: {value}" for key, value in specs.items()])
                else:
                    specs = "N/A"
                
                print(f"{platform:<15} {title:<50} {price:<12} {specs}")
                
        print("\n--- End of Report ---")

# Usage example
if __name__ == "__main__":
    scraper = EcommerceScraper()
    search_terms = ['iPhone 15', 'iPhone 14', 'Samsung S24', 'Samsung S23']
    scraper.print_report(search_terms)
