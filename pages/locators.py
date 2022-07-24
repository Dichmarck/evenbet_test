from selenium.webdriver.common.by import By




class BasePageLocators:
    BLOCK_TEXTURE = (By.CSS_SELECTOR, ".block.texture")
    LOGO = (By.CSS_SELECTOR, ".block.panel.lobby_logo")
    LOGIN_LINK = (By.CSS_SELECTOR, "div.MiniUserInfo__login_button")
    CASINO_LINK = (By.XPATH, "//div[text()='Casino']")
    SPINS_LINK = (By.XPATH, "//div[text()='Spins']")
    GAMES_LINK = (By.CSS_SELECTOR, ".text_block.TabButton__text:nth-child(1)")
    PROVIDERS_LINK = (By.XPATH, "//div[text()='providers'] ")
    CLOSE_BUTTON = (By.CSS_SELECTOR, ".close_button")


class GamesPageLocator:
    GAME = (By.CSS_SELECTOR, ".viewable-monitor .block")
    #GAME = (By.CSS_SELECTOR, "div.image")
    #GAME = (By.CSS_SELECTOR, "div.viewable-monitor")
    GAME_HOVER_NAME = (By.CSS_SELECTOR, ".viewable-monitor .block .text")
    GAMES_CONTAINER = (By.CSS_SELECTOR, "div.WidgetCasinoGameListContainer__games")
    GAME_WINDOW = (By.CSS_SELECTOR, ".block.Popup__content")
    GAME_WINDOW_NAME = (By.CSS_SELECTOR, ".text_block.Dialog__title_content")


class ProvidersPageLocator:
    PROVIDERS_CONTAINER = (By.CSS_SELECTOR, ".block .WidgetCasinoProvidersListContainer__providers__items")
    PROVIDER = (By.CSS_SELECTOR, ".block .WidgetCasinoProvidersListContainer__providers__items .image")
    PROVIDER_GAME_COUNT = (By.CSS_SELECTOR, ".WidgetCasinoProvidersListItemContainer__count__text")


class LoginPageLocator:
    USERNAME = (By.CSS_SELECTOR, "input[name=username]")
    PASSWORD = (By.CSS_SELECTOR, "input[name=password]")
    SIGN_IN = (By.CSS_SELECTOR, ".block.LoginContainer__buttons > div:nth-child(1)")
