"""
Script to reset/wipe a gateway with the server.
Uses only built-in Python libraries (no dependencies).
"""

import sys
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from urllib.parse import urlencode
import config

# Configuration from config.py
GATEWAY_MAC = config.GATEWAY_MAC
WIPE_ENDPOINT = config.WIPE_ENDPOINT
TIMEOUT = 10
ONLY_DB = True

def main():
    """
    Main function to reset/wipe the gateway.
    """
    print(f"Starting gateway reset for {GATEWAY_MAC}...")
    
    try:
        # Build the URL with query parameters
        url = f"{WIPE_ENDPOINT}?macAddress={GATEWAY_MAC};onlydb={ONLY_DB}"
        
        # Make the HTTP GET request
        with urlopen(url, timeout=TIMEOUT) as response:
            status_code = response.getcode()
            
            if status_code in [200, 201]:
                print("Wipe successful")
                print(f"Response: {response.read().decode('utf-8')}")
                sys.exit(0)
            else:
                print(f"Wipe failed: {status_code}")
                sys.exit(1)
                
    except HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        sys.exit(1)
    except URLError as e:
        print(f"URL Error: {e.reason}")
        sys.exit(1)
    except Exception as e:
        print(f"Wipe request failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
