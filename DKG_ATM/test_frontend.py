from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

def test_frontend():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://127.0.0.1:8000/")
    
    try:
        # Wait for page to load
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "loginForm"))
        )
        print("Page loaded.")
        
        # Click OTP tab
        otp_tab = driver.find_element(By.XPATH, "//div[contains(text(), 'OTP')]")
        otp_tab.click()
        print("Clicked OTP tab.")
        
        # Check if OTP field is visible
        otp_field = driver.find_element(By.ID, "otpField")
        if otp_field.is_displayed():
            print("OTP field is visible.")
        else:
            print("ERROR: OTP field is NOT visible.")
            
        password_field = driver.find_element(By.ID, "passwordField")
        if not password_field.is_displayed():
            print("Password field is hidden.")
        else:
            print("ERROR: Password field is STILL visible.")
            
        # Enter username
        driver.find_element(By.ID, "username").send_keys("testuser")
        print("Entered username.")
        
        # Click Send OTP
        send_otp_btn = driver.find_element(By.ID, "sendOtpBtn")
        send_otp_btn.click()
        print("Clicked Send OTP.")
        
        # Check for success message
        success_div = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, "loginSuccess"))
        )
        print("Success message displayed:", success_div.text)
        
        # Check console logs
        logs = driver.get_log('browser')
        if logs:
            print("Browser logs:")
            for log in logs:
                print(log)
        else:
            print("No browser console errors.")
            
    except Exception as e:
        print(f"Test failed: {e}")
        logs = driver.get_log('browser')
        for log in logs:
            print(log)
            
    finally:
        driver.quit()

if __name__ == "__main__":
    test_frontend()
