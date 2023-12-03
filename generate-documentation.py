"""
This file is used to generate documentation for the app.
This documentation is in the form of a HTML page.

To use this, run the following command:
    python generate-documentation.py -p 80 -n 0.0.0.0
Then, go to http://localhost:80/ to see the documentation.
"""

import django
import pydoc
import os

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cs130_efi.settings')
    django.setup()
    pydoc.cli()
