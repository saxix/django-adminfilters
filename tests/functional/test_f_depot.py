import pytest
from demo.utils import ChangeListWrapper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from adminfilters.depot.models import StoredFilter

pytestmark = pytest.mark.selenium


def get_elements(selenium):
    container = selenium.find_element(By.ID, "adminfilters_depot_adminfilters_depot_op")
    btn = container.find_elements(By.CSS_SELECTOR, "a.button")
    return [
        container,
        Select(container.find_element(By.CSS_SELECTOR, "select")),
        btn[0] if btn else None,
        ChangeListWrapper.find_in_page(selenium),
    ]


@pytest.mark.selenium
def test_save_filter(admin_site):
    qs = "?name__in=Angus&name__in__negate=false"
    admin_site.open(f"/demo/artist/{qs}")
    __, select, button, cl = get_elements(admin_site.driver)

    button.click()
    admin_site.prompt("Filter #1").accept()

    __, select, button, cl = get_elements(admin_site.driver)
    sf = StoredFilter.objects.get(name="Filter #1")
    assert sf.query_string == qs


@pytest.mark.selenium
def test_select_filter(admin_site):
    sf = StoredFilter.objects.get(name="QueryString")

    __, select, button, cl = get_elements(admin_site.driver)
    select.select_by_visible_text(sf.name)
    admin_site.wait_for(By.TAG_NAME, "body")
    assert sf.query_string in admin_site.driver.current_url


@pytest.mark.selenium
def test_delete_filter(admin_site):
    sf = StoredFilter.objects.get(name="QueryString")
    __, select, button, cl = get_elements(admin_site.driver)
    select.select_by_visible_text(sf.name)
    admin_site.wait_for(By.TAG_NAME, "body")
    __, select, button, cl = get_elements(admin_site.driver)
    button.click()
    admin_site.confirm().accept()
    admin_site.wait_for(By.TAG_NAME, "body")
    assert not StoredFilter.objects.filter(name="QueryString").exists()
