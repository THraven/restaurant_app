#!/bin/python
"""when the main.py file is run the application will start and run the window."""

import sys
import requests as rq
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from components import components as comp

class Handler():
    """the event handler for the app"""

    # these fields are for addItem to work
    items = {}
    def addItem(self, *args):
        builder = args[2]
        item = args[1][1]
        
        # creating item labels
        orderGrid = builder.get_object("OrderList")
        itemname = Gtk.Label(item["name"])
        price = Gtk.Label(item["price"])

        # attaching the items to the ticket and showing them
        orderGrid.attach(itemname, 0, 0, 1, 1)
        orderGrid.attach(price, 1, 0, 1, 1)
        orderGrid.show_all()

    def kill(self, *args):
        """this will en the main thread of the window thus closing it and ending the program"""
        Gtk.main_quit()


if __name__ == "__main__":
    """will parse the .glade file and parse it into something gtk can use,
    then will launch the window."""
    # this is where the builder is loaded and given the .glade file

    builder = Gtk.Builder()
    builder.add_from_file("xml/main_window_gtk.glade")
    # the Handler class is profided as the event handler
    builder.connect_signals(Handler())
    hand = Handler()

    # setting the main window and setting it to fullscreen
    window = builder.get_object("MainWindow")
    window.fullscreen()

    itemGrid = builder.get_object("itemGrid")
    orderGrid = builder.get_object("OrderList")

    # calling to the api of the webserver to get all the categories
    categories = rq.get(
        'http://185.224.89.248/api/categories/getall?key=WLkdBrcdsgtwKJRFYyyh4j2D9SmzwXRbu94GCpXEsM5dUZGkWrM3ffunXgzN').json()
    for category in enumerate(categories):
        comp.categoryLabel(itemGrid, category[1]["name"], category[0])
        # getting the items that belong with the category
        items = rq.get(
            'http://185.224.89.248/api/products/find/%s?key=WLkdBrcdsgtwKJRFYyyh4j2D9SmzwXRbu94GCpXEsM5dUZGkWrM3ffunXgzN' % category[1]["id"]).json()
        for item in enumerate(items):
            button = comp.itemButtons(orderGrid, itemGrid, item[1], item[1]["category"], item[0])
            button.connect("clicked", hand.addItem, item, builder)

    # here the window to gotten out of the builder and the main loop is started
    window = builder.get_object("MainWindow")
    window.show_all()
    Gtk.main()
