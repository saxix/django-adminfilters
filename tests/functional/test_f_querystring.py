import pytest
from demo.management.commands.init_demo import sample_data
from demo.utils import ChangeListWrapper, Checkbox
from selenium.webdriver.common.by import By

pytestmark = pytest.mark.selenium


@pytest.fixture
def data():
    from demo.factories import ArtistFactory
    ArtistFactory.create_batch(20)
    sample_data()


def get_elements(selenium):
    container = selenium.find_element(By.ID, 'qs_qs__negate')
    return [container,
            container.find_element(By.CSS_SELECTOR, 'textarea'),
            container.find_element(By.CSS_SELECTOR, 'a.button'),
            Checkbox(container.find_element(By.CSS_SELECTOR, 'input[type=checkbox]')),
            ChangeListWrapper.find_in_page(selenium)]


@pytest.mark.parametrize('query,negated,check',
                         [('name=Angus', False, lambda cl: len(cl.rows) == 1),
                          ('bands__name=AC/DC', False, lambda cl: len(cl.rows) == 5),
                          ('bands__name=AC/DC', True, lambda cl: 'Rudd, Phil' not in cl.get_values(None, 4)),
                          ('country__name=United Kingdom\nbands__name=AC/DC\n!name=Angus', True,
                           lambda cl: 'Young, Angus' not in cl.get_values(None, 4)),
                          ('bands__name=AC/DC\nname__in=Angus,Malcom', False,
                           lambda cl: {'Young'} == set(cl.get_values(None, 3))),
                          ])
@pytest.mark.selenium
def test_querystring(admin_site, query, negated, check):
    __, textarea, button, negate, cl = get_elements(admin_site.driver)
    textarea.send_keys(query)
    negate.checked(negated)
    button.click()
    __, __, __, __, cl = get_elements(admin_site.driver)
    assert check(cl), cl.pretty()

    #
    # textarea.send_keys('name=Angus')
    # button.click()
    # __, textarea, button, __, cl = get_elements(admin_site.driver)
    # assert len(cl.rows) == 1
    #
    # textarea.clear()
    # textarea.send_keys('bands__name=AC/DC')
    # button.click()
    # __, textarea, button, negate, cl = get_elements(admin_site.driver)
    # assert len(cl.rows) == 5
    # assert 'Rudd, Phil' in cl.get_col(4)
    #
    # negate.check()
    # textarea.clear()
    # textarea.send_keys('bands__name=AC/DC')
    # button.click()
    # __, textarea, button, negate, cl = get_elements(admin_site.driver)
    # assert 'Rudd, Phil' not in cl.get_col(4)
    #
    # negate.uncheck()
    # textarea.clear()
    # textarea.send_keys('country__name=United Kingdom\nbands__name=AC/DC\n!name=Angus')
    # button.click()
    # __, textarea, button, negate, cl = get_elements(admin_site.driver)
    # assert 'Young, Angus' not in cl.get_col(4)
    #
    # textarea.clear()
    # textarea.send_keys('bands__name=AC/DC\nname__in=Angus,Malcom')
    # button.click()
    # __, textarea, button, negate, cl = get_elements(admin_site.driver)
    # assert len(cl.rows) == 2
    # assert 'Young, Angus' in cl.get_col(4)
    #


@pytest.mark.selenium
@pytest.mark.parametrize('flag,results', [('active=true', 1),
                                          ('active=false', 0),
                                          ('!active=false', 1),
                                          ('!active=true', 0),
                                          ])
def test_querystring_bool(admin_site, flag, results):
    textarea, button, negate, cl = get_elements(admin_site.driver)

    negate.uncheck()
    textarea.clear()
    textarea.send_keys(f'{flag}\ncountry__name=Australia\nname=Phil')
    button.click()
    textarea, button, negate, cl = get_elements(admin_site.driver)
    assert len(cl.rows) == results


@pytest.mark.selenium
def test_errored_querystring(admin_site):
    textarea, button, negate, cl = get_elements(admin_site.driver)

    textarea.send_keys('invalid_field=AAAA')
    button.click()
    assert "Unknown field 'invalid_field'" in admin_site.driver.page_source


@pytest.mark.selenium
def test_invalid_querystring(admin_site):
    textarea, button, negate, cl = get_elements(admin_site.driver)

    textarea.send_keys('=')
    button.click()
    assert 'Invalid django filter' in admin_site.driver.page_source
