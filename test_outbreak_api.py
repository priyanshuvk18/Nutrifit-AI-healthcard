import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_outbreak_api():
    print("Testing Outbreak API...")
    
    # -1. Register a test user
    print("\n-1. Registering test user...")
    import time
    timestamp = int(time.time())
    email = f"test_{timestamp}@example.com"
    password = "password123"
    
    try:
        reg_res = requests.post(f"{BASE_URL}/auth/register", json={
            "email": email,
            "password": password,
            "full_name": "Test User",
            "age": 30,
            "gender": "male",
            "height": 180,
            "weight": 75,
            "activity_level": "moderate",
            "goal": "maintenance"
        })
        if reg_res.status_code == 201:
            print(f"Registration Successful: {email}")
        else:
            print(f"Registration Failed (might exist): {reg_res.text}")
    except Exception as e:
        print(f"Registration Error: {e}")

    # 0. Login to get token
    print("\n0. Logging in...")
    try:
        login_res = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
        if login_res.status_code == 200:
            token = login_res.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            print("Login Successful!")
        else:
            print(f"Login Failed: {login_res.text}")
            print("Skipping authenticated tests...")
            headers = {}
    except Exception as e:
        print(f"Login Error: {e}")
        headers = {}
    
    # 1. Test POST report
    print("\n1. Testing POST /outbreak/report")
    report_data = {
        "location": "Mumbai",
        "latitude": 19.0760,
        "longitude": 72.8777,
        "disease_type": "Dengue",
        "symptoms": ["fever", "rash"],
        "severity": "moderate",
        "status": "verified"
    }
    
    try:
        if headers:
            response = requests.post(f"{BASE_URL}/outbreak/report", json=report_data, headers=headers)
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                print(f"Success! Report ID: {response.json().get('report_id')}")
            else:
                 print(f"Response: {response.text}")
        else:
            print("Skipping POST test due to missing token.")
        
    except Exception as e:
        print(f"Error: {e}")

    # 2. Test GET heatmap
    print("\n2. Testing GET /outbreak/heatmap")
    try:
        response = requests.get(f"{BASE_URL}/outbreak/heatmap")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"Success! Data Count: {len(response.json())}")
        else:
            print(f"Failed: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

    # 3. Test GET alerts
    print("\n3. Testing GET /outbreak/alerts")
    try:
        response = requests.get(f"{BASE_URL}/outbreak/alerts")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"Success! Alerts: {len(response.json())}")
        else:
            print(f"Failed: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_outbreak_api()
