#!/usr/bin/env python3

from django.core.management.utils import get_random_secret_key
import os
import json

config_path = os.path.join(
    os.getenv('HOME'),
    '.config',
    'photosite')

if not os.path.exists(config_path):
    os.makedirs(config_path)

def gen_config(
        dest,
        secret,
        server_host='localhost',
        static_url=None,
        static_path=None,
        media_url=None,
        media_path=None):

    config_data = {
        'database' : {
            'ENGINE' : 'django.db.backends.mysql',
            'NAME' : 'dbname',
            'USER' : 'user',
            'PASSWORD' : 'pass',
            'HOST' : '/var/run/mysqld/mysqld.sock',
            'PORT' : '',
        },
        'alt-database' : {
            'ENGINE' : 'django.db.backends.postgresql',
            'NAME' : 'dbname',
            'USER' : 'user',
            'PASSWORD' : 'pass',
            'HOST' : 'localhost',
            'PORT' : '5432',
        },
        'alt2-database': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'path/to/db.sqlite3',
        },
        'django-secret' : secret,
        'server-host' : server_host,
    }

    if media_url:
        config_data['media-url'] = media_url

    if static_url:
        config_data['static-url'] = static_url

    if media_path:
        config_data['media-path'] = media_path

    if static_path:
        config_data['static-path'] = static_path

    print('Generating config: %s' % dest)

    if os.path.exists(dest):
        if input('WARNING: File exists, overwrite it? ') != 'y':
           print('Cancelled')
           return

    with open(dest, 'w') as file:
        file.write(json.dumps(config_data, indent=4) + '\n')

gen_config(
    os.path.join(config_path, 'dev.ini'),
    get_random_secret_key(),
    static_path='path/to/static/folder',
    media_path='path/to/media/folder')

gen_config(
    os.path.join(config_path, 'production.ini'),
    get_random_secret_key(),
    server_host='someserver.com',
    static_url='static.someserver.com/static/',
    media_url='media.someserver.com/media/',
    media_path='path/to/media/folder/')
