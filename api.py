import allure
import requests
from typing import Dict, Optional, Any
from config import Config


class KinopoiskAPI:
    def __init__(
            self, base_url:
            Optional[str] = None, api_key: Optional[str] = None):
        self.base_url = base_url or Config.API_BASE_URL
        self.api_key = api_key or Config.API_KEY
        self.headers = {'X-API-KEY': self.api_key} if self.api_key else {}

    @allure.step("GET {path}")
    def _get(
        self, path: str, params:
            Optional[Dict[str, Any]] = None) -> requests.Response:
        url = f"{self.base_url}{path}"
        response = requests.get(url, headers=self.headers, params=params)
        return response

    @allure.step("Поиск фильма по названию '{query}'")
    def search_movie(
            self, query: str, page: int = 1,
            limit: int = 1) -> requests.Response:
        params = {'query': query, 'page': page, 'limit': limit}
        return self._get("/v1.4/movie/search", params=params)

    @allure.step("Получить список фильмов с параметрами {params}")
    def get_movies(self, params: Dict[str, Any]) -> requests.Response:
        return self._get("/v1.4/movie", params=params)
