import allure
import pytest
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import handle_captcha, close_popups
from pages import MainPage, SearchResultsPage
from config import Config

SEARCH_QUERY = "Мастер"
INVALID_QUERY = "несуществующийфильм12345"


@pytest.mark.ui
@allure.story("UI: Поиск на главной")
class TestUISearch:

    @allure.title("Проверка отображения поля поиска на главной странице")
    def test_search_field_displayed(self, browser):
        browser.get(Config.UI_BASE_URL)
        handle_captcha(browser)
        close_popups(browser)
        main_page = MainPage(browser)
        WebDriverWait(browser, 30).until(
            EC.visibility_of_element_located(main_page.SEARCH_INPUT)
        )
        assert main_page.is_search_displayed()

    @allure.title(
            "Клик по кнопке фильтра открывает страницу расширенного поиска")
    def test_filter_button_click(self, browser):
        browser.get(Config.UI_BASE_URL)
        handle_captcha(browser)
        close_popups(browser)
        main_page = MainPage(browser)
        WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable(main_page.FILTER_BUTTON)
        )
        main_page.click_filter()
        WebDriverWait(browser, 15).until(
            lambda d: "/s/" in d.current_url
        )
        assert "/s/" in browser.current_url

    @allure.title("При вводе символов в поле поиска появляются подсказки")
    def test_search_suggestions(self, browser):
        browser.get(Config.UI_BASE_URL)
        handle_captcha(browser)
        close_popups(browser)
        main_page = MainPage(browser)
        WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable(main_page.SEARCH_INPUT)
        )
        for attempt in range(3):
            try:
                main_page.send_keys(main_page.SEARCH_INPUT, SEARCH_QUERY)
                break
            except Exception as e:
                print(f"Попытка ввода {attempt+1} не удалась: {e}")
                time.sleep(2)
        else:
            pytest.fail("Не удалось ввести текст после 3 попыток")
        results_page = SearchResultsPage(browser)
        assert results_page.wait_for_suggestions()

    @allure.title("Поиск по запросу 'Мастер' находит соответствующий фильм")
    def test_search_found_master(self, browser):
        browser.get(Config.UI_BASE_URL)
        handle_captcha(browser)
        close_popups(browser)
        main_page = MainPage(browser)
        WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable(main_page.SEARCH_INPUT)
        )
        main_page.send_keys(main_page.SEARCH_INPUT, SEARCH_QUERY + "\n")
        results_page = SearchResultsPage(browser)
        WebDriverWait(browser, 30).until(
            EC.visibility_of_element_located(results_page.FIRST_RESULT)
        )
        text = results_page.get_first_result_text()
        assert SEARCH_QUERY in text

    @allure.title(
            "Поиск несуществующего названия показывает сообщение об ошибке")
    def test_search_not_found(self, browser):
        browser.get(Config.UI_BASE_URL)
        handle_captcha(browser)
        close_popups(browser)
        main_page = MainPage(browser)
        WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable(main_page.SEARCH_INPUT)
        )
        main_page.send_keys(main_page.SEARCH_INPUT, INVALID_QUERY + "\n")
        results_page = SearchResultsPage(browser)
        WebDriverWait(browser, 30).until(
            EC.visibility_of_element_located(results_page.NOT_FOUND_MESSAGE)
        )
        assert results_page.is_not_found_message_displayed()
