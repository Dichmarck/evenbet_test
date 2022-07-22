from selenium.webdriver.common.by import By




class BasePageLocators:
    BLOCK_TEXTURE = (By.CSS_SELECTOR, ".block.texture")
    LOGO = (By.CSS_SELECTOR,
            ".block.panel.LobbyContainer.LobbyContainer_v_default.LobbyContainer_c_blue.lpg-lobby-promo-list")
    LOGIN_LINK = (By.CSS_SELECTOR,""".block.panel.button.SimpleButton.SimpleButton_v_flat.SimpleButton_c_light.SimpleButton_use_text_use_icon.MiniUserInfo__login_button.SimpleButton_interactive""" )
    CASINO_LINK = (By.XPATH, "//div[text()='Casino']")
    SPINS_LINK = (By.XPATH, "//div[text()='Spins']")
    GAMES_LINK = (By.CSS_SELECTOR, ".text_block.TabButton__text:nth-child(1)")
    #PROVIDERS_LINK = (By.CSS_SELECTOR, ".WidgetCasinoGameListRootContainer__tabs .block.TabButton__content") # [1]
    PROVIDERS_LINK = (By.XPATH, "//div[text()='providers'] ")


class GamesPageLocator:
    GAME = (By.CSS_SELECTOR, ".viewable-monitor .block")
    CLOSE_GAME = (By.CSS_SELECTOR, ".block.panel.button.SimpleButton.SimpleButton_v_transparent.SimpleButton_c_blue.SimpleButton_use_icon.Dialog__top_action.close_button.SimpleButton_interactive")
    #GAMES_CONTAINER = (By.CSS_SELECTOR, ".block.scroll-wrapper .WidgetCasinoGameListContainer__items")
    GAMES_CONTAINER = (By.CSS_SELECTOR, ".block.panel.LobbyContainer.LobbyContainer_v_default.LobbyContainer_c_blue.lpg-lobby-casino-game-list")
    #.block.panel.LobbyContainer.LobbyContainer_v_default.LobbyContainer_c_blue.lpg-lobby-casino-game-list


class ProvidersPageLocator:
    PROVIDERS_CONTAINER = (By.CSS_SELECTOR, ".block .WidgetCasinoProvidersListContainer__providers__items")
    PROVIDER = (By.CSS_SELECTOR, ".block .WidgetCasinoProvidersListContainer__providers__items .image")
    PROVIDER_GAME_COUNT = (By.CSS_SELECTOR, ".WidgetCasinoProvidersListItemContainer__count__text")


class LoginPageLocator:
    USERNAME = (By.CSS_SELECTOR, ".block.panel.FormField.FormField_v_default.FormField_c_light.LoginContainer__form_field.LoginContainer__input.LoginContainer__username input")
    PASSWORD = (By.CSS_SELECTOR, ".block.panel.FormField.FormField_v_default.FormField_c_light.LoginContainer__form_field.LoginContainer__input.LoginContainer__password input")
    SIGN_IN = (By.CSS_SELECTOR, ".block.panel.button.SimpleButton.SimpleButton_v_flat.SimpleButton_c_success_blue.SimpleButton_use_text.LoginContainer__action.LoginContainer__sign_in_action.SimpleButton_interactive")
    #SIGN_IN = (By.XPATH, "//div[text()='Sign In']")
