'''
SEE ../LICENCE.TXT FOR LICENSING DETAILS
'''

import json
from os import path

class settings(object):
    def __init__(self, config='settings.json'):
        self.config = config
        self.settings = None
        self.load_config()

    def load_config(self):
        if path.exists(self.config):
            with open(self.config, 'r') as config:
                self.settings = json.loads(config.read())
        else:
            self.settings = {
                'twitter_api': {
                    'token': '',
                    'token_key': '',
                    'con_secret': '',
                    'con_secret_key': ''
                },
                'last_action': 0,
            }
            self.save_config()

    def save_config(self):
        with open(self.config, 'w') as config:
            config.write(json.dumps(self.settings, 
                sort_keys=True,
                indent=4))