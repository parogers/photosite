
import json
import os

CONFIG_PATH = os.path.join(
    os.getenv('HOME'),
    '.config',
    'photosite')

def load_config(path):
    return json.load(open(os.path.join(CONFIG_PATH, path)))
