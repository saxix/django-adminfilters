#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    here = os.path.realpath(os.path.dirname(__file__))
    sys.path.insert(0, here)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
