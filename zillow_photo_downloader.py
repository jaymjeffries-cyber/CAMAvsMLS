"""
Zillow Photo Downloader - Improved Version
Downloads property photos from Zillow for each address with robust zpid extraction
"""

import requests
from bs4 import BeautifulSoup
import re
import os
from urllib.parse import quote, urljoin
import time
import json

def create_photo_folder(output_folder="zillow_photos"):
    """Create folder for storing downloaded photos."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    return output_folder

def extract_zpid_from_direct_url(address, city, state, zip_code):
    """
    Build a direct Zillow URL from address and extract zpid from redirect.
    This is the PRIMARY method - most reliable!
    
    URL Template: https://www.zillow.com/homedetails/Address-City-State-Zip/
    Zillow will redirect to the correct property with zpid
    """
    if not address or not city or not zip_code:
        return None
    
    try:
        # Clean and format address parts
        address_clean = str(address).strip()
        city_clean = str(city).strip()
        state_clean = str(state).strip() if state else 'OH'
        zip_clean = str(zip_code).strip().split('-')[0]  # Remove ZIP+4 if present
        
        # Format for URL: remove special chars, replace spaces with hyphens
        address_formatted = re.sub(r'[^\w\s-]', '', address_clean)
        address_formatted = re.sub(r'\s+', '-', address_formatted)
        
        city_formatted = re.sub(r'[^\w\s-]', '', city_clean)
        city_formatted = re.sub(r'\s+', '-', city_formatted)
        
        # Build the direct URL
        direct_url = f"https://www.zillow.com/homedetails/{address_formatted}-{city_formatted}-{state_clean}-{zip_clean}/"
        
        # Headers to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        
        # Make request - Zillow will redirect to actual property page with zpid
        response = requests.get(direct_url, headers=headers, timeout=15, allow_redirects=True)
        
        if response.status_code == 200:
            # Check the final URL after redirect
            final_url = response.url
            
            # Extract zpid from URL: .../12345678_zpid/...
            zpid_match = re.search(r'/(\d{8,})_zpid/', final_url)
            if zpid_match:
                return zpid_match.group(1)
            
            # Also try to find zpid in page content as backup
            zpid_patterns = [
                r'"zpid":"(\d{8,})"',
                r'"zpid":(\d{8,})',
                r'data-zpid="(\d{8,})"',
            ]
            
            for pattern in zpid_patterns:
                match = re.search(pattern, response.text)
                if match:
                    return match.group(1)
        
    except Exception as e:
        pass
    
    return None

def extract_zpid_robust(address, city, state, zip_code, max_retries=2):
    """
    Extract zpid using direct URL method FIRST (most reliable).
    Falls back to search if direct method fails.
    """
    if not address or not city or not zip_code:
        return None
    
    # METHOD 1: Direct URL construction (BEST METHOD)
    zpid = extract_zpid_from_direct_url(address, city, state, zip_code)
    if zpid:
        return zpid
    
    # If direct method failed, try search as fallback
    # Clean inputs
    address_clean = str(address).strip()
    city_clean = str(city).strip()
    state_clean = str(state).strip() if state else 'OH'
    zip_clean = str(zip_code).strip().split('-')[0]
    
    # Create search query
    search_query = f"{address_clean} {city_clean} {state_clean} {zip_clean}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    for attempt in range(max_retries):
        try:
            # METHOD 2: Try Zillow's search
            encoded_query = quote(search_query)
            search_url = f"https://www.zillow.com/homes/{encoded_query}_rb/"
            
            response = requests.get(search_url, headers=headers, timeout=15, allow_redirects=True)
            
            if response.status_code == 200:
                content = response.text
                
                # Try multiple extraction patterns
                zpid_patterns = [
                    r'"zpid":"(\d{8,})"',
                    r'data-zpid="(\d{8,})"',
                    r'/homedetails/[^/]+/(\d{8,})_zpid/',
                    r'"propertyId":"(\d{8,})"',
                    r'(\d{8,})_zpid',
                ]
                
                for pattern in zpid_patterns:
                    matches = re.findall(pattern, content)
                    if matches:
                        return matches[0]
        
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(1)
    
    return None

def construct_photo_url(zpid, address, city, state, zip_code):
    """
    Construct the Zillow photo URL with mmlb=g,0 parameter.
    Format: https://www.zillow.com/homedetails/ADDRESS/ZPID_zpid/?mmlb=g,0
    """
    if not zpid:
        return None
    
    # Format address for URL
    address_clean = str(address).strip()
    city_clean = str(city).strip()
    state_clean = str(state).strip() if state else 'OH'
    zip_clean = str(zip_code).strip().split('-')[0]
    
    # Remove special characters and replace spaces with hyphens
    address_formatted = re.sub(r'[^\w\s-]', '', address_clean)
    address_formatted = re.sub(r'\s+', '-', address_formatted)
    
    city_formatted = re.sub(r'[^\w\s-]', '', city_clean)
    city_formatted = re.sub(r'\s+', '-', city_formatted)
    
    # Construct URL with photo parameter
    url_slug = f"{address_formatted}-{city_formatted}-{state_clean}-{zip_clean}"
    photo_url = f"https://www.zillow.com/homedetails/{url_slug}/{zpid}_zpid/?mmlb=g,0"
    
    return photo_url

def download_photo_from_url(photo_page_url, parcel_id, output_folder):
    """
    Download the main photo from a Zillow property page.
    The page with mmlb=g,0 shows the main photo.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    
    try:
        # Get the property page with photo view
        response = requests.get(photo_page_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for the main photo - try multiple methods
            photo_url = None
            
            # Method 1: Look for high-resolution images in picture elements
            for picture in soup.find_all('picture'):
                for img in picture.find_all('img'):
                    src = img.get('src', '')
                    if 'photos.zillowstatic.com' in src or 'ssl.cdn-redfin.com' in src:
                        photo_url = src
                        break
                if photo_url:
                    break
            
            # Method 2: Look for main image with specific classes
            if not photo_url:
                for img in soup.find_all('img'):
                    src = img.get('src', '')
                    alt = img.get('alt', '').lower()
                    if ('photos.zillowstatic.com' in src or 'ssl.cdn-redfin.com' in src) and ('photo' in alt or 'home' in alt):
                        photo_url = src
                        break
            
            # Method 3: Look for any large Zillow photo
            if not photo_url:
                for img in soup.find_all('img'):
                    src = img.get('src', '')
                    if 'photos.zillowstatic.com' in src:
                        # Prefer larger images
                        if any(size in src for size in ['1280x960', '1024x768', '800x600']):
                            photo_url = src
                            break
            
            # Method 4: Extract from JSON data
            if not photo_url:
                scripts = soup.find_all('script', type='application/json')
                for script in scripts:
                    try:
                        data = json.loads(script.string)
                        # Try to find image URLs in the JSON
                        photo_url = extract_photo_from_json(data)
                        if photo_url:
                            break
                    except:
                        pass
            
            # Download the photo
            if photo_url:
                # Clean the URL
                photo_url = photo_url.split('?')[0] if '?' in photo_url else photo_url
                
                photo_response = requests.get(photo_url, headers=headers, timeout=15)
                
                if photo_response.status_code == 200:
                    # Determine file extension
                    file_extension = '.jpg'
                    content_type = photo_response.headers.get('content-type', '')
                    if 'png' in content_type or '.png' in photo_url.lower():
                        file_extension = '.png'
                    elif 'webp' in content_type or '.webp' in photo_url.lower():
                        file_extension = '.webp'
                    
                    filename = f"{parcel_id}{file_extension}"
                    filepath = os.path.join(output_folder, filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(photo_response.content)
                    
                    return filepath
            
        return None
        
    except Exception as e:
        return None

def extract_photo_from_json(data, depth=0, max_depth=5):
    """Recursively search JSON for photo URLs."""
    if depth > max_depth or not isinstance(data, (dict, list)):
        return None
    
    if isinstance(data, dict):
        # Look for common photo URL keys
        for key in ['url', 'src', 'photoUrl', 'imageUrl', 'imgSrc']:
            if key in data:
                value = data[key]
                if isinstance(value, str) and 'photos.zillowstatic.com' in value:
                    return value
        
        # Recursively search nested structures
        for value in data.values():
            result = extract_photo_from_json(value, depth + 1, max_depth)
            if result:
                return result
    
    elif isinstance(data, list):
        for item in data:
            result = extract_photo_from_json(item, depth + 1, max_depth)
            if result:
                return result
    
    return None

def download_property_photo(parcel_id, address, city, state, zip_code, output_folder="zillow_photos"):
    """
    Main function to download a property photo from Zillow.
    Fully automatic - extracts zpid and downloads photo.
    """
    # Create output folder if needed
    create_photo_folder(output_folder)
    
    # Check if photo already exists
    for ext in ['.jpg', '.png', '.webp']:
        existing_file = os.path.join(output_folder, f"{parcel_id}{ext}")
        if os.path.exists(existing_file):
            return existing_file
    
    print(f"  📸 Downloading photo for parcel {parcel_id}...")
    
    # Step 1: Extract zpid from Zillow
    zpid = extract_zpid_robust(address, city, state, zip_code)
    if not zpid:
        print(f"  ⚠️  Could not find property on Zillow")
        return None
    
    print(f"  ✅ Found zpid: {zpid}")
    
    # Step 2: Construct photo URL with mmlb=g,0
    photo_page_url = construct_photo_url(zpid, address, city, state, zip_code)
    if not photo_page_url:
        print(f"  ⚠️  Could not construct photo URL")
        return None
    
    # Step 3: Download the photo
    filepath = download_photo_from_url(photo_page_url, parcel_id, output_folder)
    
    if filepath:
        print(f"  ✅ Photo saved: {filepath}")
        return filepath
    else:
        print(f"  ⚠️  Could not download photo")
        return None

def batch_download_photos(df, output_folder="zillow_photos", delay=3):
    """
    Download photos for all properties in a DataFrame.
    Uses direct URL construction for reliable zpid extraction.
    """
    photo_map = {}
    total = len(df)
    
    print(f"\n📸 Downloading {total} property photos from Zillow...")
    print(f"   Output folder: {output_folder}")
    print(f"   Delay between requests: {delay} seconds")
    print(f"   Method: Direct URL from address (most reliable)")
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
        if idx < total - 1:
            time.sleep(delay)
        
        print()
    
    print(f"✅ Downloaded {len(photo_map)} out of {total} photos")
    print(f"   Success rate: {len(photo_map)/total*100:.1f}%")
    print(f"   Photos saved in: {output_folder}/")
    print()
    
    return photo_map

if __name__ == "__main__":
    # Test the photo downloader
    print("🧪 Testing Zillow Photo Downloader\n")
    
    # Test with your example address
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
