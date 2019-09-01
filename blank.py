import Tkinter as tk

class Blank(tk.Frame):

    def __init__(self, master, global_data, **kw):
        tk.Frame.__init__(self, master, **kw)
        self.globals = global_data
        self.globals.blank = self
        self.setup()

    def setup(self):
        pass