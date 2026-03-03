import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Tuple


class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    @allure.step("Найти элемент {locator}")
    def find_element(self, locator: Tuple[str, str], timeout: int = 20):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    @allure.step("Кликнуть на элемент {locator}")
    def click(self, locator: Tuple[str, str]):
        self.find_element(locator).click()

    @allure.step("Ввести текст '{text}' в элемент {locator}")
    def send_keys(self, locator: Tuple[str, str], text: str):
        self.find_element(locator).send_keys(text)

    @allure.step("Получить текущий URL")
    def get_current_url(self) -> str:
        return self.driver.current_url


class MainPage(BasePage):
    SEARCH_INPUT = (By.CSS_SELECTOR, 'input[name="kp_query"]')
    FILTER_BUTTON = (By.CSS_SELECTOR, 'a[href="/s/"]')

    @allure.step("Проверить, что поле поиска отображается")
    def is_search_displayed(self) -> bool:
        return self.find_element(self.SEARCH_INPUT).is_displayed()

    @allure.step("Кликнуть на кнопку фильтра")
    def click_filter(self) -> None:
        self.click(self.FILTER_BUTTON)


class SearchResultsPage(BasePage):
    SUGGESTIONS = (By.CSS_SELECTOR, '#suggest-container')
    FIRST_RESULT = (
        By.CSS_SELECTOR, '[data-tid="search-result-item"]:first-child')
    NOT_FOUND_MESSAGE = (
        By.XPATH, '//*[contains(text(), "ничего не найдено")]')

    @allure.step("Дождаться появления подсказок")
    def wait_for_suggestions(self) -> bool:
        return bool(self.find_element(self.SUGGESTIONS))

    @allure.step("Получить текст первого результата")
    def get_first_result_text(self) -> str:
        return self.find_element(self.FIRST_RESULT).text

    @allure.step(
            "Проверить, что отображается сообщение об отсутствии результатов")
    def is_not_found_message_displayed(self) -> bool:
        return self.find_element(self.NOT_FOUND_MESSAGE).is_displayed()
