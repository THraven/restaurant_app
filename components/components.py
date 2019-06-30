#!/bin/python
"""This file contains all the components used in the app such as buttons that have to be made after loading the .glade file"""

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import sys

class categoryLabel(Gtk.Label):
    """this is for the labels with the category name on them on the top of the selection menu."""

    def __init__(self, grid, text, column):
        """takes three args
        grid: the gird it is suposed to put the label on.
        text: the text that will apear on the label.
        column: the column the where the label will apear.
        """
        Gtk.Label.__init__(self, "")
        self.set_text(text)
        grid.attach(self, column, 0, 1, 1)

class itemButtons(Gtk.Button):
    """this will put a button in the item grid with the name of the item it represents,
    the button will also add that item to the order."""

    # price of the item
    price = 0
    # name of the item
    item = ""

    def __init__(self, grid, text, column, row):
        """takes four args
        grid: the grid it is suposed to put the button on.
        text: the text on the button (this will be the name of the item).
        column: the column under which it should sit.
        row: the row the item should apear on.
        """
        Gtk.Button.__init__(self, "")
        # label = Gtk.Label(text)
        # label.set_padding(10,10)
        self.set_label(text)
        self.set_size_request(100, 80)
        grid.attach(self, column - 1, row + 1, 1, 1)
        self.connect("clicked", lambda q=text: self.addItem(q))
