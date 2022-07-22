import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def pytest_addoption(parser):
    parser.addoption("--browser_name", action="store", default="chrome",
                     help="Choose browser: chrome or firefox")


@pytest.fixture(scope="class")
def browser(request):
    browser_name = request.config.getoption("browser_name")
    if browser_name == "chrome":
        print("\nStarting chrome browser for test..")
        options = Options()
        browser = webdriver.Chrome(options=options)

    elif browser_name == "firefox":
        print("\nstarting firefox browser for test..")
        firefox_profile = webdriver.FirefoxProfile()
        browser = webdriver.Firefox(firefox_profile=firefox_profile)

    else:
        raise pytest.UsageError("--browser_name should be chrome or firefox")
    browser.set_window_size(1920, 1080)
    yield browser

    print("\nQuit browser after test..")
    browser.quit()