import os
import sys


def pytest_configure(config):
    sys._called_from_pytest = True

    if config.option.show_browser:
        setattr(config.option, 'enable_selenium', True)

    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'demoapp'))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'demo.settings'
    import django
    django.setup()

def pytest_addoption(parser):
    parser.addoption('--selenium', action='store_true', dest='enable_selenium',
                     default=False, help='enable selenium tests')

    parser.addoption('--show-browser', '-S', action='store_true', dest='show_browser',
                     default=False, help='will not start browsers in headless mode')

