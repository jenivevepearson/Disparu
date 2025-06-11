import os
import argparse

from nicegui import ui, app
from disparu.disparu import *
from disparu.candidates import *
from disparu.img_pages import *

def main():

    ui.run(
        title = 'Disparu', # sets the title of the tab
        favicon = '',
        dark = False, # inherits dark mode from the computer settings
        port = 8081,
    )

if __name__ in {"__main__", "__mp_main__"}:
    main()
