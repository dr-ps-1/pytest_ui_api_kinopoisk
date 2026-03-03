import pickle
import os
import sys
import time
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from fake_useragent import UserAgent
from config import Config
from api import KinopoiskAPI

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

COOKIES_FILE = "cookies.pkl"


def handle_captcha(driver):
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located
            ((By.CSS_SELECTOR, "iframe[src*='captcha']"))
        )
        print("\n--- ОБНАРУЖЕНА КАПЧА ---")
        print("Пожалуйста, решите её вручную в течение 20 секунд.")
        time.sleep(20)
        print("Продолжаем выполнение теста...")
    except Exception:
        pass


def close_popups(driver):
    print("Проверяем наличие всплывающих окон...")
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert"))
        )
        print("Окно 'alert' обнаружено, ищем кнопку 'Остаться'...")
        stay_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "stay-button"))
        )
        stay_button.click()
        print("Кнопка 'Остаться' нажата")
        WebDriverWait(driver, 5).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "alert"))
        )
        print("Окно закрылось")
    except Exception as e:
        print(f"Окно не обнаружено или не удалось закрыть: {e}")
    popup_selectors = [
        (By.CSS_SELECTOR, "button[data-tid='accept-cookie']"),
        (By.XPATH, "//button[contains(text(), 'Принять')]"),
        (By.XPATH, "//button[contains(text(), 'ОК')]"),
        (By.CSS_SELECTOR, "button[aria-label='Закрыть']"),
        (By.CSS_SELECTOR, "svg[aria-label='Закрыть']"),
        (By.XPATH, "//button[contains(text(), 'Нет, спасибо')]"),
        (By.XPATH, "//button[contains(text(), 'Да')]"),
        (By.XPATH, "//button[contains(text(), 'Нет')]"),
    ]
    for by, selector in popup_selectors:
        try:
            element = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((by, selector))
            )
            element.click()
            print(f"Закрыто всплывающее окно: {selector}")
            time.sleep(0.5)
        except Exception:
            pass


@pytest.fixture
def browser():
    with allure.step("Открыть браузер со stealth-настройками"):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        ua = UserAgent()
        user_agent = ua.random
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument("--lang=ru-RU")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        stealth(driver,
                languages=["ru-RU", "ru"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

        driver.implicitly_wait(5)
        driver.maximize_window()

        driver.get(Config.UI_BASE_URL)

        if os.path.exists(COOKIES_FILE):
            with allure.step("Загрузить сохранённые куки авторизации"):
                with open(COOKIES_FILE, "rb") as f:
                    cookies = pickle.load(f)
                    for cookie in cookies:
                        if 'domain' in cookie:
                            del cookie['domain']
                        driver.add_cookie(cookie)
                driver.refresh()
                time.sleep(3)
                print(f"Загружено {len(cookies)} кук")
        else:
            print("Файл cookies.pkl не найден, продолжаем без авторизации")

        close_popups(driver)

        yield driver

    with allure.step("Закрыть браузер"):
        driver.quit()


@pytest.fixture
def api_client():
    return KinopoiskAPI(base_url=Config.API_BASE_URL, api_key=Config.API_KEY)
