import pytest
from selenium.webdriver.common.by import By

pytestmark = pytest.mark.selenium



#
# def get_linked_ac(driver):
#     elements = [
#         get_elements(driver, cssid=cssid)
#         for cssid in [
#             'favourite_city__region__country__exact_favourite_city__region__country__isnull',
#             'favourite_city__region__exact_favourite_city__region__isnull',
#             'favourite_city__exact_favourite_city__isnull',
#         ]
#     ]
#     return elements


@pytest.mark.selenium
def test_unionlist_filter(admin_factory):
    site = admin_factory('UnionFieldListFilters')
    site.driver.find_elements(By.CSS_SELECTOR, '<details>[data-filter-title~="Bands"]')

    print(1)
    print(1)

    # __, select2, *__ = get_elements(site.driver)
    # select2.click()
    # __, __, input_text, __ = get_elements(site.driver)
    # input_text.send_keys("United K")
    # admin_site.wait_and_click(By.XPATH, '//li[contains(text(), "United Kingdom")]')
    # *__, cl = get_elements(admin_site.driver)
    # assert set(cl.get_values(None, 5)) == {"United Kingdom"}
    # el = admin_site.driver.find_elements(By.ID, "select2-ac_country-container")
    # assert 'United Kingdom' in el[0].text

#
# @pytest.mark.selenium
# def test_linked_autocomplete(admin_site):
#     __, select2, *__ = get_elements(admin_site.driver)
#     select2.click()
#     __, __, input_text, __ = get_elements(admin_site.driver)
#     input_text.send_keys("United K")
#     admin_site.wait_and_click(By.XPATH, '//li[contains(text(), "United Kingdom")]')
#     *__, cl = get_elements(admin_site.driver)
#     assert set(cl.get_values(None, 5)) == {"United Kingdom"}
#     el = admin_site.driver.find_elements(By.ID, "select2-ac_country-container")
#     assert 'United Kingdom' in el[0].text
#
#     country, region, city = get_linked_ac(admin_site.driver)
#     assert country and not (region or city), "Others should be disabled"
#     country[1].click()
#     country, region, city = get_linked_ac(admin_site.driver)
#     country[2].send_keys("Aus")
#     admin_site.wait_and_click(By.XPATH, '//li[contains(text(), "Australia")]')
#     country, region, city = get_linked_ac(admin_site.driver)
#     assert country and region and not city, "Only city should be disabled"
#
#     region[1].click()
#     country, region, city = get_linked_ac(admin_site.driver)
#     region[2].send_keys("Cap")
#     admin_site.wait_and_click(By.XPATH, '//li[contains(text(), "Australian Capital Territory")]')
#     country, region, city = get_linked_ac(admin_site.driver)
#     assert country and region and city, "All should be there"
#
#     city[1].click()
#     country, region, city = get_linked_ac(admin_site.driver)
#     city[2].send_keys("Cam")
#     admin_site.wait_and_click(By.XPATH, '//li[contains(text(), "Camberra")]')
