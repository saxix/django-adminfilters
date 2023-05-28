import pytest
from demo.utils import ChangeListWrapper, Checkbox
from selenium.webdriver.common.by import By

pytestmark = pytest.mark.selenium


def get_elements(selenium):
    container = selenium.find_element(By.ID, "qs_qs__negate")
    return [
        container,
        container.find_element(By.CSS_SELECTOR, "textarea"),
        container.find_element(By.CSS_SELECTOR, "a.button"),
        Checkbox(container.find_element(By.CSS_SELECTOR, "input[type=checkbox]")),
        ChangeListWrapper.find_in_page(selenium),
    ]


@pytest.mark.parametrize(
    "query,negated,check",
    [
        ("name=Angus", False, lambda cl: len(cl.rows) == 1),
        ("bands__name=AC/DC", False, lambda cl: len(cl.rows) == 5),
        (
            "bands__name=AC/DC",
            True,
            lambda cl: "Rudd, Phil" not in cl.get_values(None, 4),
        ),
        (
            "country__name=United Kingdom\nbands__name=AC/DC\n!name=Angus",
            False,
            lambda cl: "Young, Angus" not in cl.get_values(None, 4),
        ),
        (
            "bands__name=AC/DC\nname__in=Angus,Malcom",
            False,
            lambda cl: {"Young"} == set(cl.get_values(None, 3)),
        ),
    ],
)
@pytest.mark.selenium
def test_querystring(admin_site, query, negated, check):
    __, textarea, button, negate, cl = get_elements(admin_site.driver)
    textarea.send_keys(query)
    negate.checked(negated)
    button.click()
    __, textarea, button, negate, cl = get_elements(admin_site.driver)
    assert check(cl), cl.pretty()


@pytest.mark.selenium
@pytest.mark.parametrize(
    "flag,results",
    [
        ("active=true", 1),
        ("active=false", 0),
        ("!active=false", 1),
        ("!active=true", 0),
    ],
)
def test_querystring_bool(admin_site, flag, results):
    __, textarea, button, negate, cl = get_elements(admin_site.driver)

    negate.uncheck()
    textarea.clear()
    textarea.send_keys(f"{flag}\ncountry__name=Australia\nname=Phil")
    button.click()
    __, textarea, button, negate, cl = get_elements(admin_site.driver)
    assert len(cl.rows) == results


@pytest.mark.selenium
def test_errored_querystring(admin_site):
    __, textarea, button, negate, cl = get_elements(admin_site.driver)

    textarea.send_keys("invalid_field=AAAA")
    button.click()
    assert "Unknown field 'invalid_field'" in admin_site.driver.page_source


@pytest.mark.selenium
def test_invalid_querystring(admin_site):
    __, textarea, button, negate, cl = get_elements(admin_site.driver)

    textarea.send_keys("=")
    button.click()
    assert "Invalid django filter" in admin_site.driver.page_source
