import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# تحميل الحسابات
def load_accounts(file_path="accounts.txt"):
    with open(file_path, "r") as f:
        return [line.strip().split(":") for line in f.readlines()]

# متابعة الصفحة
def follow_page(email, password, page_url):
    options = Options()
    options.add_argument("--headless")  # حذف السطر ده لو عاوز تشوف المتصفح
    options.add_argument("--disable-notifications")
    options.add_argument("--lang=ar")  # ضبط اللغة لو الحسابات بالعربي

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.facebook.com/login")

    try:
        time.sleep(2)
        driver.find_element(By.ID, "email").send_keys(email)
        driver.find_element(By.ID, "pass").send_keys(password)
        driver.find_element(By.NAME, "login").click()

        time.sleep(5)
        driver.get(page_url)
        time.sleep(6)

        try:
            follow_btn = driver.find_element(By.XPATH, "//div[@aria-label='متابعة' or @aria-label='Follow']")
            follow_btn.click()
            print(f"[✔] {email} تابع الصفحة.")
        except:
            print(f"[!] {email} لم يعثر على زر المتابعة أو يتابع بالفعل.")
    except Exception as e:
        print(f"[✘] {email} فشل: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("❌ استخدم: python follow_script.py <page_link> <count>")
        sys.exit(1)

    page_url = sys.argv[1]
    count = int(sys.argv[2])
    accounts = load_accounts()[:count]

    for email, password in accounts:
        follow_page(email, password, page_url)
        time.sleep(8)
