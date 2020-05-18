import cx_Freeze
import sys

executables = [cx_Freeze.Executable("Simulation.py")]

base = None
if sys.platform == "win32":
    base = "Win32GUI"

cx_Freeze.setup(  name = "guifoo",
        version = "0.1",
        description = "My GUI application!",
        options = {"build_exe":{"packages":["numpy", "pygame", "pandas",
         "matplotlib", "pickle", "path", "random", "noise", "sklearn.linear_model", "tkinter"], "include_files":[]}},
        executables = executables)