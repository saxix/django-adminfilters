import pytest
from demo.utils import ChangeListWrapper, Checkbox
from selenium.webdriver.common.by import By


@pytest.mark.selenium
def test_genericlookup_forced_negated(live_server, selenium):
    def get_elements():
        return [selenium.wait_for(By.CSS_SELECTOR, 'input.filter-lookup'),
                selenium.find_element(By.CSS_SELECTOR, 'a.filter-lookup.button.name__istartswith'),
                ChangeListWrapper.find_in_page(selenium)]

    selenium.get(f'{live_server.url}/')
    dim = selenium.get_window_size()
    selenium.set_window_size(1100, dim['height'])
    selenium.wait_for(By.LINK_TEXT, 'Artists').click()
    input, button, cl = get_elements()

    input.send_keys('a')
    button.click()
    assert 'Angus Young' not in selenium.page_source


@pytest.mark.selenium
def test_genericlookup(live_server, selenium):
    def get_elements():
        return [selenium.wait_for(By.CSS_SELECTOR, '#country__name__istartswith '
                                                   'input[type=text].filter-lookup.country__name__istartswith'),
                Checkbox(selenium.find_element(By.CSS_SELECTOR, 'input[type=checkbox].filter-querystring.negate.qs')),
                selenium.find_element(By.CSS_SELECTOR, 'a.filter-lookup.button.country__name__istartswith'),
                ChangeListWrapper.find_in_page(selenium)]

    selenium.get(f'{live_server.url}/')
    dim = selenium.get_window_size()
    selenium.set_window_size(1100, dim['height'])
    selenium.wait_for(By.LINK_TEXT, 'Artists').click()
    input, negate, button, cl = get_elements()

    input.send_keys('Australia')
    button.click()
    input, negate, button, cl = get_elements()

    assert 'Rudd, Phil' in cl.get_col(4)
