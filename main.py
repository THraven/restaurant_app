#!/bin/python

import sys
import requests as rq
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from components import components as comp

class Handler():
    """the event handler for the app"""

    def kill(self, *args):
        """this will en the main thread of the window thus closing it and ending the program"""
        Gtk.main_quit()


def run():
    """will parse the .glade file and parse it into something gtk can use,
    then will launch the window."""
    # this is where the builder is loaded and given the .glade file
    builder = Gtk.Builder()
    builder.add_from_file("xml/main_window_gtk.glade")
    # the Handler class is profided as the event handler
    builder.connect_signals(Handler())

    itemGrid = builder.get_object("itemGrid")

    # calling to the api of the webserver to get all the categories
    result = rq.get(
        'http://185.224.89.248/api/categories/getall?key=WLkdBrcdsgtwKJRFYyyh4j2D9SmzwXRbu94GCpXEsM5dUZGkWrM3ffunXgzN').json()
    for i in enumerate(result):
        comp.categoryLabel(itemGrid, i[1]["name"], i[0])

    # here the window to gotten out of the builder and the main loop is started
    window = builder.get_object("MainWindow")
    window.show_all()
    Gtk.main()

if __name__ == "__main__":
    run()
