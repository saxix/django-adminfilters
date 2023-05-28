import pytest
from demo.utils import ChangeListWrapper, Checkbox
from selenium.webdriver.common.by import By

pytestmark = pytest.mark.selenium


def get_elements(selenium):
    container = selenium.find_element(
        By.ID, "last_name__istartswith_last_name__istartswith__negate"
    )
    return [
        container.find_element(By.CSS_SELECTOR, "input[type=text]"),
        Checkbox(container.find_element(By.CSS_SELECTOR, "input[type=checkbox]")),
        container.find_element(By.CSS_SELECTOR, "a.button"),
        ChangeListWrapper.find_in_page(selenium),
    ]


@pytest.mark.selenium
def test_value_simple_filter(data, admin_site):
    input_text, negate, button, cl = get_elements(admin_site.driver)
    input_text.send_keys("Young")
    button.click()
    input_text, negate, button, cl = get_elements(admin_site.driver)
    assert set(cl.get_values(None, 3)) == {"Young"}
    negate.click()
    button.click()
    input_text, negate, button, cl = get_elements(admin_site.driver)
    assert "Young" not in set(cl.get_values(None, 3))


@pytest.mark.selenium
def test_multivalue_simple_filter(data, admin_site):
    input_text, negate, button, cl = get_elements(admin_site.driver)
    input_text.send_keys("Young")
    button.click()
    input_text, negate, button, cl = get_elements(admin_site.driver)
    assert set(cl.get_values(None, 3)) == {"Young"}

    negate.click()
    button.click()
    input_text, negate, button, cl = get_elements(admin_site.driver)
    assert "Young" not in set(cl.get_values(None, 3))


@pytest.mark.selenium
def test_multivalue_filter_clear(data, admin_site):
    input_text, negate, button, cl = get_elements(admin_site.driver)
    input_text.send_keys("Young")
    button.click()
    input_text, negate, button, cl = get_elements(admin_site.driver)
    assert set(cl.get_values(None, 3)) == {"Young"}
    assert len(cl.rows) == 2

    button.click()
    input_text, negate, button, cl = get_elements(admin_site.driver)
    assert len(cl.rows) == 25
