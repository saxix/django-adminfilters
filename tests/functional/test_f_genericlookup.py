import pytest
from selenium.webdriver.common.by import By


@pytest.mark.selenium
def test_genericlookup_negated(live_server, selenium):
    input, button = None, None

    def submit():
        nonlocal input, button
        if button:
            button.click()
        input = selenium.wait_for(By.CSS_SELECTOR, 'input.filter-lookup')
        button = selenium.find_element(By.CSS_SELECTOR, 'a.filter-lookup.button.name__istartswith')

    selenium.get(f'{live_server.url}/')
    dim = selenium.get_window_size()
    selenium.set_window_size(1100, dim['height'])

    selenium.wait_for(By.LINK_TEXT, 'Artists').click()
    input = selenium.wait_for(By.CSS_SELECTOR, 'input.filter-lookup.name__istartswith')
    button = selenium.find_element(By.CSS_SELECTOR, 'a.filter-lookup.button.name__istartswith')

    input.send_keys('a')
    submit()
    assert 'Angus Young' not in selenium.page_source
