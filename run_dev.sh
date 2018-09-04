#!/bin/bash

export DJANO_SETTINGS_MODULE=photosite.settings.dev

pipenv run ./manage.py runserver
