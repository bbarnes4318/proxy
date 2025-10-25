"""
Simple test script to verify the proxy connection works
"""
import requests

# IPRoyal residential proxy configuration
PROXY_HOST = "geo.iproyal.com"
PROXY_PORT = 12321
PROXY_USER = "TmwjTsVQHgTiXElI"
PROXY_PASS = "Topproducer2026_country-us_city-lasvegas_session-QNpU9Vlz_lifetime-168h"

# Construct proxy URL
proxy_url = f'http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}'

proxies = {
    'http': proxy_url,
    'https': proxy_url
}

def test_connection():
    """Test the proxy connection"""
    print("=" * 60)
    print("Testing Proxy Connection...")
    print("=" * 60)
    
    try:
        # Test URL - returns your public IP
        url = 'https://ipv4.icanhazip.com'
        
        print(f"\nConnecting to {url} through proxy...")
        print(f"Proxy: {PROXY_HOST}:{PROXY_PORT}")
        
        response = requests.get(url, proxies=proxies, timeout=10)
        response.raise_for_status()
        
        ip_address = response.text.strip()
        
        print(f"\nSUCCESS!")
        print(f"Your proxy IP address: {ip_address}")
        print(f"Status code: {response.status_code}")
        print(f"\nProxy is working correctly!")
        
        return True
        
    except requests.exceptions.ProxyError as e:
        print(f"\nPROXY ERROR:")
        print(f"Could not connect to the proxy server.")
        print(f"Details: {e}")
        return False
        
    except requests.exceptions.RequestException as e:
        print(f"\nREQUEST ERROR:")
        print(f"An error occurred: {e}")
        return False
    
    finally:
        print("=" * 60)

if __name__ == "__main__":
    test_connection()

