import pyperclip

try:
    # Python 2
    import Tkinter as tk
except ModuleNotFoundError:
    # Python 3
    import tkinter as tk

class Riches(tk.Frame):

    def __init__(self, master, global_data, **kw):
        tk.Frame.__init__(self, master, **kw)
        self.globals = global_data
        self.globals.neutron = self
        self.plotter = None
        self.setup()

    def setup(self):
        # Unified width
        width = 16

        self.globals.logger.debug("Riches -> Creating road to riches GUI")

        # Label origin
        self.label_origin = tk.Label(self, text="Origin: ", justify=tk.LEFT)
        self.label_origin.grid(row=0, column=0, sticky=tk.W, pady=(10, 0))

        self.globals.logger.debug("Riches -> road riches gui label origin done...")

        # Entry origin
        self.entry_origin = tk.Entry(self, width=width)
        self.entry_origin.grid(row=0, column=1, sticky=tk.E, pady=(10, 0))

        self.globals.logger.debug("Riches -> road riches gui entry origin done...")

        # Label destination
        self.label_destination = tk.Label(self, text="Destination: ", justify=tk.LEFT)
        self.label_destination.grid(row=1, column=0, sticky=tk.W)

        self.globals.logger.debug("Riches -> road riches gui label destination done...")

        # Entry destination
        self.entry_destination = tk.Entry(self, width=width)
        self.entry_destination.grid(row=1, column=1, sticky=tk.E)

        self.globals.logger.debug("Riches -> road riches gui entry destination done...")

        self.columnconfigure(6, weight=1)

        self.globals.logger.debug("Riches -> Road to riches GUI created")

