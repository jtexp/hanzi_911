# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)
from builtins import *
from bs4 import BeautifulSoup
import requests
import codecs
import binascii
import shutil
import pprint
import tempfile

# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *
# https://commons.wikimedia.org/wiki/File:%E4%B8%89-bw.png
from anki.find import Finder
from anki.notes import Note
image_types = {'char': '', 'sequences': '-bw.png', 'shades of red': '-red.png', 'animations': '-order.gif' }
c = '三'
wiki = "https://commons.wikimedia.org/wiki/File:"
pp = pprint.PrettyPrinter(indent=4)

sdir = tempfile.mkdtemp(prefix="hanzi")


def char_url(c):
    return two_split(binascii.hexlify(c.encode('utf-8')).decode('utf-8').upper())

def two_split(s):
    t = iter(s)
    return '%'.join(a+b for a,b in zip(t, t))

def parse_wiki(url):
    header = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=header)
    soup = BeautifulSoup(r.text, 'html.parser')
    image = soup.find("div", {"class" : "fullImageLink"}).find("img")
    return image['src']

def grab_image(url):
    response = requests.get(url, stream=True)
    path = os.path.join(sdir, url.split('/')[-1])
    with open(path, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
    return path

def save_image(c):
    u = wiki + '%' + char_url(c) + image_types['sequences']
    print(u)
    image = parse_wiki(u)
    return grab_image(image)

def do(c, deck):
    return mw.col.media.addFile(save_image(c)) 

def testFunction():
    deck_name = 'c2' 
    did = mw.col.decks.id(deck_name)
    mw.col.decks.select(did)
    deck = mw.col.decks.get(did)
    print(type(deck))
    f = Finder(mw.col)
    cs = f.findNotes('deck:c2 Strokes:')
    
    
    for c in cs:
       pp.pprint(c)
       note = mw.col.getNote(c)
       items = note.items()
       pp.pprint(items)
       for (key, value) in items:
           if key == 'Hanzi':
               strokes = ''
               for c in list(note[key]):
                   path = do(c, deck)
                   
                   strokes = strokes + '<img src="{0}">'.format(path)
                   print(strokes)
           if key == 'Strokes':
               note[key] = strokes
               note.flush()

       


    # get the number of cards in the current collection, which is stored in
    # the main window
    # cardCount = mw.col.cardCount()
    # show a message box
    #showInfo("Card count: %d" % cardCount)

# create a new menu item, "test"
action = QAction("Get Hanzi Stroke Order", mw)
# set it to call testFunction when it's clicked
mw.connect(action, SIGNAL("triggered()"), testFunction)
# and add it to the tools menu
mw.form.menuTools.addAction(action)
