import pytest
from demo.utils import ChangeListWrapper, Checkbox
from selenium.webdriver.common.by import By

pytestmark = pytest.mark.selenium


def get_elements(selenium, target):
    container = selenium.find_element(By.ID, target)
    return [container.find_element(By.CSS_SELECTOR, 'input[type=text]'),
            Checkbox(container.find_element(By.CSS_SELECTOR, 'input[type=checkbox]')),
            container.find_element(By.CSS_SELECTOR, 'a.button'),
            ChangeListWrapper.find_in_page(selenium)]


@pytest.mark.selenium
def test_value_simple_filter(admin_site):
    target = 'last_name__istartswith_last_name__istartswith__negate'

    input_text, negate, button, cl = get_elements(admin_site.driver, target)
    input_text.send_keys('Young')
    button.click()
    input_text, negate, button, cl = get_elements(admin_site.driver, target)
    assert set(cl.get_values(None, 3)) == {'Young'}

    negate.click()
    button.click()
    input_text, negate, button, cl = get_elements(admin_site.driver, target)
    assert 'Young' not in set(cl.get_values(None, 3))


@pytest.mark.selenium
def test_multivalue_simple_filter(admin_site):
    target = 'last_name__istartswith_last_name__istartswith__negate'

    input_text, negate, button, cl = get_elements(admin_site.driver, target)
    input_text.send_keys('Young')
    button.click()
    input_text, negate, button, cl = get_elements(admin_site.driver, target)
    assert set(cl.get_values(None, 3)) == {'Young'}

    negate.click()
    button.click()
    input_text, negate, button, cl = get_elements(admin_site.driver, target)
    assert 'Young' not in set(cl.get_values(None, 3))
