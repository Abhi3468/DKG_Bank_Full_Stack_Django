import requests
import json

s = requests.Session()

# 1. Get CSRF token
res = s.get("http://127.0.0.1:8000/")
csrf_token = s.cookies.get('csrftoken', '')
print("CSRF Token:", csrf_token)

# 2. Send OTP
headers = {
    "Content-Type": "application/json",
    "X-CSRFToken": csrf_token,
    "Referer": "http://127.0.0.1:8000/"
}
payload = {"username": "testuser"}
print("Sending OTP...")
res2 = s.post("http://127.0.0.1:8000/send-login-otp/", headers=headers, json=payload)
print("Send OTP Response:", res2.status_code, res2.text)

# We can't automatically get the OTP from the console here, but we can verify the session was set.
print("Cookies after Send OTP:", s.cookies.get_dict())
