#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'czaspracytrenera.settings.development')
    os.environ['DJANGO_SECRET_KEY'] = "5q&x$c_lgx5ioo%8p)1vzd)m5#7n43v)5iodvrxqfpr8*jl&*%"
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
