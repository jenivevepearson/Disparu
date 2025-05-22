import os, glob
import pandas as pd
from nicegui import ui
from functools import partial
from nicegui import app
from pathlib import Path

from .theme import frame
from .util import (
    update_check,
    update_comment,
    _post_table,
    _generate_table,
    load_annotations,
    save_annotations,
    CSV_PATH
)


################################
# THE NICEGUI PAGE DEFINITIONS #
################################

@ui.page("/")
async def home():
    galaxy_df = _generate_table(str(Path(__file__).parent / "static/images/sciimg*"))
    with frame():
        ui.label("Disparu:").classes("text-h1")
        ui.label("The Hunt for Failed Supernovae").classes("text-h2")
        
        _post_table(galaxy_df)
                
"""
print("Defining /test route")
@ui.page("/test")
def test_page():
    print("Test page function executing")
    with frame():
        ui.label("Test Page").classes("text-h1")
"""
