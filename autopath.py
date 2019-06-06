from Tkinter import DoubleVar
from plotter import Plotter
import pyperclip
import Tkinter as tk
import ttk


class Autopath:

    def __init__(self, pointer):
        # Pre-Init
        self.pointer = pointer
        self.plotter = pointer.plotter
        self.frame = None
        self.label_origin = None
        self.separator = None
        self.entry_origin = None
        self.entry_destination = None
        self.label_efficiency = None
        self.entry_efficiency = None
        self.button_calculate = None
        self.label_range = None
        self.entry_range = None
        self.route = list()
        self.route_ready = False
        self.label_status = None
        self.checkbox_clipboard = None
        self.checkbox_status = None
        pass

    def update_clipboard(self, arrived_to):
        # Check none
        if self.checkbox_status is not None or self.checkbox_clipboard is None:
            # Check for route ready and checkbox
            if self.route_ready and self.checkbox_status.get() == 1:
                try:
                    index = self.route.index(arrived_to)
                    pyperclip.copy(self.route[index+1])
                    self.update_status("Clipboard updated to: ")
                    self.status_append(self.route[index+1])
                except:
                    # Ignore errors
                    pass

    def calculate_path(self):
        origin = self.entry_origin.get()
        dest = self.entry_destination.get()
        eff = -1
        range = -1.0

        self.update_status("")

        try:
            eff = int(self.entry_efficiency.get())
            range = float(self.entry_range.get())
        except ValueError:
            pass

        # If origin is empty, use current system
        if len(origin) < 1:
            origin = self.pointer.current_system

        # Check for data validation
        if len(origin) < 1:
            self.status_append("ERROR: Origin must not be empty!")
        if len(dest) < 1:
            self.status_append("ERROR: Destination must not be empty!")
        if eff < 1 or eff > 100:
            self.status_append("ERROR: Efficiency must be number between 1 and 100!")
        if range < 0:
            self.status_append("ERROR: Range must be decimal and not empty!")

        # Check for errors
        if len(self.label_status["text"]) > 0:
            self.route_ready = False
            return False

        self.update_status("Calculating..")

        # request calculation
        route = self.plotter.request_calculation(origin, dest, eff, range)

        self.update_status("Processing data..")

        # Process json for system names
        self.route = list()
        for record in route["result"]["system_jumps"]:
            self.route.append(record["system"])

        # Mark as ready
        if len(self.route) > 0:
            self.update_status("Route calculated..")
            self.route_ready = True
            # simulate arrive to origin system
            self.update_clipboard(self.route[0])
        else:
            self.update_status("ERROR: Route has less than one system")
            self.route_ready = False

    def status_append(self, status_text):
        if self.label_status is not None:
            self.label_status["text"] = self.label_status["text"] + "\n" + status_text
            self.label_status.update()

    def update_status(self, status_text):
        if self.label_status is not None:
            self.label_status["text"] = status_text
            self.label_status.update()

    def create_gui(self, parrent):
        # Unified width
        width = 16

        # Frame
        self.frame = tk.Frame(parrent)

        # Label origin
        self.label_origin = tk.Label(self.frame, text="Origin: ", justify=tk.LEFT)
        self.label_origin.grid(row=0, column=0, sticky=tk.W, pady=(10, 0))

        # Entry origin
        self.entry_origin = tk.Entry(self.frame, width=width)
        self.entry_origin.grid(row=0, column=1, sticky=tk.E, pady=(10, 0))
        self.entry_origin.update()

        # Label origin
        self.label_origin = tk.Label(self.frame, text="Destination: ", justify=tk.LEFT)
        self.label_origin.grid(row=1, column=0, sticky=tk.W, )

        # Entry destination
        self.entry_destination = tk.Entry(self.frame, width=width)
        self.entry_destination.grid(row=1, column=1, sticky=tk.E)
        self.entry_destination.update()

        # Label range
        self.label_range = tk.Label(self.frame, text="Range (LY): ", justify=tk.LEFT)
        self.label_range.grid(row=2, column=0, sticky=tk.W)

        # Entry range
        range_default = tk.DoubleVar(value=50.0)
        self.entry_range = tk.Entry(self.frame, width=width, textvariable=range_default)
        self.entry_range.grid(row=2, column=1, sticky=tk.E)
        self.entry_range.update()

        # Label efficiency
        self.label_efficiency = tk.Label(self.frame, text="Efficiency (%): ", justify=tk.LEFT)
        self.label_efficiency.grid(row=3, column=0, sticky=tk.W)

        # Efficiency entry
        efficiency_default = tk.IntVar(value=60)
        self.entry_efficiency = tk.Spinbox(self.frame, from_=1, to=100, width=width - 2, textvariable=efficiency_default)
        self.entry_efficiency.grid(row=3, column=1, sticky=tk.E)

        # Checkbox clipboard
        self.checkbox_status = tk.IntVar(value=1)
        self.checkbox_clipboard = tk.Checkbutton(self.frame, text="autoclipboard", variable=self.checkbox_status)
        self.checkbox_clipboard.grid(row=4, column=0, columnspan=2, sticky=tk.W)

        # Button
        self.button_calculate = tk.Button(self.frame, text="Calculate", command=self.calculate_path)
        self.button_calculate.grid(row=5, column=0, columnspan=2, pady=(3, 0))

        # Label Status
        self.label_status = tk.Label(self.frame, text="Ready.. ", justify=tk.CENTER)
        self.label_status.grid(row=6, column=0, columnspan=2, pady=(0,10))

        # Frame layout
        self.frame.columnconfigure(6, weight=1)
        
        return self.frame
