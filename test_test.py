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

    def test_click_all_games(self, browser, timeout=20):
        games_page = GamesPage(browser, "https://poker.evenbetpoker.com/html5/", timeout=timeout)
        games_page.go_to_games()
        games_page.click_all_games()



@pytest.mark.scroll_all_games
def test_scroll_games_in_all_games(browser, timeout=20):
    games_page = GamesPage(browser, "https://poker.evenbetpoker.com/html5/", timeout=timeout)
    games_page.open()
    games_page.go_to_games()
    games_page.scroll_all_games()


@pytest.mark.scroll_one_provider
def test_scroll_games_in_one_provider(browser, timeout=20):
    provider_index = 13

    providers_page = ProvidersPage(browser, "https://poker.evenbetpoker.com/html5/", timeout)
    providers_page.open()
    providers_page.go_to_providers()
    provider_games_count = providers_page.find_games_count_by_provider_index(provider_index)
    providers_page.open_games_by_providers_index(provider_index)
    providers_page.scroll_all_games(provider_games_count)


