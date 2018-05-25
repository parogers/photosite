#!/usr/bin/env python3

import os
import sys
import django
from django.core.management.utils import get_random_secret_key

secret_path = os.path.join(os.getenv('HOME'), '.photosite-secret-key')
if os.path.exists(secret_path):
    print('ERROR: path already exists: %s' % secret_path)
    sys.exit()

with open(secret_path, 'w') as file:
    file.write(get_random_secret_key())
