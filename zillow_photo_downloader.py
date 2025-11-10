"""
Zillow Photo Downloader
Downloads property photos from Zillow for each address
"""

import requests
from bs4 import BeautifulSoup
import re
import os
from urllib.parse import quote
import time

def create_photo_folder(output_folder="zillow_photos"):
    """Create folder for storing downloaded photos."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    return output_folder

def format_zillow_search_url(address, city, state, zip_code):
    """
    Create a Zillow search URL from address components.
    Returns: Search URL
    """
    if not address or not city or not zip_code:
        return None
    
    # Clean components
    address_clean = str(address).strip()
    city_clean = str(city).strip()
    zip_clean = str(zip_code).strip().split('-')[0]
    
    # Create search query
    search_query = f"{address_clean}, {city_clean}, OH {zip_clean}"
    encoded_query = quote(search_query)
    
    return f"https://www.zillow.com/homes/{encoded_query}_rb/"

def extract_zpid_from_search(search_url, max_retries=2):
    """
    Try to extract zpid from Zillow search results.
    Returns: zpid string or None
    """
    if not search_url:
        return None
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.get(search_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                # Method 1: Look for zpid in the page content
                zpid_match = re.search(r'"zpid":"(\d+)"', response.text)
                if zpid_match:
                    return zpid_match.group(1)
                
                # Method 2: Look for zpid in data attributes
                zpid_match = re.search(r'data-zpid="(\d+)"', response.text)
                if zpid_match:
                    return zpid_match.group(1)
                
                # Method 3: Look for zpid in links
                zpid_match = re.search(r'/homedetails/[^/]+/(\d+)_zpid/', response.text)
                if zpid_match:
                    return zpid_match.group(1)
            
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(1)  # Wait before retry
            else:
                print(f"  ⚠️  Could not extract zpid: {str(e)[:50]}")
    
    return None

def construct_photo_url(zpid, address, city, state, zip_code):
    """
    Construct the Zillow photo URL.
    Format: https://www.zillow.com/homedetails/ADDRESS/ZPID_zpid/?mmlb=g,0
    """
    if not zpid:
        return None
    
    # Format address for URL
    address_clean = str(address).strip()
    city_clean = str(city).strip()
    zip_clean = str(zip_code).strip().split('-')[0]
    
    # Remove special characters and replace spaces with hyphens
    address_formatted = re.sub(r'[^\w\s-]', '', address_clean)
    address_formatted = re.sub(r'\s+', '-', address_formatted)
    
    city_formatted = re.sub(r'[^\w\s-]', '', city_clean)
    city_formatted = re.sub(r'\s+', '-', city_formatted)
    
    # Construct URL with photo parameter
    url_slug = f"{address_formatted}-{city_formatted}-OH-{zip_clean}"
    photo_url = f"https://www.zillow.com/homedetails/{url_slug}/{zpid}_zpid/?mmlb=g,0"
    
    return photo_url

def download_photo_from_url(photo_page_url, parcel_id, output_folder):
    """
    Download the main photo from a Zillow property page.
    The page with mmlb=g,0 shows the main photo.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    
    try:
        # Get the property page with photo view
        response = requests.get(photo_page_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for the main photo - Zillow uses various selectors
            photo_url = None
            
            # Method 1: Look for photo in picture elements
            picture = soup.find('picture', class_=re.compile('photo'))
            if picture:
                img = picture.find('img')
                if img and img.get('src'):
                    photo_url = img['src']
            
            # Method 2: Look for data-image-url or similar attributes
            if not photo_url:
                img = soup.find('img', attrs={'data-image-url': True})
                if img:
                    photo_url = img['data-image-url']
            
            # Method 3: Look for main listing photo
            if not photo_url:
                img = soup.find('img', class_=re.compile('listing-photo'))
                if img and img.get('src'):
                    photo_url = img['src']
            
            # Method 4: Look for any large image
            if not photo_url:
                for img in soup.find_all('img'):
                    src = img.get('src', '')
                    if 'photos.zillowstatic.com' in src and '1280x960' in src:
                        photo_url = src
                        break
            
            # Download the photo
            if photo_url:
                # Clean the URL (remove query parameters that might cause issues)
                photo_url = photo_url.split('?')[0] if '?' in photo_url else photo_url
                
                photo_response = requests.get(photo_url, headers=headers, timeout=10)
                
                if photo_response.status_code == 200:
                    # Save photo with parcel ID as filename
                    file_extension = '.jpg'
                    if '.png' in photo_url.lower():
                        file_extension = '.png'
                    elif '.webp' in photo_url.lower():
                        file_extension = '.webp'
                    
                    filename = f"{parcel_id}{file_extension}"
                    filepath = os.path.join(output_folder, filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(photo_response.content)
                    
                    return filepath
            
        return None
        
    except Exception as e:
        print(f"  ⚠️  Error downloading photo: {str(e)[:50]}")
        return None

def download_property_photo(parcel_id, address, city, state, zip_code, output_folder="zillow_photos"):
    """
    Main function to download a property photo from Zillow.
    
    Args:
        parcel_id: Property parcel ID (for filename)
        address: Street address
        city: City name
        state: State (OH)
        zip_code: ZIP code
        output_folder: Folder to save photos
    
    Returns:
        str: Path to downloaded photo, or None if failed
    """
    # Create output folder if needed
    create_photo_folder(output_folder)
    
    # Check if photo already exists
    for ext in ['.jpg', '.png', '.webp']:
        existing_file = os.path.join(output_folder, f"{parcel_id}{ext}")
        if os.path.exists(existing_file):
            return existing_file
    
    print(f"  📸 Downloading photo for parcel {parcel_id}...")
    
    # Step 1: Create search URL
    search_url = format_zillow_search_url(address, city, state, zip_code)
    if not search_url:
        print(f"  ⚠️  Could not create search URL")
        return None
    
    # Step 2: Extract zpid from search results
    zpid = extract_zpid_from_search(search_url)
    if not zpid:
        print(f"  ⚠️  Could not find property on Zillow")
        return None
    
    print(f"  ✅ Found zpid: {zpid}")
    
    # Step 3: Construct photo URL
    photo_page_url = construct_photo_url(zpid, address, city, state, zip_code)
    if not photo_page_url:
        print(f"  ⚠️  Could not construct photo URL")
        return None
    
    # Step 4: Download the photo
    filepath = download_photo_from_url(photo_page_url, parcel_id, output_folder)
    
    if filepath:
        print(f"  ✅ Photo saved: {filepath}")
        return filepath
    else:
        print(f"  ⚠️  Could not download photo")
        return None

def batch_download_photos(df, output_folder="zillow_photos", delay=2):
    """
    Download photos for all properties in a DataFrame.
    
    Args:
        df: DataFrame with columns: Parcel_ID, Address, City, State, Zip
        output_folder: Folder to save photos
        delay: Seconds to wait between downloads (to be respectful to Zillow)
    
    Returns:
        dict: Mapping of parcel_id to photo filepath
    """
    photo_map = {}
    total = len(df)
    
    print(f"\n📸 Downloading {total} property photos from Zillow...")
    print(f"   Output folder: {output_folder}")
    print(f"   Delay between requests: {delay} seconds")
    print()
    
    for idx, row in df.iterrows():
        parcel_id = row.get('Parcel_ID')
        address = row.get('Address')
        city = row.get('City')
        state = row.get('State', 'OH')
        zip_code = row.get('Zip')
        
        print(f"[{idx + 1}/{total}] {address}, {city}")
        
        filepath = download_property_photo(
            parcel_id, address, city, state, zip_code, output_folder
        )
        
        if filepath:
            photo_map[parcel_id] = filepath
        
        # Be respectful - wait between requests
        if idx < total - 1:  # Don't wait after the last one
            time.sleep(delay)
        
        print()
    
    print(f"✅ Downloaded {len(photo_map)} out of {total} photos")
    print(f"   Photos saved in: {output_folder}/")
    print()
    
    return photo_map

if __name__ == "__main__":
    # Test the photo downloader
    print("🧪 Testing Zillow Photo Downloader\n")
    
    # Test with a sample address
    test_address = "1118 Raff Rd SW"
    test_city = "Canton"
    test_state = "OH"
    test_zip = "44710"
    test_parcel = "TEST123"
    
    print(f"Testing with: {test_address}, {test_city}, {test_state} {test_zip}\n")
    
    result = download_property_photo(
        test_parcel, test_address, test_city, test_state, test_zip
    )
    
    if result:
        print(f"\n✅ Success! Photo saved to: {result}")
    else:
        print(f"\n❌ Could not download photo")
