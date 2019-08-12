from gui import *
import sys
import logging
import os

# Plugin name
PLUGIN_NAME = 'Autopath'
DEBUG = False
ROLL_LOGS = False

# For holding module globals
globals = sys.modules[__name__]
globals.gui = None


def gui_update():
    if globals.gui is not None:
        globals.gui.update()


def setup_logger():
    # Logging
    globals.dir_path = os.path.dirname(os.path.realpath(__file__))
    globals.logger = logging.getLogger("edmc-autopath")
    globals.logger.setLevel(logging.DEBUG)
    globals.log_file = os.path.join(globals.dir_path, 'edmc-autopath.log')

    # Roll log files
    if os.path.exists(globals.log_file) and ROLL_LOGS:
        i = 1
        while os.path.exists(os.path.join(globals.dir_path, os.path.basename(globals.log_file) + "." + str(i) + ".log")):
            i = i + 1
        os.rename(globals.log_file, os.path.join(globals.dir_path, os.path.basename(globals.log_file) + "." + str(i) + ".log"))

    fh = logging.FileHandler(globals.log_file, "a")
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s: %(message)s", "%d.%m.%Y %H:%M:%S")
    fh.setFormatter(formatter)
    globals.logger.addHandler(fh)

    # Enable
    globals.logger.disabled = not DEBUG



def plugin_start(plugin_dir):
    """
    Load this plugin into EDMC
    """

    # Logging
    setup_logger()

    globals.current_system = ""
    globals.last_system = ""
    print('{}: PLUGIN STARTED'.format(PLUGIN_NAME))
    globals.logger.info('{}: PLUGIN STARTED'.format(PLUGIN_NAME))


def plugin_stop():
    """
    EDMC is closing
    """
    globals.logger.info('{}: PLUGIN DISABLED'.format(PLUGIN_NAME))
    globals.logger.info('*************************************************************')
    print('{}: PLUGIN DISABLED'.format(PLUGIN_NAME))

def plugin_app(parent):
    """
    Creates plugin's GUI frame and returns it
    :param parent: EDMC parent frame
    :return: created frame
    """
    globals.logger.debug("Creating GUI...")
    globals.gui = MainGUI(parent, globals)
    return globals.gui


def plugin_prefs(parent, cmdr, is_beta):
   """
   Return a TK Frame for adding to the EDMC settings dialog.
   """
   globals.logger.debug("Creating settings GUI...")
   return PrefGUI.create_gui(parent, gui_update, globals)


def dashboard_entry(cmdr, is_beta, entry):
    globals.logger.debug("Dashboard entry received")
    pass


def cmdr_data(data, is_beta):
    globals.logger.debug("CMDR DATA received")

    # Update current system
    if "lastSystem" in data.keys():
        dct = data["lastSystem"]
        if "name" in dct.keys():
            new = dct["name"]
            if len(globals.current_system) < 1:
                globals.current_system = new
            else:
                globals.last_system = globals.current_system
                globals.current_system = new
                globals.neutron.update_location(globals.current_system)


def journal_entry(cmdr, is_beta, system, station, entry, state):
    globals.logger.debug("Journal entry received")

    # Update current system
    if entry is not None and entry["event"].lower() in ("fsdjump","startup"):
        if len(globals.current_system) < 1:
            globals.current_system = entry["StarSystem"]
        else:
            globals.last_system = globals.current_system
            globals.current_system = entry["StarSystem"]
            globals.neutron.update_location(globals.current_system)
