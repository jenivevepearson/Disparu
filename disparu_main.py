import os
import argparse

from nicegui import ui, app
from disparu.disparu import *
from disparu.candidates import *
from disparu.img_pages import *

def main():
    ui.run(
        title = 'Disparu Main',
        favicon = '',
        dark = False,
        port = 8085,
    )

if __name__ in {"__main__", "__mp_main__"}:
    main()
