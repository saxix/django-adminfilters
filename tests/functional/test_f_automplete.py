import pytest
from demo.utils import ChangeListWrapper
from selenium.webdriver.common.by import By

pytestmark = pytest.mark.selenium


def get_elements(selenium):
    container = selenium.find_element(By.ID, "country__exact_country__isnull")
    el = selenium.find_elements(By.CSS_SELECTOR, "input.select2-search__field")
    return [
        container,
        container.find_element(By.CSS_SELECTOR, "span[role=combobox]"),
        el[0] if el else None,
        ChangeListWrapper.find_in_page(selenium),
    ]


@pytest.mark.selenium
def test_autocomplete(admin_site):
    __, select2, *__ = get_elements(admin_site.driver)
    select2.click()
    __, __, input_text, __ = get_elements(admin_site.driver)
    input_text.send_keys("United K")
    admin_site.wait_and_click(By.XPATH, '//li[contains(text(), "United Kingdom")]')
    *__, cl = get_elements(admin_site.driver)
    assert set(cl.get_values(None, 5)) == {"United Kingdom"}
