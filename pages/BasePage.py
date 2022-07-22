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
        except [NoSuchElementException, TimeoutException]:
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
        print(games_link)
        time.sleep(2)

    def go_to_providers(self):
        self.should_be_logo()
        self.should_not_be_block_texture()
        casino_link = self.should_be_clickable_casino_link()
        casino_link.click()
        providers_link = self.should_be_clickable_providers_link()
        providers_link.click()
        print(providers_link)
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
        #password_field.send_keys(Keys.ENTER)

        sign_in_button = self.should_be_sign_in_button_field()
        #self.should_not_be_block_texture()
        sign_in_button.click()


class GamesPage(BasePage):

    def should_be_clickable_close_game(self):
        assert self.is_element_clickable(*GamesPageLocator.CLOSE_GAME, timeout=5), \
            "No clickable Close-Game button at game page"
        return self.browser.find_element(*GamesPageLocator.CLOSE_GAME)

    def should_be_games_container(self):
        assert self.is_element_appeared(*GamesPageLocator.GAMES_CONTAINER, timeout=10), \
            "No Games Container at games page"
        return self.browser.find_element(*GamesPageLocator.GAMES_CONTAINER)

    def scroll_all_games(self, provider_games_count=1375):
        self.should_not_be_block_texture()
        games_container = self.should_be_games_container()
        self.show_alert("Games Container is loaded", 0.3)
        action_chains = ActionChains(self.browser)
        scroll_origin = ScrollOrigin.from_element(games_container)

        games = []
        games_visited = 0
        exceptions_count = 0

        while games_visited < provider_games_count:
            time.sleep(1)
            new_games = self.browser.find_elements(*GamesPageLocator.GAME)

            if len(new_games) == 0:
                continue

            new_games_uniq = []

            for game in new_games:
                if game not in games:
                    new_games_uniq.append(game)
                    games.append(game)

            #for game in games:
            #    print(game)
            print("Всего игр: ", len(games))

            i = 0
            for game in new_games_uniq:
                try:
                    #action_chains.scroll_to_element(game).perform()
                    time.sleep(0.1)
                    game.click()
                    action_chains.send_keys(Keys.ESCAPE).perform()
                    games_visited += 1
                    i += 1
                    print("i = ", i)
                except StaleElementReferenceException:
                    games.remove(game)
                    new_games_uniq.remove(game)
                    exceptions_count += 1


            action_chains.scroll_from_origin(scroll_origin, 0, 284).perform() # высота блока 142

        print("Всего игр: ", len(games), "(", len(set(games)), ")")
        print("Игр посещено: ", games_visited)
        print("Всего игр у провадера: ", provider_games_count)
        print("Исключений сработано: ", exceptions_count)


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

