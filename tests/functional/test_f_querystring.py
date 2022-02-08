import pytest
from demo.management.commands.init_demo import sample_data
from demo.utils import ChangeListWrapper, Checkbox
from selenium.webdriver.common.by import By


@pytest.fixture
def data():
    from demo.factories import ArtistFactory
    ArtistFactory.create_batch(20)
    sample_data()


def get_elements(selenium):
    return [selenium.wait_for(By.CSS_SELECTOR, 'textarea.filter-querystring.qs'),
            selenium.find_element(By.CSS_SELECTOR, 'a.filter-querystring.adminfilters.button.qs'),
            Checkbox(selenium.find_element(By.CSS_SELECTOR, 'input.filter-querystring.negate.qs')),
            ChangeListWrapper.find_in_page(selenium)]


@pytest.mark.selenium
def test_querystring(live_server, selenium):
    selenium.get(f'{live_server.url}/')
    dim = selenium.get_window_size()
    selenium.set_window_size(1100, dim['height'])
    selenium.wait_for(By.LINK_TEXT, 'Artists').click()

    textarea, button, negate, cl = get_elements(selenium)

    textarea.send_keys('name=Angus')
    button.click()
    textarea, button, negate, cl = get_elements(selenium)
    assert len(cl.rows) == 1

    textarea.clear()
    textarea.send_keys('bands__name=AC/DC')
    button.click()
    textarea, button, negate, cl = get_elements(selenium)
    assert len(cl.rows) == 5
    assert 'Rudd, Phil' in cl.get_col(4)

    negate.check()
    textarea.clear()
    textarea.send_keys('bands__name=AC/DC')
    button.click()
    textarea, button, negate, cl = get_elements(selenium)
    assert 'Rudd, Phil' not in cl.get_col(4)

    negate.uncheck()
    textarea.clear()
    textarea.send_keys('country__name=United Kingdom\nbands__name=AC/DC\n!name=Angus')
    button.click()
    textarea, button, negate, cl = get_elements(selenium)
    assert 'Young, Angus' not in cl.get_col(4)

    textarea.clear()
    textarea.send_keys('bands__name=AC/DC\nname__in=Angus,Malcom')
    button.click()
    textarea, button, negate, cl = get_elements(selenium)
    assert len(cl.rows) == 2
    assert 'Young, Angus' in cl.get_col(4)


@pytest.mark.selenium
@pytest.mark.parametrize('flag,results', [('active=_T_', 1),
                                          ('active=_F_', 0),
                                          ('!active=_F_', 1),
                                          ('!active=_T_', 0),
                                          ])
def test_querystring_bool(live_server, selenium, flag, results):
    from demo.utils import wait_for

    selenium.get(f'{live_server.url}/')
    dim = selenium.get_window_size()
    selenium.set_window_size(1100, dim['height'])
    wait_for(selenium, By.LINK_TEXT, 'Artists').click()
    textarea, button, negate, cl = get_elements(selenium)

    negate.uncheck()
    textarea.clear()
    textarea.send_keys(f'{flag}\ncountry__name=Australia\nname=Phil')
    button.click()
    textarea, button, negate, cl = get_elements(selenium)
    assert len(cl.rows) == results


@pytest.mark.selenium
def test_errored_querystring(live_server, selenium):
    selenium.get(f'{live_server.url}/')
    dim = selenium.get_window_size()
    selenium.set_window_size(1100, dim['height'])
    selenium.wait_for(By.LINK_TEXT, 'Artists').click()

    textarea, button, negate, cl = get_elements(selenium)

    textarea.send_keys('invalid_field=AAAA')
    button.click()
    assert "Unknown field or lookup: 'invalid_field'" in selenium.page_source


@pytest.mark.selenium
def test_invalid_querystring(live_server, selenium):
    selenium.get(f'{live_server.url}/')
    dim = selenium.get_window_size()
    selenium.set_window_size(1100, dim['height'])
    selenium.wait_for(By.LINK_TEXT, 'Artists').click()

    textarea, button, negate, cl = get_elements(selenium)

    textarea.send_keys('=')
    button.click()
    assert 'Invalid django filter' in selenium.page_source
