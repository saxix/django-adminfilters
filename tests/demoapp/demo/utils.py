from django.urls import reverse

DATA = {
    "date": "2013-01-29",
    "datetime": "2013-01-01T02:18:33Z",
    "integer": 888888,
    "nullable": "bbbb",
    "time": "19:00:35",
    "bigint": 333333333,
    # "blank": "",
    "choices": 2,
    "decimal": "22.2",
    # "email": "s.apostolico@gmail.com",
    "float": 10.1,
    "generic_ip": "192.168.10.2",
    # "logic": False,
    # "not_editable": None,
    # "text": "lorem ipsum",
    # "url": "https://github.com/saxix/django-adminfilters",
    # # "flags": {},
}


def check_link_by_class(selenium, cls, view_name):
    link = selenium.find_element_by_class_name(cls)
    url = reverse(f'{view_name}')
    return f' href="{url}"' in link.get_attribute('innerHTML')


def get_all_attributes(driver, element):
    return list(driver.execute_script(
        'var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) {'
        ' items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value'
        ' }; return items;',
        element))


def is_clickable(driver, element):
    """Tries to click the element"""
    try:
        element.click()
        return True
    except Exception:
        return False


def mykey(group, request):
    return request.META['REMOTE_ADDR'][::-1]


def callable_rate(group, request):
    if request.user.is_authenticated:
        return None
    return (0, 1)


def wait_for(driver, *args, _timeout=10):
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    wait = WebDriverWait(driver, _timeout)
    wait.until(EC.visibility_of_element_located((*args,)))
    return driver.find_element(*args)


def wait_for_url(driver, url):
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains(url))

