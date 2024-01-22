import contextlib
import logging
from urllib.parse import urljoin

import pytest
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


@pytest.fixture
def chrome_options(request):
    chrome_options = Options()
    if not request.config.getvalue("show_browser"):
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--allow-insecure-localhost")
    chrome_options.add_argument("--disable-translate")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--lang=en-GB")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-browser-side-navigation")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    return chrome_options


SELENIUM_DEFAULT_PAGE_LOAD_TIMEOUT = 3
SELENIUM_DEFAULT_IMPLICITLY_WAIT = 2
SELENIUM_DEFAULT_SCRIPT_TIMEOUT = 2


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


def get_errors(driver):
    """
    Checks browser for errors, returns a list of errors
    :param driver:
    :return:
    """
    try:
        browser_logs = driver.get_log("browser")
    except (ValueError, WebDriverException) as e:
        # Some browsers does not support getting logs
        logging.debug(
            "Could not get browser logs for driver %s due to exception: %s", driver, e
        )
        return []

    errors = [entry for entry in browser_logs if entry["level"] == "SEVERE"]

    return errors


@pytest.fixture
def selenium(driver):
    from demo.utils import confirm, prompt, wait_and_click, wait_for

    driver.with_timeouts = timeouts.__get__(driver)
    driver.set_input_value = set_input_value.__get__(driver)
    driver.wait_for = wait_for.__get__(driver)
    driver.wait_and_click = wait_and_click.__get__(driver)
    driver.prompt = prompt.__get__(driver)
    driver.confirm = confirm.__get__(driver)
    driver.get_errors = get_errors.__get__(driver)
    yield driver


@pytest.fixture(autouse=True)
def data():
    from demo.factories import ArtistFactory
    from demo.management.commands.init_demo import sample_data

    batch = ArtistFactory.create_batch(20)
    sample_data()
    return batch


class AdminSite:
    def __init__(self, live_server, driver):
        self.live_server = live_server
        self.driver = driver

    def open(self, path=""):
        self.driver.get(urljoin(self.live_server.url, path))
        dim = self.driver.get_window_size()
        self.driver.set_window_size(1100, dim["height"])

    def wait_for(self, *args):
        return self.driver.wait_for(*args)

    def prompt(self, *args):
        return self.driver.prompt(*args)

    def confirm(self, *args):
        return self.driver.confirm(*args)

    def wait_and_click(self, *args):
        return self.driver.wait_and_click(*args)

    def get_errors(self):
        return self.driver.get_errors()


@pytest.fixture
def admin_site(live_server, selenium, data):
    site = AdminSite(live_server, selenium)
    site.open("/")
    site.wait_for(By.LINK_TEXT, "Artists").click()
    errors = [err for err in site.get_errors() if err and 'favicon' not in err['message']]
    assert len(errors) == 0, "\n".join(["{message}".format(**err) for err in errors])
    return site
