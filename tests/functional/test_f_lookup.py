import pytest
from demo.utils import ChangeListWrapper
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

pytestmark = pytest.mark.selenium


def get_elements(selenium):
    container = selenium.find_element(By.ID, "dj__key_dj__value_dj__negate")
    return [
        container,
        container.find_element(By.CSS_SELECTOR, "input[name=key]"),
        container.find_element(By.CSS_SELECTOR, "input[name=value]"),
        container.find_element(By.CSS_SELECTOR, "input[type=checkbox]"),
        container.find_element(By.CSS_SELECTOR, "a.button"),
        ChangeListWrapper.find_in_page(selenium),
    ]


@pytest.mark.selenium
def test_djangolookup_simple(admin_site):
    __, key, value, __, button, cl = get_elements(admin_site.driver)

    key.send_keys("name")
    value.send_keys("Angus")
    button.click()
    __, key, value, __, button, cl = get_elements(admin_site.driver)
    assert set(cl.get_values(None, 2)) == {"Angus"}


@pytest.mark.selenium
def test_djangolookup_negate(admin_site):
    __, key, value, negate, __, cl = get_elements(admin_site.driver)

    key.send_keys("name")
    value.send_keys("Angus")
    negate.click()
    value.send_keys(Keys.ENTER)
    __, key, value, negate, button, cl = get_elements(admin_site.driver)
    assert "Angus" not in set(cl.get_values(None, 2))


@pytest.mark.selenium
def test_djangolookup_invalid_field(admin_site):
    __, key, value, __, __, __ = get_elements(admin_site.driver)

    key.send_keys("xxx")
    value.send_keys("Angus")
    value.send_keys(Keys.ENTER)
    container, __, __, __, __, __ = get_elements(admin_site.driver)
    assert "Unknown field 'xxx'" in container.get_attribute("innerHTML")
