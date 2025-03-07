# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import requests

def send_telegram_notification(message):
    bot_token = "8112971939:AAEyVsTG4xW94QnOmX6z1viv6bAXltNzKKE"
    chat_id = "-1002362370692"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {"chat_id": chat_id, "text": message}
    requests.post(url, params=params)

def check_keywords_exists(driver):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, 
                "//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'epl') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'available')]"
            ))
        )
        return True
    except:
        return False

def monitor_matches():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), 
        options=options
    )
    driver.get("https://tazkarti.com/#/matches")
    
    try:
        while True:
            driver.refresh()  # تحديث الصفحة هنا
            print(f"تم تحديث الصفحة في: {time.strftime('%H:%M:%S')}")
            time.sleep(random.uniform(8, 15))
            
            if check_keywords_exists(driver):
                print("تم العثور على كلمة مفتاحية!")
                send_telegram_notification("🔥 تذاكر متاحة الآن!")
                break
            else:
                print("لم يتم العثور على نتائج، إعادة المحاولة...")
                time.sleep(random.randint(16, 20))
                
    except Exception as e:
        print(f"حدث خطأ: {str(e)}")
        send_telegram_notification(f"⚠️ خطأ في النظام: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    monitor_matches()