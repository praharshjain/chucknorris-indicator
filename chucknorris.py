import os
import signal
import json
from urllib2 import Request, urlopen, URLError
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify


APPINDICATOR_ID = 'Chuck Norris'

def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, os.path.abspath('icon.png'), appindicator.IndicatorCategory.APPLICATION_STATUS)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify.init(APPINDICATOR_ID)
    gtk.main()

def build_menu():
    menu = gtk.Menu()
    item_joke = gtk.MenuItem('Fetch a fact')
    item_joke.connect('activate', joke)
    menu.append(item_joke)
    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu

def fetch_joke():
    try:
        request = Request('http://api.icndb.com/jokes/random?limitTo=[nerdy]')
        joke = json.loads(urlopen(request).read())['value']['joke']
    except:
        joke = 'Raise your standards to get a Chuck Norris fact!'
    return joke

def joke(_):
    notify.Notification.new("Joke", fetch_joke(), os.path.abspath('icon.png')).show()

def quit(_):
    notify.uninit()
    gtk.main_quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()