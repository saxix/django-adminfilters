import sys

from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.html import strip_tags
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

DATA = {
    "date": "2013-01-29",
    "datetime": "2013-01-01T02:18:33Z",
    "integer": 888888,
    "nullable": "bbbb",
    "time": "19:00:35",
    "bigint": 333333333,
    # "blank": "",
    "choices": 2,
    "decimal": "22.2",
    # "email": "s.apostolico@gmail.com",
    "float": 10.1,
    "generic_ip": "192.168.10.2",
    # "logic": False,
    # "not_editable": None,
    # "text": "lorem ipsum",
    # "url": "https://github.com/saxix/django-adminfilters",
    # # "flags": {},
}


def check_link_by_class(selenium, cls, view_name):
    link = selenium.find_element_by_class_name(cls)
    url = reverse(f"{view_name}")
    return f' href="{url}"' in link.get_attribute("innerHTML")


def get_all_attributes(driver, element):
    return list(
        driver.execute_script(
            "var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) {"
            " items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value"
            " }; return items;",
            element,
        )
    )


def is_clickable(driver, element):
    """Tries to click the element"""
    try:
        element.click()
        return True
    except Exception:
        return False


def mykey(group, request):
    return request.META["REMOTE_ADDR"][::-1]


def callable_rate(group, request):
    if request.user.is_authenticated:
        return None
    return (0, 1)


def scroll_to(driver, *args, _timeout=10):
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait

    wait = WebDriverWait(driver, _timeout)
    wait.until(EC.visibility_of_element_located((*args,)))
    return driver.find_element(*args)


def wait_for(driver, *args, _timeout=10):
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait

    wait = WebDriverWait(driver, _timeout)
    wait.until(EC.visibility_of_element_located((*args,)))
    return driver.find_element(*args)


def prompt(driver, text, _timeout=10):
    from selenium.webdriver.common.alert import Alert
    from selenium.webdriver.support.expected_conditions import alert_is_present
    from selenium.webdriver.support.ui import WebDriverWait

    wait = WebDriverWait(driver, _timeout)
    wait.until(alert_is_present())

    alert = Alert(driver)
    alert.send_keys(text)
    return alert


def confirm(driver, _timeout=10):
    from selenium.webdriver.common.alert import Alert
    from selenium.webdriver.support.expected_conditions import alert_is_present
    from selenium.webdriver.support.ui import WebDriverWait

    wait = WebDriverWait(driver, _timeout)
    wait.until(alert_is_present())

    alert = Alert(driver)
    return alert


def wait_and_click(driver, *args, _timeout=10):
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait

    wait = WebDriverWait(driver, _timeout)
    wait.until(EC.element_to_be_clickable((*args,)))
    return driver.find_element(*args).click()


def wait_for_url(driver, url):
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait

    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains(url))


class WebElementWrapper:
    def __init__(self, element: WebElement):
        self.element = element

    def __getattr__(self, item):
        return getattr(self.element, item)

    def __repr__(self):
        return '<{0.__module__}.{0.__name__} (session="{1}", element="{2}")>'.format(
            type(self.element), self._parent.session_id, self.element._id
        )

    @property
    def driver(self):
        return self.element.parent


class CellWrapper(WebElementWrapper):
    @cached_property
    def text(self):
        return self.element.get_attribute("innerText") or strip_tags(
            self.element.get_attribute("innerHTML")
        )


class RowWrapper(WebElementWrapper):
    @cached_property
    def values(self):
        return [e.text for e in self.cells]

    @cached_property
    def cells(self):
        ret = []
        for e in self.element.find_elements(By.CSS_SELECTOR, "td,th")[1:]:
            ret.append(CellWrapper(e))
        return ret


class EmptyChangeListWrapper(WebElementWrapper):
    rows = []
    header = []
    matrix = []

    def get_row(self, num):
        return None

    def get_col(self, num):
        return None

    def get_cell(self, row, col):
        return None


class ChangeListWrapper(EmptyChangeListWrapper):
    @classmethod
    def find_in_page(cls, driver):
        try:
            return ChangeListWrapper(
                driver.find_element(By.CSS_SELECTOR, "#changelist-form #result_list")
            )
        except NoSuchElementException:
            return EmptyChangeListWrapper(None)

    @cached_property
    def header(self) -> [RowWrapper]:
        return RowWrapper(self.element.find_element(By.CSS_SELECTOR, "thead tr"))

    @cached_property
    def rows(self) -> [RowWrapper]:
        return [
            RowWrapper(e)
            for e in self.element.find_elements(By.CSS_SELECTOR, "tbody tr")
        ]

    def get_row(self, num):
        return list(self.rows)[num]

    def get_col(self, num):
        return [row.cells[num] for row in self.rows]

    def get_cell(self, row, col):
        return self.rows[row].cells[col]

    def get_values(self, row=None, col=None):
        if row is None and col is None:
            return self.matrix
        if not (row is None or col is None):
            return self.matrix[row][col]
        if row is not None:
            return self.matrix[row]
        if col is not None:
            return [row[col] for row in self.matrix]

    @cached_property
    def matrix(self):
        cells = []
        for row in self.rows:
            cells.append([c.text for c in row.cells])
        return cells

    def pretty(self):
        from prettytable import PrettyTable

        x = PrettyTable(max_table_width=180)
        x.field_names = self.header.values
        x.add_rows(self.matrix)
        sys.stdout.write(f"\n{x}\n")


class Checkbox(WebElementWrapper):
    def checked(self, value):
        if value and not self.element.is_selected():
            self.driver.execute_script("arguments[0].click();", self.element)
        if not value and self.element.is_selected():
            self.driver.execute_script("arguments[0].click();", self.element)

    def check(self):
        if not self.element.is_selected():
            self.driver.execute_script("arguments[0].click();", self.element)

    def uncheck(self):
        if self.element.is_selected():
            self.driver.execute_script("arguments[0].click();", self.element)
