# Using Josua Schmid's HTML table parser, under AGPL v.3

from html.parser import HTMLParser
import pandas as pd
from http.cookiejar import Cookie, CookieJar, LWPCookieJar, MozillaCookieJar
import os, sys, urllib
import sqlite3 as db
from io import StringIO
from pathlib import Path

FIREFOX_DIR = Path(os.path.expanduser('~'), '.mozilla', 'firefox')
OUTPUT = 'cookies.txt'
CONTENTS = 'host, path, isSecure, expiry, name, value'


class HTMLTableParser(HTMLParser):
    """ This class serves as a html table parser. It is able to parse multiple
    tables which you feed in. You can access the result per .tables field.
    """
    def __init__(
        self,
        decode_html_entities=False,
        data_separator=' ',
    ):

        HTMLParser.__init__(self)

        self._parse_html_entities = decode_html_entities
        self._data_separator = data_separator

        self._in_td = False
        self._in_th = False
        self._current_table = []
        self._current_row = []
        self._current_cell = []
        self.tables = []

    def handle_starttag(self, tag, attrs):
        """ We need to remember the opening point for the content of interest.
        The other tags (<table>, <tr>) are only handled at the closing point.
        """
        if tag == 'td':
            self._in_td = True
        if tag == 'th':
            self._in_th = True

    def handle_data(self, data):
        """ This is where we save content to a cell """
        if self._in_td or self._in_th:
            self._current_cell.append(data.strip())

    def handle_charref(self, name):
        """ Handle HTML encoded characters """

        if self._parse_html_entities:
            self.handle_data(self.unescape('&#{};'.format(name)))

    def handle_endtag(self, tag):
        """ Here we exit the tags. If the closing tag is </tr>, we know that we
        can save our currently parsed cells to the current table as a row and
        prepare for a new row. If the closing tag is </table>, we save the
        current table and prepare for a new one.
        """
        if tag == 'td':
            self._in_td = False
        elif tag == 'th':
            self._in_th = False

        if tag in ['td', 'th']:
            final_cell = self._data_separator.join(self._current_cell).strip()
            self._current_row.append(final_cell)
            self._current_cell = []
        elif tag == 'tr':
            self._current_table.append(self._current_row)
            self._current_row = []
        elif tag == 'table':
            self.tables.append(self._current_table)
            self._current_table = []


def get_summary_by_team(target):
    cj = CookieJar()
    cookie_db = get_cookie_db_path(str(FIREFOX_DIR))
    conn = db.connect(cookie_db)
    cursor = conn.cursor()
    sql = "SELECT {c} FROM moz_cookies WHERE host LIKE '%{h}%'".format(c=CONTENTS, h=host)
    cursor.execute(sql)

    for item in cursor.fetchall():
        c = Cookie(0, item[4], item[5],
            None, False,
            item[0], item[0].startswith('.'), item[0].startswith('.'),
            item[1], False,
            item[2],
            item[3], item[3]=="",
            None, None, {})
        #print c
        cj.set_cookie(c)
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    response = opener.open(target)
    xhtml = response.read().decode("utf-8")
    #req = urllib.request.Request(url=target)
    #f = urllib.request.urlopen(req)
    #xhtml = f.read().decode("utf-8")
    return html_to_pd(xhtml, 2)

def html_to_pd(html, idx):
    p = HTMLTableParser()
    p.feed(html)
    return pd.DataFrame.from_dict(p.tables[idx])


def get_cookie_db_path(firefox_dir):
    for e in os.listdir(firefox_dir):
        if e.endswith('.default'):
            p = Path(firefox_dir, e, 'cookies.sqlite')
            if not p.is_file():
                print("Error: the file '{0}' doesn't exist".format(str(p)))
                sys.exit(1)
            else:
                return str(p)
    # else
    print("Error: the user dir. was not found in '{0}'".format(firefox_dir))
    sys.exit(1)

def get_cookies_in_cookiejar(host):
    """Export cookies and put them in a cookiejar.
    Return value: a cookiejar filled with cookies."""
    # based on http://www.guyrutenberg.com/2010/11/27/building-cookiejar-out-of-firefoxs-cookies-sqlite/
    cj = MozillaCookieJar() 
    cookie_db = get_cookie_db_path(str(FIREFOX_DIR))
    conn = db.connect(cookie_db)
    cursor = conn.cursor()
    sql = "SELECT {c} FROM moz_cookies WHERE host LIKE '%{h}%'".format(c=CONTENTS, h=host)
    cursor.execute(sql)

    for item in cursor.fetchall():
        c = Cookie(0, item[4], item[5],
            None, False,
            item[0], item[0].startswith('.'), item[0].startswith('.'),
            item[1], False,
            item[2],
            item[3], item[3]=="",
            None, None, {})
        #print c
        cj.set_cookie(c)

    return cj


## Using cookies
#host = "profootballfocus.com"
#target = "https://www.profootballfocus.com/data/by_team.php"
#print(get_cookies_in_cookiejar(host))
#print(get_summary_by_team(target))

##HTTPSBasicAuth -- doesn't work
#import requests
#from requests.auth import HTTPBasicAuth
#content = requests.get("https://www.profootballfocus.com/data/by_team.php", auth=HTTPBasicAuth("JamiePats", "791PEAsGkuNp")).content
#print (html_to_pd(content.decode("utf-8"), 0))

#FROM FILE
#f = open("one-on-one-stat-v-gid-3406-winnerteamid-19.html", "rb")
#print (html_to_pd(f.read().decode("utf-8"), 3))
