import contextlib

import pytest
from selenium.webdriver.chrome.options import Options


def pytest_configure(config):
    # if not config.option.driver:
    setattr(config.option, 'driver', 'chrome')


@pytest.fixture
def chrome_options(request):
    chrome_options = Options()
    if not request.config.getvalue('show_browser'):
        chrome_options.add_argument('--headless')
    return chrome_options


SELENIUM_DEFAULT_PAGE_LOAD_TIMEOUT = 3
SELENIUM_DEFAULT_IMPLICITLY_WAIT = 1
SELENIUM_DEFAULT_SCRIPT_TIMEOUT = 1


# @contextlib.contextmanager
# def page_load_timeout(driver, secs):
#     driver.set_page_load_timeout(secs)
#     yield
#     driver.set_page_load_timeout(SELENIUM_DEFAULT_PAGE_LOAD_TIMEOUT)
#
#
# @contextlib.contextmanager
# def implicitly_wait(driver, secs):
#     driver.implicitly_wait(secs)
#     yield
#     driver.implicitly_wait(SELENIUM_DEFAULT_IMPLICITLY_WAIT)
#

@contextlib.contextmanager
def timeouts(driver, wait=None, page=None, script=None):
    from selenium.webdriver.common.timeouts import Timeouts
    _current: Timeouts = driver.timeouts
    if wait:
        driver.implicitly_wait(wait)
    if page:
        driver.set_page_load_timeout(page)
    if script:
        driver.set_script_timeout(script)
    yield
    driver.timeouts = _current


def set_input_value(driver, *args):
    rules = args[:-1]
    el = driver.find_element(*rules)
    el.clear()
    el.send_keys(args[-1])


@pytest.fixture
def selenium(driver):
    driver.with_timeouts = timeouts.__get__(driver)
    driver.set_input_value = set_input_value.__get__(driver)

    yield driver
