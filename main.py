import sys
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class Handler():
    """the event handler for the app"""

    def kill(self, *args):
        """this will en the main thread of the window thus closing it and ending the program"""
        Gtk.main_quit()


# this is where the builder is loaded and given the .glade file
builder = Gtk.Builder()
builder.add_from_file("xml/main_window_gtk.glade")
# the Handler class is profided as the event handler
builder.connect_signals(Handler())


# here the window to gotten out of the builder and the main loop is started
window = builder.get_object("MainWindow")
window.show_all()
Gtk.main()

# if __name__ == "__main__":
#     run = app()
