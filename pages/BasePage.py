import time
from telnetlib import EC
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

    def go_to_games(self):
        #link = "https://poker.evenbetpoker.com/html5/"
        #browser.get(link)
        WebDriverWait(self.browser, timeout=self.timeout).until(EC.presence_of_element_located(BasePageLocators.LOGO))
        time.sleep(2)
        print("LOGO found")
        casino_link = self.browser.find_element(*GamesPageLocator.CASINO_LINK)
        casino_link.click()
        games_link = self.browser.find_element(*GamesPageLocator.GAMES_LINK)
        games_link.click()
        print(games_link)
        time.sleep(5)

    def login(self):
        self.browser.delete_all_cookies()
        self.open()
        self.browser.implicitly_wait(5)
        login_link = WebDriverWait(self.browser, timeout=self.timeout).until(
            EC.element_to_be_clickable(BasePageLocators.LOGIN_LINK))
        # login_link = WebDriverWait(browser, timeout=timeout).until(EC.presence_of_element_located(BasePageLocators.LOGIN_LINK))
        time.sleep(2)
        login_link.click()
        username_field = self.browser.find_element(*LoginPageLocator.USERNAME)
        password_field = self.browser.find_element(*LoginPageLocator.PASSWORD)
        username_field.click()  # без этого клика не работает
        # time.sleep(1)
        username_field.send_keys("for_tests")
        password_field.send_keys("for_tests")
        password_field.send_keys(Keys.ENTER)


class GamesPage(BasePage):

    def find_all_games(self):
        actions = ActionChains(self.browser)
        actions.move_by_offset(600, 600).perform()
        games = self.browser.find_elements(*GamesPageLocator.GAME)
        print(len(set(games)))
        games[0].click()
        close_game = WebDriverWait(self.browser, self.timeout).\
            until(EC.presence_of_element_located(GamesPageLocator.CLOSE_GAME))
        time.sleep(2)
        close_game.click()
        time.sleep(2)

        #self.browser.execute_script("arguments[0].scrollIntoView(true);", games[20])
        self.browser.execute_script("window.scrollTo(0, 200)")

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





