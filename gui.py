import ttk
import Tkinter as tk
from config import config
import myNotebook as nb
from ttkHyperlinkLabel import HyperlinkLabel
import types
from neutron import Neutron
from riches import Riches


class MainGUI(tk.Frame):
    """
    For new page:
        Set new ID for that page
        Create setup function to create menu and page
        You can see how its done in setup_neutron for example
    """

    def __init__(self, master, global_data, **kw):
        self.NEUTRON_ID = 1
        self.RICHES_ID = 2

        tk.Frame.__init__(self, master, **kw)
        self.main_frame = None
        self.menu_frame = None
        self.globals = global_data
        self.pages = dict()
        self.menu_buttons = dict()
        self.page_active = 0
        self.setup()
        self.update()

    def setup(self):
        """
        Creates main frame and menu frame
        :return:
        """
        # Plugin's frame
        self.globals.logger.debug("Creating GUI's main frame...")
        self.main_frame = tk.Frame(self, borderwidth=2, relief="flat")
        self.main_frame.pack(side="top", fill="both", expand=True, padx=0, pady=0)
        self.globals.logger.debug("GUI's main frame created")

        # Plugin's menu frame
        self.globals.logger.debug("Creating GUI's menu frame..")
        self.menu_frame = tk.Frame(self.main_frame, borderwidth=0, highlightthickness=0)
        self.setup_riches()
        self.setup_neutron()
        self.menu_frame.pack(side="top", fill="both", expand=True, anchor="w")
        self.globals.logger.debug("GUI's menu frame created.")

    def setup_neutron(self):
        """
        Creates Neutron Plotter GUI
        """

        self.globals.logger.debug("Creating neutron plotter frame GUI...")

        # MENU
        ID = self.NEUTRON_ID
        self.menu_buttons[ID] = tk.Button(self.menu_frame, text="Neutron", relief=tk.FLAT,
                                                   command=lambda page=ID: self.page(page))

        # PAGE
        self.pages[ID] = Neutron(self.main_frame, self.globals)

        self.globals.logger.debug("Neutron plotter frame GUI created.")

    def setup_riches(self):
        """
        Creates Road to Riches GUI
        :return:
        """

        self.globals.logger.debug("Creating road to riches frame GUI...")

        # MENU
        ID = self.RICHES_ID
        self.menu_buttons[ID] = tk.Button(self.menu_frame, text="Riches", relief=tk.FLAT,
                                                   command=lambda page=ID: self.page(page))

        # PAGE
        self.pages[ID] = Riches(self.main_frame, self.globals)

        self.globals.logger.debug("Neutron road to riches GUI created.")

    def update(self):
        self.globals.logger.debug("Updating GUI")

        # Are pages enabled
        neutron = config.getint("autopath_neutron") # page 1
        riches = config.getint("autopath_riches")   # page 2

        # Menu column
        column = 0
        button_len = 0

        # Hide all buttons
        self.globals.logger.debug("Hiding all menu buttons")
        for button in self.menu_buttons.values():
            button.grid_forget()
        self.globals.logger.debug("Menu buttons hidden.")



        # Neutron button shown
        if neutron:
            button_len = button_len + 1
            self.globals.logger.debug("Neutron plotter menu button shown.")
            self.menu_buttons[self.NEUTRON_ID].grid(row=0, column=column)
            column = column + 1
            if self.page_active == 0:
                self.page_active = self.NEUTRON_ID
        else:
            if self.page_active == self.NEUTRON_ID:
                self.page_active = 0

        # Road to riches button shown
        # Todo: Road to riches unimplememted so hardcode disabled
        if riches and False:
            button_len = button_len + 1
            self.globals.logger.debug("Road to riches menu button shown")
            self.menu_buttons[self.RICHES_ID].grid(row=0, column=column)
            column = column + 1
            if self.page_active == 0:
                self.page_active = self.RICHES_ID
        else:
            if self.page_active == self.RICHES_ID:
                self.page_active = 0


        self.menu_frame.pack_forget()
        if button_len > 2:
            self.menu_frame.pack(side="top", fill="both", expand=True, anchor="w")

        # Hide all pages
        self.globals.logger.debug("Hide all pages")
        for page in self.pages.values():
            page.pack_forget()
        self.globals.logger.debug("All pages hidden.")

        # Show page
        self.globals.logger.debug("Trying to show page number " + str(self.page_active))
        if self.page_active in self.pages.keys():
            self.globals.logger.debug("Page " + str(self.page_active) + " exist, enabled")
            self.pages[self.page_active].pack(side="top", fill="both", expand=True, anchor="w")

    def page(self, page):
        self.globals.logger.debug("Changing GUI page to " + str(page))
        self.page_active = page
        self.update()


class PrefGUI:
    # Settings for pref layout
    PADX = 10
    BUTTONX = 12

    # Storage for checkboxes
    neutron = tk.IntVar(value=config.getint('autopath_neutron'))
    riches = tk.IntVar(value=config.getint('autopath_riches'))
    clipboard = tk.IntVar(value=config.getint('autopath_clipboard'))
    overlay = tk.IntVar(value=config.getint('autopath_overlay'))

    @staticmethod
    def create_gui(parent, update_func, globals):
        """
        Create plugin's preference GUI
        :param parent: parent frame
        :param gui:
        :return: plugin's preference GUI
        """

        # Settings frame
        frame = nb.Frame(parent)
        frame.columnconfigure(1, weight=1)

        # Headline label
        globals.logger.debug("Creating settings hyperling label..")
        HyperlinkLabel(frame, text='EDMC: Autopath', background=nb.Label().cget('background'),
                       url='https://github.com/Sognus/EDMC-Autopath', underline=True).grid(columnspan=2,
                                                                                           padx=PrefGUI.PADX,
                                                                                           sticky=tk.W)

        globals.logger.debug("Settings hyperlink label created.")

        # Checkbox for Road To Riches
        globals.logger.debug("Creating settings neutron plotter checkbox...")
        neutron_button = nb.Checkbutton(frame, text=_('Enable neutron plotter feature'), variable=PrefGUI.neutron,
                                        command=lambda update_func=update_func: PrefGUI.prefs_changed(update_func))
        neutron_button.grid(columnspan=2, padx=PrefGUI.BUTTONX, pady=(5, 0), sticky=tk.W)
        globals.logger.debug("Settings neutron plotter created.")

        # Checkbox for Road To Riches
        globals.logger.debug("Creating settings road to riches checkbox")
        riches_button = nb.Checkbutton(frame, text=_('Enable road to riches feature'), variable=PrefGUI.riches,
                                       command=lambda update_func=update_func: PrefGUI.prefs_changed(update_func, globals))
        riches_button.grid(columnspan=2, padx=PrefGUI.BUTTONX, pady=(5, 0), sticky=tk.W)
        globals.logger.debug("Settings road to riches created")

        # Checkbox for Copy to Clipboard
        globals.logger.debug("Creating settings copy to clipboard checkbox")
        clipboard_button = nb.Checkbutton(frame, text=_('Copy next waypoint to clipboard'), variable=PrefGUI.clipboard,
                                       command=lambda update_func=update_func: PrefGUI.prefs_changed(update_func, globals))
        clipboard_button.grid(columnspan=2, padx=PrefGUI.BUTTONX, pady=(5, 0), sticky=tk.W)
        globals.logger.debug("Settings copy to clipboard created")

        # Checkbox for Overlay
        globals.logger.debug("Creating settings overlay checkbox")
        overlay_button = nb.Checkbutton(frame, text=_('Use EDMCOverlay (if installed)'), variable=PrefGUI.overlay,
                                          command=lambda update_func=update_func: PrefGUI.prefs_changed(update_func,
                                                                                                        globals))
        overlay_button.grid(columnspan=2, padx=PrefGUI.BUTTONX, pady=(5, 0), sticky=tk.W)
        globals.logger.debug("Settings overlay created")


        return frame

    @staticmethod
    def prefs_changed(update_func=None, globals=None):
        """
        Save changes to config storage (whatever is used - windows registers or file)
        If update func is set, func will be called
        :return: None
        """
        globals.logger.debug("Saving settings..")
        config.set("autopath_neutron", PrefGUI.neutron.get())
        config.set("autopath_riches",  PrefGUI.riches.get())
        config.set("autopath_clipboard", PrefGUI.clipboard.get())
        config.set("autopath_overlay", PrefGUI.overlay.get())
        globals.logger.debug("Settings saved.")

        if update_func is not None and isinstance(update_func, types.FunctionType):
            globals.logger.debug("Calling GUI update function...")
            update_func()
            globals.logger.debug("GUI update function completed")
