import time
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
        games_page = GamesPage(browser, "https://poker.evenbetpoker.com/html5/", timeout=timeout)
        games_page.go_to_games()
        games_page.scroll_and_click_all_games(start_index=0)

    providers_indexes = [i for i in range(19)]
    @pytest.mark.scroll_one_provider_auth  # pytest -s -v --tb=short -m scroll_one_provider_auth
    # @pytest.mark.parametrize("provider_index", providers_indexes)
    def test_scroll_and_click_all_games_in_one_provider(self, browser, provider_index=10, timeout=20):
        providers_page = ProvidersPage(browser, "https://poker.evenbetpoker.com/html5/", timeout)
        providers_page.go_to_providers()
        provider_games_count = providers_page.find_games_count_by_provider_index(provider_index)
        providers_page.open_games_by_providers_index(provider_index)
        providers_page.scroll_and_click_all_games(total_games_count=provider_games_count, provider_index=provider_index)
