import time

import allure
import pytest
from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from evenbet_test.pages.BasePage import *


class TestGamesClickingAuthorized:
    @pytest.fixture(scope="class", autouse=True)
    def login(self, browser, timeout=30):
        login_page = BasePage(browser, "https://poker.evenbetpoker.com/html5/", timeout=timeout)
        login_page.login()

    @pytest.mark.scroll_all_games_auth  # pytest -s -v --tb=short -m scroll_all_games_auth
    def test_click_all_games(self, browser, timeout=20):
        """In this test we try to open website, login, go to Casino -> Games and click every games one by one."""
        games_page = GamesPage(browser, "https://poker.evenbetpoker.com/html5/", timeout=timeout)
        games_page.go_to_games()
        games_page.scroll_and_click_all_games(start_index=0)

    #provider_indexes = [i for i in range(19)]
    #provider_indexes.remove(10)
    #provider_indexes.remove(18)
    provider_indexes = [18]
    @pytest.mark.scroll_one_provider_auth  # pytest -s -v --tb=short -m scroll_one_provider_auth
    @pytest.mark.parametrize("provider_index", provider_indexes)
    def test_scroll_and_click_all_games_in_one_provider(self, browser, provider_index, timeout=30):
        """In this test we try to open website, login, go to Casino -> Providers.
        Then we try to open every provider and click all it's games."""
        with allure.step('Создаём объект страницы провайдеров'):
            providers_page = ProvidersPage(browser, "https://poker.evenbetpoker.com/html5/", timeout)
        with allure.step('Переходим во вкладку Games'):
            providers_page.go_to_games()
        with allure.step('Переходим во вкладку Providers'):
            providers_page.go_to_providers()
        with allure.step('Находим количество игр рассматриваемого провайдера'):
            provider_games_count = providers_page.find_games_count_by_provider_index(provider_index)
        with allure.step('Переходим в рассматриваемого провайдера'):
            providers_page.open_games_by_providers_index(provider_index)
        with allure.step('Прокликиваем все игры рассматриваемого провайдера'):
            providers_page.scroll_and_click_all_games(total_games_count=provider_games_count,
                                                      provider_index=provider_index)

