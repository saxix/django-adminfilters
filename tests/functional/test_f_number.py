import pytest
from demo.management.commands.init_demo import sample_data
from demo.utils import ChangeListWrapper
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


@pytest.fixture
def data():
    sample_data()


def get_elements(selenium):
    return [selenium.wait_for(By.CSS_SELECTOR, '#year_of_birth input[type=text]'),
            ChangeListWrapper.find_in_page(selenium)]


@pytest.mark.parametrize('value,expected', [('1955', 1),
                                            ('>1953', 2),
                                            ('<>1955', 4),
                                            ('<1947', 1),
                                            ('<=1947', 2),
                                            ('1955,1953', 2),
                                            ('1953..1955', 3),
                                            ])
@pytest.mark.selenium
def test_number_filter(live_server, selenium, value, expected):
    selenium.get(f'{live_server.url}/')
    dim = selenium.get_window_size()
    selenium.set_window_size(1100, dim['height'])
    selenium.wait_for(By.LINK_TEXT, 'Artists').click()

    input, cl = get_elements(selenium)

    input.send_keys(value)
    input.send_keys(Keys.ENTER)
    input, cl = get_elements(selenium)
    assert len(cl.rows) == expected
