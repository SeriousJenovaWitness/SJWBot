'''
SEE ../LICENCE.TXT FOR LICENSING DETAILS
'''

import requests
from os import path
import sqlite3 as lite

from settings import settings

class block_tracker(object):
    def __init__(self, target=None, database='tracker.db'):
        self.target = target
        self.users = []
        self.database = database
        if target is None:
            self.target = 'https://raw.githubusercontent.com/sstjohn/sjwautoblocker/master/block_names.txt'
        self.build_db()

    def build_list(self):
        data = None
        r = requests.get(self.target)
        if r.status_code == 200:
            data = r.text
        if data is not None:
            data = [ x for x in data.split('\n') if x not in [ '' ] ]
            self.users = data

    def build_db(self):
        if path.exists(self.database) is not True:
            print '* Creating a new database for tracking purposes.'
            con = lite.connect(self.database)
            with con:
                cur = con.cursor()
                sql = 'CREATE TABLE follows (Name TEXT, Followed INT)'
                cur.execute(sql)
                sql = 'CREATE UNIQUE INDEX IF NOT EXISTS TwitterUnique ON follows (Name)'
                cur.execute(sql)
                con.commit()

    def check_list(self):
        con = lite.connect(self.database)
        with con:
            cur = con.cursor()
            sql = 'INSERT OR IGNORE INTO follows (Name, Followed) VALUES (?, 0)'
            cur.executemany(sql, [(x, ) for x in self.users])
            con.commit()

    def not_followed(self):
        con = lite.connect(self.database)
        with con:
            cur = con.cursor()
            sql = 'SELECT Name FROM follows WHERE Followed = 0 LIMIT 100'
            cur.execute(sql)
            return [ x[0] for x in cur.fetchall() ]

    def now_followed(self, user):
        con = lite.connect(self.database)
        with con:
            cur = con.cursor()
            sql = 'UPDATE follows SET Followed = 1 WHERE Name = ?'
            cur.execute(sql, (user,))
            con.commit()
