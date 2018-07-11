#!/usr/bin/env python3

import base64
import sys
import os

try:
    src = sys.argv[1]
except:
    print('usage: %s file' % os.path.basename(sys.argv[0]))
    sys.exit()

data = open(src, 'rb').read()

content_type = os.path.splitext(src)[1][1:]

encoded = 'data:image/' + content_type + ';base64,' + base64.b64encode(data).decode('UTF-8')

print(encoded)

