import allure
import pytest

SEARCH_QUERY = "Мастер"
TV_SERIES_COUNTRY = "Австралия"
TV_SERIES_YEAR = 2000
COMEDY_GENRE = "комедия"
RATING_FROM = 9
RATING_TO = 10
INVALID_YEAR = 200025


@pytest.mark.api
@allure.story("API: Поиск фильмов")
class TestAPISearch:

    @allure.title("Поиск фильма по названию на кириллице")
    def test_search_movie_cyrillic(self, api_client):
        response = api_client.search_movie(SEARCH_QUERY)
        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200
        data = response.json()
        with allure.step("Проверить название первого фильма"):
            assert data['docs'][0]['name'] == SEARCH_QUERY

    @allure.title("Поиск сериалов по стране производства и году релиза")
    def test_search_tv_series_by_country_and_year(self, api_client):
        params = {
            'type': 'tv-series',
            'countries.name': TV_SERIES_COUNTRY,
            'releaseYears.start': TV_SERIES_YEAR
        }
        response = api_client.get_movies(params)
        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200
        data = response.json()
        with allure.step("Проверить соответствие фильтров"):
            for movie in data['docs']:
                countries = [c['name'] for c in movie.get('countries', [])]
                assert TV_SERIES_COUNTRY in countries
                assert movie.get('year') == TV_SERIES_YEAR
                assert movie.get('type') == 'tv-series'

    @allure.title("Поиск комедий с рейтингом 9-10")
    def test_search_comedies_rating_9_10(self, api_client):
        params = {
            'genres.name': COMEDY_GENRE,
            'rating.kp': f"{RATING_FROM}-{RATING_TO}"
        }
        response = api_client.get_movies(params)
        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200
        data = response.json()
        with allure.step("Проверить рейтинг каждого фильма"):
            for movie in data['docs']:
                rating = movie.get('rating', {}).get('kp')
                assert rating is not None
                assert RATING_FROM <= rating <= RATING_TO

    @allure.title("Поиск с превышением лимита (должен вернуть 400)")
    def test_search_exceed_limit(self, api_client):
        params = {'limit': 251}
        response = api_client.get_movies(params)
        with allure.step("Проверить статус код 400"):
            assert response.status_code == 400
        data = response.json()
        with allure.step("Проверить сообщение об ошибке"):
            assert "limit" in str(data)

    @allure.title("Поиск с невалидным годом (должен вернуть 400)")
    def test_search_invalid_year(self, api_client):
        params = {'year': INVALID_YEAR}
        response = api_client.get_movies(params)
        with allure.step("Проверить статус код 400"):
            assert response.status_code == 400
        data = response.json()
        with allure.step("Проверить сообщение об ошибке"):
            assert "диапазоне" in data.get('message', [''])[0]
