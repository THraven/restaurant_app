#!/bin/python
# -*- coding: utf-8 -*-
"""when the main.py file is run the application will start and run the window."""

import sys
import requests as rq
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from components import components as comp

class Handler():
    """the event handler for the app"""

    # these fields are for setTable to work
    table = 0
    def setTable(self, *args):
        """this is for setting the table number"""
        self.table = args[0].get_text()


    # these fields are for addItem to work
    # total is for the total price
    total = 0.00
    # order is for containing all the data regarding the order
    order = {}
    def addItem(self, *args):
        """will add a item to the order ticket"""
        builder = args[2]
        item = args[1][1]

        # setting the total price
        self.total += float(item["price"])
        totalPrice = builder.get_object("totalPrice")
        totalPrice.set_text("    totaal prijs: €%.2f" % self.total)

        # checking if that item already exists
        if item["name"] in self.order:
            idx = item["name"]
            self.order[idx]["amount"] += 1
            self.order[idx]["amountLabel"].set_text(str(self.order[idx]["amount"]))
            self.order[idx]["price"] = "%.2f" % (float(item["price"]) * int(self.order[idx]["amount"]))
            self.order[idx]["priceLabel"].set_text(self.order[idx]["price"])
        else:
            # creating item labels
            orderGrid = builder.get_object("OrderList")
            itemname = Gtk.Label(item["name"])
            price = Gtk.Label(item["price"])
            amount = Gtk.Label(1)

            # attaching the items to the ticket and showing them
            orderGrid.attach(amount, 0, len(self.order) +1 , 1, 1)
            orderGrid.attach(itemname, 1, len(self.order) + 1, 1, 1)
            orderGrid.attach(price, 2, len(self.order) + 1, 1, 1)
            orderGrid.show_all()

            # setting up the order field
            self.order.update({item["name"]: {"id": item["id"],
                                             "itemLabel": itemname,
                                             "amountLabel": amount,
                                             "amount": 1,
                                             "priceLabel": price,
                                             "price": item["price"],
                                             }})

    def kill(self, *args):
        """this will en the main thread of the window thus closing it and ending the program"""
        Gtk.main_quit()

    def finish(self, *args):
        """this will finish the order, send it to the database and then clear the ticket"""
        order = ""
        # stringing all the id together into a string array
        for i in self.order:
            order += "%s," % self.order[i]["id"] * self.order[i]["amount"]
        order = order[:-2]
        # sending a get requist to the api to take my hot date in its database
        r = rq.get("""http://185.224.89.248/api/tickets/add?tableNum=%s&waiter=kassa&order=[%s]&key=WLkdBrcdsgtwKJRFYyyh4j2D9SmzwXRbu94GCpXEsM5dUZGkWrM3ffunXgzN""" % (self.table, order))
        for i in self.order:
            self.order[i]["itemLabel"].destroy()
            self.order[i]["amountLabel"].destroy()
            self.order[i]["priceLabel"].destroy()
        self.order.clear()
        self.total = 0.00
        totalPrice = builder.get_object("totalPrice")
        totalPrice.set_text("    totaal prijs: €%.2f" % self.total)


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
