'''
SEE LICENCE.TXT FOR LICENSING DETAILS
'''

from time import sleep

from ggbot.blocked import block_tracker
from ggbot.social import manage_twitter

def main():
    blckd = block_tracker()
    print '* Retrieving the most recent Jenova Witness protection list.'
    blckd.build_list()
    print '* Checking to see if we have new followers to work with.'
    blckd.check_list()
    print '* Now working to see what we can do for them.'
    mgtwit = manage_twitter()
    if mgtwit.valid_api() is not True:
        print '! Please edit the newly created config file. Exiting...\n'
        exit(1)
    else:
        print '* Attempting to follow the newly converted...\n'
        mgtwit.new_follow()

if __name__ == '__main__':
    while True:
        main()
        sleep(60)