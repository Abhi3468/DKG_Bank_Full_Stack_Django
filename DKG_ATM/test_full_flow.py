import requests
import json

s = requests.Session()

res = s.get("http://127.0.0.1:8000/")
csrf_token = s.cookies.get('csrftoken', '')

headers = {
    "Content-Type": "application/json",
    "X-CSRFToken": csrf_token,
    "Referer": "http://127.0.0.1:8000/"
}
payload = {
    "username": "testuser"
}
print("Sending OTP Request...")
res2 = s.post("http://127.0.0.1:8000/send-login-otp/", headers=headers, json=payload)
print("Send OTP Response:", res2.status_code, res2.text)

if res2.status_code == 200:
    data = res2.json()
    otp = data.get('otp')
    print("Received OTP:", otp)
    
    verify_payload = {
        "username": "testuser",
        "method": "otp",
        "otp": otp
    }
    print("Verifying OTP...")
    res3 = s.post("http://127.0.0.1:8000/login/", headers=headers, json=verify_payload)
    print("Verify Response:", res3.status_code, res3.text)
