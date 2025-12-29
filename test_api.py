import requests
import json

def test_login():
    url = "http://127.0.0.1:8000/api/auth/login/"
    payload = {
        "username": "admin",
        "password": "admin"
    }
    
    print(f"Testing URL: {url}")
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:200]}") # Print first 200 chars
        
        if response.status_code == 200:
            print("✅ Login API is working correctly!")
        else:
            print("❌ Login API returned an error.")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Refused. Is the server running?")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_login()
