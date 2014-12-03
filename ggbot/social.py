'''
SEE ../LICENCE.TXT FOR LICENSING DETAILS
'''

import twitter
from time import time, sleep
from random import randint

from settings import settings
from blocked import block_tracker

class manage_twitter(object):
    def __init__(self, delay=5):
        self.delay = delay

    def valid_api(self):
        sttngs = settings()
        return sttngs.settings['twitter_api']['token'] != ''

    def action_proceed(self):
        sttngs = settings()
        return time() >= sttngs.settings['last_action']

    def new_follow(self):
        sttngs = settings()
        tset = sttngs.settings['twitter_api']
        api = twitter.Api(consumer_key=tset['con_secret'],
            consumer_secret=tset['con_secret_key'],
            access_token_key=tset['token'],
            access_token_secret=tset['token_key'])
        btr = block_tracker()
        blocked = btr.not_followed()
        for user in blocked:
            if time() <= sttngs.settings['last_action']:
                sleep(self.delay)
            next = time() + self.delay + randint(0, 5)
            sttngs.settings['last_action'] = next
            sttngs.save_config()
            api.CreateFriendship(screen_name=user)
            btr.now_followed(user=user)
            print '* Followed: %s' % user
        sttngs.save_config()