import os
import argparse

from nicegui import ui, app
from disparu import *

def main():
    
    ui.run(
        title = 'Disparu', # sets the title of the tab
        favicon = '',
        dark = False, # inherits dark mode from the computer settings
    )

if __name__ in {"__main__", "__mp_main__"}:
    main()
