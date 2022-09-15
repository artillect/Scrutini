#!/Users/mtaylor/.pyenv/shims/python
"""Scrutini Main."""
import argparse
import os
import sys
import gui
from db import SCDatabase
from classes import Settings
from fbs_runtime.application_context.PyQt6 import ApplicationContext
from qt_material import apply_stylesheet
import PyQt6.QtGui as qg
import subprocess
import darkdetect
import platform

def check_appearance():
    """Checks DARK/LIGHT mode of macos."""
    cmd = 'defaults read -g AppleInterfaceStyle'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, shell=True)
    return bool(p.communicate()[0])

class AppContext(ApplicationContext):
    def run(self, db):
        result = platform.uname()
        print(result)
        mode = "light"
        if (result.system=="Darwin" and check_appearance()) or (result.system != "Darwin" and darkdetect.isDark()):
        # if darkdetect.isDark():
        # if check_appearance():
            mode = "dark"
        apply_stylesheet(self.app, theme=f"{mode}_blue.xml")
        # print(darkdetect.theme())
        window = gui.SMainWindow(self, db)
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        icon = qg.QIcon(scriptDir + os.path.sep + '../icons/mac/256.png')
        self.app.setWindowIcon(icon)
        # version = self.build_settings['version']
        window.show()
        return self.app.exec()

# initiate the parser
parser = argparse.ArgumentParser()
# parser.add_argument("-i0", "--interface0",
#                     help="Use command-line interface (0)", action="store_true")
# parser.add_argument("-i1", "--interface1",
#                     help="Use Graphical User Interface (1)",
#                     action="store_true")
parser.add_argument("-v", "--verbose", help="Prints extra information to the\
                     command line", action="store_true")
parser.add_argument("-s", "--settings", help="Use the specified config file.")
parser.add_argument("-db", "--database", help="Use the specified database.")
parser.add_argument("-o", "--open", help="Open the chosen Competition file.")
# read arguments from the command line
args = parser.parse_args()
# check for Verbose
VERBOSE = bool(args.verbose)
# check for --interface0 or -i0
# if args.interface0:
#     INTERFACE = 0
#     # import scruinterface0 as scruinterface
#     if VERBOSE:
#         print("Command-Line Interface (0)")
# else:
#     INTERFACE = 1
#     import gui
#     if VERBOSE:
#         print("GUI (1)")
# check settings and database
if args.settings and os.path.exists(args.settings):
    SETTINGS_FILE = args.settings
else:
    SETTINGS_FILE = 'config.json'

if __name__ == "__main__":
    # appctxt = ApplicationContext()
    settings = Settings(SETTINGS_FILE, VERBOSE)
    if args.database and os.path.exists(args.database):
        settings.db_file = args.database
    if VERBOSE:
        print(settings)
    scrudb = SCDatabase(settings)
    appctxt = AppContext()
    rc = appctxt.run(scrudb)
    # if INTERFACE == 0:
    #     print("Command Line Interface not available in this version.")
    #     # scruinterface.print_settings()
    #     # scruinterface.menu_main()
    # else:
    # import pdb
    # pdb.set_trace()
    # g = gui.App(scrudb)
    # g.start()
    # window = gui.SMainWindow(None, scrudb)
    # window.show()
    # rc = 0
    # rc = appctxt.app.exec()
    # rc = appctxt.app.exec()
    # del appctxt.app
    settings.write()
    if VERBOSE:
        print(f"Exit main {rc}")
    sys.exit(rc)
