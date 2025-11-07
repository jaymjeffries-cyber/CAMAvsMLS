"""
Quick Test - CAMA Login with Correct URL
Tests login to https://iasworld.starkcountyohio.gov/iasworld/Main/Login.aspx
"""

import requests
from bs4 import BeautifulSoup

def test_login_page_access():
    """Test if we can access the login page."""
    print("=" * 80)
    print("Testing CAMA Login Page Access")
    print("=" * 80)
    
    login_url = "https://iasworld.starkcountyohio.gov/iasworld/Main/Login.aspx"
    
    try:
        print(f"\n🔗 Accessing: {login_url}")
        response = requests.get(login_url, timeout=10)
        
        print(f"✅ Status Code: {response.status_code}")
        print(f"✅ Final URL: {response.url}")
        
        if response.status_code == 200:
            print("\n✅ Login page is accessible!")
            
            # Parse the form
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the login form
            forms = soup.find_all('form')
            print(f"\n📋 Found {len(forms)} form(s)")
            
            if forms:
                form = forms[0]
                
                # Find input fields
                inputs = form.find_all('input')
                print(f"\n🔍 Form Fields:")
                
                username_field = None
                password_field = None
                
                for inp in inputs:
                    field_name = inp.get('name', 'No name')
                    field_type = inp.get('type', 'text')
                    field_id = inp.get('id', 'No ID')
                    
                    if field_type != 'hidden':
                        print(f"  • {field_name} (type: {field_type}, id: {field_id})")
                    
                    # Identify fields
                    if field_type == 'password':
                        password_field = field_name
                        print(f"    ⭐ This is the PASSWORD field")
                    elif field_type == 'text':
                        field_lower = field_name.lower()
                        if 'user' in field_lower or 'login' in field_lower:
                            username_field = field_name
                            print(f"    ⭐ This is likely the USERNAME field")
                
                print("\n" + "=" * 80)
                print("CONFIGURATION TO USE:")
                print("=" * 80)
                
                if username_field and password_field:
                    print(f"\n✅ Found login fields!\n")
                    print(f"Login URL: {login_url}")
                    print(f"Username field: {username_field}")
                    print(f"Password field: {password_field}")
                    
                    print(f"\nUpdate cama_windowid_extractor.py line ~52 with:")
                    print(f"  login_data['{username_field}'] = username")
                    print(f"  login_data['{password_field}'] = password")
                else:
                    print("\n⚠️  Could not clearly identify fields")
                    print("Run cama_login_diagnostic.py for more details")
            
            return True
        else:
            print(f"❌ Could not access login page (Status: {response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_with_credentials():
    """Test login with credentials (if available)."""
    print("\n" + "=" * 80)
    print("Test Login with Credentials")
    print("=" * 80)
    
    # Try to load credentials
    try:
        with open('cama_credentials.txt', 'r') as f:
            credentials = {}
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    credentials[key.lower()] = value
            
            if 'username' in credentials and 'password' in credentials:
                print(f"\n✅ Found credentials file")
                print(f"   Username: {credentials['username']}")
                print(f"   Password: {'*' * len(credentials['password'])}")
                
                # Import the extractor
                try:
                    from cama_windowid_extractor import extract_window_id_with_login
                    
                    print(f"\n🔐 Testing login...")
                    window_id = extract_window_id_with_login(
                        credentials['username'],
                        credentials['password']
                    )
                    
                    if window_id:
                        print(f"\n✅ SUCCESS! WindowId: {window_id}")
                        return True
                    else:
                        print(f"\n❌ Login test failed")
                        return False
                        
                except ImportError:
                    print("\n⚠️  Could not import extractor module")
                    return False
            else:
                print("\n⚠️  Credentials file incomplete")
                return False
                
    except FileNotFoundError:
        print("\n⚠️  No credentials file found (cama_credentials.txt)")
        print("   Create one to test login functionality")
        return False


if __name__ == "__main__":
    print("\n🧪 CAMA Login Quick Test\n")
    
    # Test 1: Access login page
    can_access = test_login_page_access()
    
    if can_access:
        print("\n" + "=" * 80)
        input("\nPress Enter to test login with credentials (if available)...")
        
        # Test 2: Try login if credentials available
        test_with_credentials()
    
    print("\n" + "=" * 80)
    print("Test Complete!")
    print("=" * 80)
    print("\nNext steps:")
    print("1. Update the field names in cama_windowid_extractor.py")
    print("2. Create cama_credentials.txt with your login info")
    print("3. Run your main script to test end-to-end")
    print()
