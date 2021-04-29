import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk

class Open:
    """An Open File dialog
    
    Valid options: initialdir, parent, title"""

    def __init__(self, **kw):

        try: self.title = kw["title"]
        except:
            self.title = "Open File"

        try: self.initialdir = kw["initialdir"]
        except:
            self.initialdir = None

        try: self.parent = kw["parent"]
        except:
            self.parent = None
        
        # The dialog
        self.dialog = Gtk.FileChooserDialog(title=self.title, parent=self.parent, 
            action=Gtk.FileChooserAction.OPEN)
        self.dialog.add_buttons("Cancel", Gtk.ResponseType.CANCEL, "OK", Gtk.ResponseType.ACCEPT)
        self.dialog.set_action(Gtk.FileChooserAction.OPEN)
        if self.initialdir:
            self.dialog.set_current_folder(self.initialdir)
        self.dialog.set_select_multiple(False)
        self.dialog.connect("response", self.callback)

    def callback(self, dialog=None, response=None, whoknows=None):
        """The method to be called when the user responds to the file dialog."""
        self.filenames = self.dialog.get_filenames()
        self.response = response
        self.dialog.destroy()

    def show(self):
        """Show the dialog."""
        self.dialog.show()
        while self.dialog.get_mapped():
            Gtk.main_iteration()
        if self.response == Gtk.ResponseType.ACCEPT:
            return self.filenames[0]
        else:
            return None

class SaveAs:
    """A Save File As dialog.
    
    Valid options: initialdir, parent"""

    def __init__(self, **kw):

        try: self.initialdir = kw["initialdir"]
        except:
            self.initialdir = None

        try: self.parent = kw["parent"]
        except:
            self.parent = None

        self.dialog = Gtk.FileChooserDialog(parent=self.parent, 
            action=Gtk.FileChooserAction.SAVE)
        self.dialog.add_buttons("Cancel", Gtk.ResponseType.CANCEL, "Save", Gtk.ResponseType.ACCEPT)
        self.dialog.set_action(Gtk.FileChooserAction.SAVE)
        self.dialog.set_do_overwrite_confirmation(True)
        if self.initialdir:
            self.dialog.set_current_folder(self.initialdir)

        self.dialog.set_select_multiple(False)
        self.dialog.connect('response', self.callback)
        self.dialog.show()

    def callback(self, dialog=None, response=None, whoknows=None):
        """The method to be called when the user responds to the file dialog."""
        self.filenames = self.dialog.get_filenames()
        self.response = response
        self.dialog.destroy()

    def show(self):
        """Show the dialog."""
        self.dialog.show()
        while self.dialog.get_mapped():
            Gtk.main_iteration()
        if self.response == Gtk.ResponseType.ACCEPT:
            return self.filenames[0]
        else:
            return None

if __name__ == "__main__":
    window = Gtk.Window()
    window.connect("delete-event", Gtk.main_quit)
    print(Open(title="Open - Custom title", initialdir="/home/sam/").show())
    print(SaveAs(initialdir="/home/sam/").show())
    exit()