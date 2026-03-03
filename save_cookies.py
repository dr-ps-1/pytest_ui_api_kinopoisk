import pickle
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config import Config

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--lang=ru-RU")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options)
driver.maximize_window()

try:
    driver.get(Config.UI_BASE_URL)
    print(
        "Открыта главная страница."
        "Пожалуйста,выполните вход вручную и пройдите капчу, "
        "если она появится.")
    input("После успешного входа нажмите Enter для сохранения куки...")

    with open("cookies.pkl", "wb") as f:
        pickle.dump(driver.get_cookies(), f)
    print("Куки сохранены в файл cookies.pkl")
finally:
    driver.quit()
