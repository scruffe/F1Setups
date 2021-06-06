from tkinter import Toplevel, Button, Tk, Menu


class TopMenu:
    """create menu bar"""
    def __init__(self, widgets, root):
        self.widgets = widgets
        menubar = Menu(root)
        file = Menu(menubar, tearoff=0)
        file.add_command(label="import previous setups", command=self.widgets.update.populate_db_from_setups_dir)
        file.add_command(label="Open", command=self.widgets.open_cmd)
        file.add_command(label="Save", command=self.widgets.save_cmd)
        file.add_command(label="Save as...", command=self.widgets.save_as_cmd)
        file.add_command(label="Close")

        file.add_separator()

        file.add_command(label="Exit", command=root.quit)

        menubar.add_cascade(label="File", menu=file)
        edit = Menu(menubar, tearoff=0)
        edit.add_command(label="Undo")

        edit.add_separator()

        edit.add_command(label="Cut")
        edit.add_command(label="Copy")
        edit.add_command(label="Paste")
        edit.add_command(label="Delete")
        edit.add_command(label="Select All")

        menubar.add_cascade(label="Edit", menu=edit)
        help = Menu(menubar, tearoff=0)
        help.add_command(label="Tip Scruffe", command=lambda: self.widgets.open_url("https://paypal.me/valar"))
        menubar.add_cascade(label="Donate", menu=help)

        root.config(menu=menubar)