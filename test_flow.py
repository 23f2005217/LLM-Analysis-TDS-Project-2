import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

def test_solve_endpoint():
    url = "http://localhost:7860/solve"
    
    payload = {
        "email": os.getenv("EMAIL", "your_email"),
        "secret": os.getenv("SECRET", "your_secret"),
        "url": "https://tds-llm-analysis.s-anand.net/demo"
    }
    
    print(f"Sending POST request to {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload)
        print(f"\nResponse Status Code: {response.status_code}")
        try:
            print(f"Response Body: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"Response Body: {response.text}")
            
        if response.status_code == 200:
            print("\nTest Passed: Server accepted the request and started the agent.")
        else:
            print("\nTest Failed: Server returned an error.")
            
    except requests.exceptions.ConnectionError:
        print(f"\nConnection Error: Could not connect to {url}. Is the server running?")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    test_solve_endpoint()
