import pytest
from selenium.webdriver.common.by import By

pytestmark = pytest.mark.selenium


@pytest.mark.selenium
def test_unionlist_filter(admin_factory):
    site = admin_factory('UnionFieldListFilters')
    site.wait_and_click(
        By.XPATH,
        '//*[@id="changelist-filter"]//a[contains(text(), "AC/DC")]'
    )
    site.wait_for(By.XPATH, '//*[@id="result_list"]/tbody/tr')
    assert len(
        site.driver.find_elements(By.XPATH, '//*[@id="result_list"]/tbody/tr')
    ) == 4, 'Should have 5 artists selected'
    site.wait_for(By.XPATH, '//*[@id="result_list"]/tbody/tr')
    site.wait_and_click(
        By.XPATH,
        '//*[@id="changelist-filter"]//a[contains(text(), "Abba")]'
    )
    assert len(
        site.driver.find_elements(By.XPATH, '//*[@id="result_list"]/tbody/tr')
    ) == 5, 'Should have 6 artists selected'
