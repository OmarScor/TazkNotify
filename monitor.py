# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import random
import requests
import os

def send_telegram_notification(message):
    bot_token = os.environ['BOT_TOKEN']
    chat_id = os.environ['CHAT_ID']
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
    # تهيئة إعدادات المتصفح
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless")  # للتشغيل في الخلفية

    # تشغيل المتصفح
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), 
        options=chrome_options
    )
    
    try:
        while True:
            driver.get("https://tazkarti.com/#/matches")
            time.sleep(random.uniform(3, 5))
            
            if check_keywords_exists(driver):
                print("تم العثور على كلمة مفتاحية!")
                send_telegram_notification("🔥 تذاكر متاحة الآن! (تم العثور على Volley أو Available)")
                break
            else:
                print("لم يتم العثور على نتائج، إعادة المحاولة...")
                time.sleep(random.randint(30, 60))
                
    except Exception as e:
        print(f"حدث خطأ: {str(e)}")
        send_telegram_notification(f"⚠️ خطأ في النظام: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    monitor_matches()
