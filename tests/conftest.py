import os
import sys
from pathlib import Path


def pytest_addoption(parser):
    parser.addoption(
        "--selenium",
        action="store_true",
        dest="enable_selenium",
        default=False,
        help="enable selenium tests",
    )

    parser.addoption(
        "--show-browser",
        "-S",
        action="store_true",
        dest="show_browser",
        default=False,
        help="will display start browsers in selenium tests",
    )


def pytest_configure(config):
    sys._called_from_pytest = True
    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    setattr(config.option, "driver", "chrome")

    if config.option.show_browser:
        setattr(config.option, "enable_selenium", True)

    if not config.option.enable_selenium:
        setattr(config.option, "markexpr", "not selenium")

    config.addinivalue_line(
        "markers", "skip_if_ci: this mark skips the tests on GitlabCI"
    )
    config.addinivalue_line(
        "markers", "skip_test_if_env(env): this mark skips the tests for the given env"
    )

    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "demoapp"))
    os.environ["DJANGO_SETTINGS_MODULE"] = "demo.settings"
    import django

    django.setup()
