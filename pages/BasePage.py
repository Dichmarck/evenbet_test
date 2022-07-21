import time
from telnetlib import EC

from selenium.common import *
from selenium.webdriver import Keys, ActionChains
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

    def is_element_present(self, how, what):
        try:
            WebDriverWait(self.browser, 30, poll_frequency=0.2).until(EC.presence_of_element_located((how, what)))
        except NoSuchElementException:
            return False
        return True

    def is_not_element_present(self, how, what, timeout=5):
        try:
            WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return True
        return False

    def is_disappeared(self, how, what, timeout=5):
        try:
            WebDriverWait(self.browser, timeout, 0.2, TimeoutException). \
                until_not(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return False
        return True

    def is_element_clickable(self, how, what):
        try:
            WebDriverWait(self.browser, 30).until(EC.element_to_be_clickable((how, what)))
        except ElementClickInterceptedException:
            return False
        return True

    def should_not_be_block_texture(self):
        assert self.is_disappeared(*BasePageLocators.BLOCK_TEXTURE), \
            "block_texture presents, but it shouldn't to"

    def should_be_logo(self):
        assert self.is_element_present(*BasePageLocators.LOGO), "No logo at page"
        return self.browser.find_element(*BasePageLocators.LOGO)

    def should_be_clickable_casino_link(self):
        assert self.is_element_clickable(*BasePageLocators.CASINO_LINK), "No clickable Casino link (button) at page"
        return self.browser.find_element(*BasePageLocators.CASINO_LINK)

    def should_be_clickable_games_link(self):
        assert self.is_element_clickable(*BasePageLocators.GAMES_LINK), "No clickable Games link (button) at page"
        return self.browser.find_element(*BasePageLocators.GAMES_LINK)

    def go_to_games(self):
        self.should_be_logo()
        self.should_not_be_block_texture()
        casino_link = self.should_be_clickable_casino_link()
        casino_link.click()
        games_link = self.should_be_clickable_games_link()
        games_link.click()
        print(games_link)
        time.sleep(2)

    def should_be_clickable_login_link(self):
        assert self.is_element_present(*BasePageLocators.LOGIN_LINK), "No Login link (button) at page"
        return self.browser.find_element(*BasePageLocators.LOGIN_LINK)

    def should_be_username_field(self):
        assert self.is_element_present(*LoginPageLocator.USERNAME), "No username field at login page"
        return self.browser.find_element(*LoginPageLocator.USERNAME)

    def should_be_password_field(self):
        assert self.is_element_present(*LoginPageLocator.PASSWORD), "No password field at login page"
        return self.browser.find_element(*LoginPageLocator.PASSWORD)

    def should_be_sign_in_button_field(self):
        assert self.is_element_present(*LoginPageLocator.SIGN_IN), "No Sign In button field at login page"
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
        assert self.is_element_clickable(*GamesPageLocator.CLOSE_GAME), \
            "No clockable Close Game button field at game page"
        return self.browser.find_element(*GamesPageLocator.CLOSE_GAME)

    def click_all_games(self):
        self.should_not_be_block_texture()
        actions = ActionChains(self.browser)
        actions.move_by_offset(600, 600).perform()
        games = self.browser.find_elements(*GamesPageLocator.GAME)
        print(len(set(games)))
        games[0].click()
        close_game = self.should_be_clickable_close_game()
        close_game.click()
        time.sleep(0.5)

        #games_container = self.browser.find_element(*GamesPageLocator.GAMES_CONTAINER)
        #games_container.click()

        #self.browser.execute_script("arguments[0].scrollIntoView(true);", games[20])
        self.browser.execute_script("window.scrollTo(0, 800)")

        time.sleep(1)


        games = []
        #games_found = self.browser.find_elements(*GamesPageLocator.GAME)
        #print(games_found)
        #while len(games) < 500:
        #    games_found = self.browser.find_elements(*GamesPageLocator.GAME)
        #    #self.browser.execute_script("arguments[0].scrollIntoView(true);", games_found[int(len(games_found)/2)])
        #    self.browser.execute_script("window.scrollTo(0, 200)")
        #    time.sleep(1)
        #    games = list(set(games + games_found))
        #    #games_found = self.browser.find_elements(*GamesPageLocator.GAME)

        #print(len(games_found))
        #print(len(set(games_found)))
        #games += games_found





