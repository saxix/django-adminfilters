import os
import sys


def pytest_configure(config):
    sys._called_from_pytest = True
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'demoapp'))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'demo.settings'
    import django
    django.setup()
