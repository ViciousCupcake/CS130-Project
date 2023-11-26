"""
To use this, run the following command:
    python my_doc.py -p 8080
Then, go to http://localhost:8080/ to see the documentation.
"""

import django
import pydoc
import os

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cs130_efi.settings')
    django.setup()
    pydoc.cli()
