#!/usr/bin/env python
import os
import sys
import threading

have_receive_ticket = False

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gti525.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise

    have_receive_ticket = False
    if 'runserver' in sys.argv:
        from api.GridCommunication import TerminalControler
        t1 = threading.Thread(name="DB Remote Init", target=TerminalControler().launch)
        t1.start()
    execute_from_command_line(sys.argv)
