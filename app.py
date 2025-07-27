import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_website(url):
    """
    Scrapes product names, prices, and ratings from the given URL.
    """
    
    # Send a request to fetch the web page's HTML
    try:
        response = requests.get(url)
        response.raise_for_status()  # This will check for any HTTP errors
    except requests.exceptions.RequestException as e:
        print(f"Could not fetch the URL: {e}")
        return None

    # Create a BeautifulSoup object to parse the HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all the articles that contain book information
    products = soup.find_all('article', class_='product_pod')
    
    product_list = []
    
    # Loop through each product found
    for product in products:
        try:
            # Extract name, price, and rating using their specific HTML tags and classes
            name = product.h3.a['title']
            price = product.find('p', class_='price_color').text
            rating_p = product.find('p', class_='star-rating')
            # The rating text is the second class name (e.g., "Five")
            rating = f"{rating_p['class'][1]} out of 5"
            
            # Add the extracted data to our list
            product_list.append({
                'Product Name': name,
                'Price': price,
                'Rating': rating
            })
        except (AttributeError, IndexError) as e:
            # Skip this product if any of the data points are missing
            print(f"Skipping a product due to missing data: {e}")
            continue
            
    return product_list

def save_data_to_csv(data, filename="products.csv"):
    """
    Saves the scraped data into a CSV file.
    """
    if not data:
        print("No data was scraped. CSV file not created.")
        return

    # Use pandas to create a DataFrame and save it as a CSV
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"Success! Data has been saved to {filename}")


# --- Main execution block ---
if __name__ == "__main__":
    target_url = 'http://books.toscrape.com/'
    scraped_data = scrape_website(target_url)
    
    if scraped_data:
        save_data_to_csv(scraped_data)