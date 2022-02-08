import pytest
from demo.utils import ChangeListWrapper
from selenium.webdriver.common.by import By


def get_elements(selenium):
    return [selenium.find_element(By.CSS_SELECTOR, 'input[name=key].filter-adam.adam'),
            selenium.find_element(By.CSS_SELECTOR, 'input[name=value].filter-adam.adam'),
            selenium.find_element(By.CSS_SELECTOR, 'input[type=checkbox].filter-adam.adam'),
            selenium.find_element(By.CSS_SELECTOR, 'a.filter-adam.adam.button'),
            ChangeListWrapper.find_in_page(selenium)]


@pytest.mark.selenium
def test_djangolookup_filter(live_server, selenium):
    selenium.get(f'{live_server.url}/')
    dim = selenium.get_window_size()
    selenium.set_window_size(1100, dim['height'])
    selenium.wait_for(By.LINK_TEXT, 'Artists').click()
    key, value, negate, button, cl = get_elements(selenium)

    key.send_keys('name')
    value.send_keys('Angus')
    button.click()
    key, value, negate, button, cl = get_elements(selenium)
    assert list(dict.fromkeys(cl.get_col(2))) == ['Angus']
