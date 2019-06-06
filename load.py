from autopath import Autopath
from plotter import Plotter
import sys
import pprint

# Plugin name
PLUGIN_NAME = 'Autopath'
# For holding module globals
this = sys.modules[__name__]


def plugin_start(plugin_dir):
    """
    Load this plugin into EDMC
    """
    this.current_system = ""
    this.last_system = ""
    this.plotter = Plotter()
    this.plugin = Autopath(this)
    print('{}: PLUGIN STARTED'.format(PLUGIN_NAME))


def plugin_stop():
    """
    EDMC is closing
    """
    del this.autopath
    print('{}: PLUGIN DISABLED'.format(PLUGIN_NAME))


def plugin_app(parrent):
    return this.plugin.create_gui(parrent)


def journal_entry(cmdr, is_beta, system, station, entry, state):
    if entry is not None and entry["event"].lower() in ("fsdjump","startup"):
        if len(this.current_system) < 1:
            this.current_system = entry["StarSystem"]
        else:
            this.last_system = this.current_system
            this.current_system = entry["StarSystem"]
            this.plugin.update_clipboard(this.current_system)