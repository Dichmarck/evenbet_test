import copy
import time
from telnetlib import EC

from selenium.common import *
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from .locators import *


class BasePage:
    def __init__(self, browser, link, timeout):
        self.browser = browser
        self.link = link
        self.timeout = timeout

    def open(self):
        self.browser.get(self.link)
        self.should_be_logo()
        self.should_not_be_block_texture()

    def show_alert(self, message: str = "Alert", duration: float = 0.5):
        self.browser.execute_script(f"alert('{message}');")
        time.sleep(duration)
        self.browser.switch_to.alert.accept()

    def is_element_present(self, how, what):
        try:
            self.browser.find_element((how, what))
        except NoSuchElementException:
            return False
        return True

    def is_element_appeared(self, how, what, timeout=30):
        try:
            WebDriverWait(self.browser, timeout, poll_frequency=0.2).until(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return False
        return True

    def is_not_element_present(self, how, what, timeout=5):
        try:
            WebDriverWait(self.browser, timeout, poll_frequency=0.1).until(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return True
        return False

    def is_disappeared(self, how, what, timeout=5):
        try:
            WebDriverWait(self.browser, timeout, 0.1, [TimeoutException]). \
                until_not(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return False
        return True

    def is_element_clickable(self, how, what, timeout=30):
        try:
            WebDriverWait(self.browser, timeout).until(EC.element_to_be_clickable((how, what)))
        except TimeoutException:
            return False
        return True

    def should_not_be_block_texture(self):
        assert self.is_disappeared(*BasePageLocators.BLOCK_TEXTURE), \
            "block_texture presents, but it shouldn't to"

    def should_be_logo(self):
        assert self.is_element_appeared(*BasePageLocators.LOGO), "No logo at page"
        return self.browser.find_element(*BasePageLocators.LOGO)

    def should_be_clickable_casino_link(self):
        assert self.is_element_clickable(*BasePageLocators.CASINO_LINK), "No clickable Casino link (button) on page"
        return self.browser.find_element(*BasePageLocators.CASINO_LINK)

    def should_be_clickable_games_link(self):
        assert self.is_element_clickable(*BasePageLocators.GAMES_LINK), "No clickable Games link (button) on page"
        return self.browser.find_element(*BasePageLocators.GAMES_LINK)

    def should_be_clickable_providers_link(self):
        assert self.is_element_clickable(*BasePageLocators.PROVIDERS_LINK), \
            "No clickable Providers link (button) at page"
        return self.browser.find_element(*BasePageLocators.PROVIDERS_LINK)

    def go_to_games(self):
        self.should_be_logo()
        self.should_not_be_block_texture()
        casino_link = self.should_be_clickable_casino_link()
        casino_link.click()
        games_link = self.should_be_clickable_games_link()
        games_link.click()
        time.sleep(2)

    def go_to_providers(self):
        self.should_be_logo()
        self.should_not_be_block_texture()
        casino_link = self.should_be_clickable_casino_link()
        casino_link.click()
        providers_link = self.should_be_clickable_providers_link()
        providers_link.click()
        time.sleep(2)

    def should_be_clickable_login_link(self):
        assert self.is_element_appeared(*BasePageLocators.LOGIN_LINK), "No Login link (button) at page"
        return self.browser.find_element(*BasePageLocators.LOGIN_LINK)

    def should_be_username_field(self):
        assert self.is_element_appeared(*LoginPageLocator.USERNAME), "No username field at login page"
        return self.browser.find_element(*LoginPageLocator.USERNAME)

    def should_be_password_field(self):
        assert self.is_element_appeared(*LoginPageLocator.PASSWORD), "No password field at login page"
        return self.browser.find_element(*LoginPageLocator.PASSWORD)

    def should_be_sign_in_button_field(self):
        assert self.is_element_appeared(*LoginPageLocator.SIGN_IN), "No Sign In button field at login page"
        return self.browser.find_element(*LoginPageLocator.SIGN_IN)

    def login(self):
        self.browser.delete_all_cookies()
        self.open()
        self.browser.implicitly_wait(5)
        login_link = self.should_be_clickable_login_link()
        self.should_not_be_block_texture()
        login_link.click()

        username_field = self.should_be_username_field()
        password_field = self.should_be_password_field()
        username_field.send_keys("for_tests")
        password_field.send_keys("for_tests")
        # password_field.send_keys(Keys.ENTER)

        sign_in_button = self.should_be_sign_in_button_field()
        # self.should_not_be_block_texture()
        sign_in_button.click()


class GamesPage(BasePage):
    game_block_height = 142

    def should_be_clickable_close_game(self):
        assert self.is_element_clickable(*BasePageLocators.CLOSE_BUTTON, timeout=5), \
            "No clickable Close-Game button at game page"
        return self.browser.find_element(*BasePageLocators.CLOSE_BUTTON)

    def should_be_games_container(self):
        assert self.is_element_appeared(*GamesPageLocator.GAMES_CONTAINER, timeout=10), \
            "No Games Container at games page"
        return self.browser.find_element(*GamesPageLocator.GAMES_CONTAINER)

    def scroll_and_click_all_games(self, total_games_count=1375, start_index=0, visited_games=0):

        self.should_not_be_block_texture()  # проверка на отсутсвие блока загрузки
        games_container = self.browser.find_element(*GamesPageLocator.GAMES_CONTAINER)

        action_chains = ActionChains(self.browser)
        scroll_origin = ScrollOrigin.from_element(games_container)
        action_chains.move_to_element_with_offset(games_container, -80, 0).perform()

        visited = visited_games
        games = []  # список для всех, найдённых при данном вызове функции
        start = start_index

        while True:

            new_games_added = 0
            load_retries = 0
            while new_games_added == 0 and load_retries < 5:
                if load_retries != 0:
                    time.sleep(1)
                #loaded_games = self.browser.find_elements(*GamesPageLocator.GAME)
                #action_chains.scroll_to_element(loaded_games[0]).move_to_element(loaded_games[0]).perform()
                #time.sleep(1)
                action_chains.click(games_container).perform()
                loaded_games = self.browser.find_elements(*GamesPageLocator.GAME)
                for loaded_game in loaded_games:
                    if loaded_game not in games:
                        games.append(loaded_game)
                        new_games_added += 1
            if load_retries >= 5:
                print("===== Просмотрены все игры на странице! =====")
                break

            print(f"Игр обнаружено: {len(games)}, игр проверено: {visited}")
            for game in games[start:]:
                #action_chains.scroll_to_element(game).move_to_element(game).perform()
                action_chains.move_to_element(game).perform()
                game.click()
                start += 1
                visited += 1
                if self.is_element_appeared(*GamesPageLocator.GAME_WINDOW, timeout=1):  # если игра в окне
                    game_name = self.browser.find_element(*GamesPageLocator.GAME_WINDOW_NAME)
                    print(f"{visited} - {game_name.text}")
                    action_chains.send_keys(Keys.ESCAPE).perform()  # закрываем
                else:
                    print(f"{visited} - Полноэкранная игра")
                    self.go_to_games()  # иначе переходим во вкладку игры
                    self.scroll_and_click_all_games(start_index=games.index(game)+1, visited_games=visited)
                    # вызваем функцию, но с пропуском всех уже прокликанных игр
                    return

            action_chains.scroll_from_origin(scroll_origin, 0, 142).perform()  # если загруженные игры кончились,
            time.sleep(1)

        assert visited == total_games_count, "Количество проверенных игр не равно общему количеству"


class ProvidersPage(GamesPage):

    def should_be_providers_container(self):
        assert self.is_element_appeared(*ProvidersPageLocator.PROVIDERS_CONTAINER, timeout=10), \
            "No Providers Container at providers page"
        return self.browser.find_element(*ProvidersPageLocator.PROVIDERS_CONTAINER)

    def find_games_count_by_provider_index(self, index):
        self.should_be_providers_container()
        provider_games_count = self.browser.find_elements(*ProvidersPageLocator.PROVIDER_GAME_COUNT)[index].text
        provider_games_count = int(provider_games_count.split()[0])
        print(provider_games_count)
        return provider_games_count

    def open_games_by_providers_index(self, index):
        self.should_be_providers_container()
        providers = self.browser.find_elements(*ProvidersPageLocator.PROVIDER)
        providers[index].click()
        time.sleep(2)

    def scroll_and_click_all_games(self, total_games_count=1375, start_index=0, visited_games=0, provider_index=0):

        self.should_not_be_block_texture()  # проверка на отсутсвие блока загрузки
        games_container = self.browser.find_element(*GamesPageLocator.GAMES_CONTAINER)

        action_chains = ActionChains(self.browser)
        scroll_origin = ScrollOrigin.from_element(games_container)
        visited = visited_games
        games = []  # список для всех, найдённых при данном вызове функции
        start = start_index

        while True:

            new_games_added = 0
            load_retries = 0
            while new_games_added == 0 and load_retries < 5:
                time.sleep(1)
                loaded_games = self.browser.find_elements(*GamesPageLocator.GAME)
                action_chains.click(games_container).perform()
                loaded_games = self.browser.find_elements(*GamesPageLocator.GAME)
                for loaded_game in loaded_games:
                    if loaded_game not in games:
                        games.append(loaded_game)
                        new_games_added += 1
                load_retries += 1
            if load_retries >= 5:
                print("===== Просмотрены все игры на странице! =====")
                break

            print(f"Игр обнаружено: {len(games)}, игр проверено: {visited}")
            for game in games[start:]:
                action_chains.scroll_to_element(game).move_to_element(game).perform()
                game.click()
                start += 1
                visited += 1
                if self.is_element_appeared(*GamesPageLocator.GAME_WINDOW, timeout=0.3):  # если игра в окне
                    game_name = self.browser.find_element(*GamesPageLocator.GAME_WINDOW_NAME)
                    print(f"{visited} - {game_name.text}")
                    time.sleep(0.1)
                    action_chains.send_keys(Keys.ESCAPE).perform()  # закрываем
                else:
                    print(f"{visited} - Полноэкранная игра")
                    self.go_to_games()  # иначе переходим во вкладку игры
                    self.go_to_providers()
                    self.open_games_by_providers_index(provider_index)
                    self.scroll_and_click_all_games(total_games_count=total_games_count,
                                                    start_index=games.index(game) + 1,
                                                    visited_games=visited,
                                                    provider_index=provider_index)
                    # вызваем функцию, но с пропуском всех уже прокликанных игр
                    return

            action_chains.scroll_from_origin(scroll_origin, 0, 142).perform()  # если загруженные игры кончились,
            time.sleep(1)

        print(f"Игр обнаружено: {len(games)}, игр проверено: {visited}")
        assert visited == total_games_count, "Количество проверенных игр не равно общему количеству"
