import requests

def connect_to_url(url):
    try:
        # Make a GET request to the specified URL
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print(f"Successfully connected to {url}")
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Headers: {response.headers}")
            print(f"Response Content:\n{response.text[:500]}...")  # Print first 500 characters of content
        else:
            print(f"Failed to connect to {url}")
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Content:\n{response.text}")
    except requests.exceptions.RequestException as e:
        # Handle any exceptions (network issues, invalid URL, etc.)
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    with open('mock_mac.txt') as file:
        mac = file.read()
    url = f"http://localhost:3015/register?macAddress={mac}"
    # Connect to the URL
    connect_to_url(url)
