#!/bin/python
"""This file contains all the components used in the app such as buttons that have to be made after loading the grid"""

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import sys

class categoryLabel(Gtk.Label):
    """this is for the labels with the category name on them on the top of the ."""

    def __init__(self, grid, text, column):
        Gtk.Label.__init__(self, "")
        self.set_text(text)
        grid.attach(self, column, 0, 1, 1)
