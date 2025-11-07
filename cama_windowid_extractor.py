"""
CAMA WindowId Extractor
Automatically retrieves a fresh windowId from the Stark County CAMA system
"""

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse, parse_qs

def extract_window_id_simple(parcel_id="204522"):
    """
    Try to extract windowId without login by searching for a property.
    This often works because property search is usually public.
    
    Args:
        parcel_id: A valid parcel ID to search for (default is a test parcel)
    
    Returns:
        str: The windowId if found, None otherwise
    """
    try:
        print("🔍 Attempting to extract windowId without login...")
        
        session = requests.Session()
        base_url = "https://iasworld.starkcountyohio.gov/iasworld/"
        
        # First, get the main page to establish session
        response = session.get(base_url)
        
        # Try to search for a property (this might work without login)
        search_url = f"{base_url}PropertySearch.aspx"
        
        # Get the search page
        response = session.get(search_url)
        
        if response.status_code == 200:
            # Look for any windowId in the page or cookies
            window_id_match = re.search(r'windowId[=:](\d{15,20})', response.text)
            if window_id_match:
                window_id = window_id_match.group(1)
                print(f"✅ Found windowId: {window_id}")
                return window_id
        
        print("⚠️  Could not extract windowId without login")
        return None
        
    except Exception as e:
        print(f"⚠️  Error extracting windowId: {e}")
        return None


def extract_window_id_with_login(username, password, parcel_id="204522"):
    """
    Extract windowId by logging into the CAMA system.
    
    Args:
        username: Your CAMA username
        password: Your CAMA password  
        parcel_id: A valid parcel ID to search for
    
    Returns:
        str: The windowId if found, None otherwise
    """
    try:
        print("🔐 Logging into CAMA system...")
        
        session = requests.Session()
        base_url = "https://iasworld.starkcountyohio.gov/iasworld/"
        
        # Get the login page
        login_url = f"{base_url}Login.aspx"
        response = session.get(login_url)
        
        if response.status_code != 200:
            print(f"❌ Could not reach login page (Status: {response.status_code})")
            return None
        
        # Parse the page to get any required form fields
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Build login payload - adjust these field names based on actual form
        login_data = {
            'username': username,
            'password': password,
        }
        
        # Add any hidden form fields (like __VIEWSTATE, __EVENTVALIDATION for ASP.NET)
        for hidden in soup.find_all('input', type='hidden'):
            if hidden.get('name') and hidden.get('value'):
                login_data[hidden['name']] = hidden['value']
        
        # Submit login
        response = session.post(login_url, data=login_data)
        
        if 'login' in response.url.lower() or response.status_code != 200:
            print("❌ Login failed - check credentials")
            return None
        
        print("✅ Login successful")
        
        # Now search for a property to get the windowId
        print(f"🔍 Searching for property {parcel_id}...")
        
        search_url = f"{base_url}PropertySearch.aspx"
        response = session.get(search_url)
        
        # Look for windowId in the page content, URLs, or form actions
        window_id = None
        
        # Method 1: Check page content
        window_id_match = re.search(r'windowId[=:](\d{15,20})', response.text)
        if window_id_match:
            window_id = window_id_match.group(1)
        
        # Method 2: Check all links on the page
        if not window_id:
            soup = BeautifulSoup(response.content, 'html.parser')
            for link in soup.find_all('a', href=True):
                if 'windowId=' in link['href']:
                    window_id_match = re.search(r'windowId=(\d{15,20})', link['href'])
                    if window_id_match:
                        window_id = window_id_match.group(1)
                        break
        
        # Method 3: Try to access a specific property page
        if not window_id:
            # This URL format might trigger a redirect with windowId
            property_url = f"{base_url}Maintain/Transact.aspx?txtMaskedPin={parcel_id}"
            response = session.get(property_url)
            
            # Check the final URL after any redirects
            if 'windowId=' in response.url:
                parsed = urlparse(response.url)
                params = parse_qs(parsed.query)
                if 'windowId' in params:
                    window_id = params['windowId'][0]
        
        if window_id:
            print(f"✅ Found windowId: {window_id}")
            return window_id
        else:
            print("⚠️  Logged in successfully but could not find windowId")
            return None
            
    except Exception as e:
        print(f"❌ Error during login extraction: {e}")
        return None


def get_window_id(username=None, password=None, fallback_id=None):
    """
    Main function to get a windowId. Tries multiple methods.
    
    Args:
        username: CAMA username (optional)
        password: CAMA password (optional)
        fallback_id: WindowId to use if extraction fails
    
    Returns:
        str: A valid windowId
    """
    print("=" * 80)
    print("CAMA WindowId Extraction")
    print("=" * 80)
    
    # Method 1: Try without login first (public access)
    window_id = extract_window_id_simple()
    
    # Method 2: If that fails and credentials provided, try with login
    if not window_id and username and password:
        window_id = extract_window_id_with_login(username, password)
    
    # Method 3: Use fallback if provided
    if not window_id and fallback_id:
        print(f"ℹ️  Using fallback windowId: {fallback_id}")
        window_id = fallback_id
    
    # If all methods failed
    if not window_id:
        print("=" * 80)
        print("⚠️  COULD NOT EXTRACT WINDOWID AUTOMATICALLY")
        print("=" * 80)
        print("Please manually get windowId from CAMA website:")
        print("1. Go to https://iasworld.starkcountyohio.gov/iasworld/")
        print("2. Search for any property")
        print("3. Copy the windowId from the URL")
        print("4. Update the WINDOW_ID variable in the script")
        print("=" * 80)
        return None
    
    print("=" * 80)
    print(f"✅ WindowId acquired: {window_id}")
    print("=" * 80)
    return window_id


if __name__ == "__main__":
    # Test the extraction
    print("Testing windowId extraction...\n")
    
    # Test without credentials
    window_id = get_window_id(fallback_id="638981240146803746")
    
    if window_id:
        print(f"\n✅ Success! WindowId: {window_id}")
        print(f"\nExample URL:")
        print(f"https://iasworld.starkcountyohio.gov/iasworld/Maintain/Transact.aspx?txtMaskedPin=204522&windowId={window_id}")
    else:
        print("\n❌ Extraction failed. Manual entry required.")
