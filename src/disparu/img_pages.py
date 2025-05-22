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

@ui.page("/{galaxyname}")
async def galaxy_pages(galaxyname):
    global annotations
    annotations = load_annotations()
    imsize = 72
    #print('loading')

    with frame():
        ui.label(f"{galaxyname.split('_')[-1]}").classes("text-h1")
        
        img_paths = glob.glob(os.path.join(
            str(Path(__file__).parent),
            f"static/images/{galaxyname}/*"
        ))
        with ui.grid(columns=1).classes("w-full"):
            for img in img_paths:
                try:
                    existing = annotations.loc[img]
                    saved_follow_up = bool(existing["follow_up"])
                    saved_comment = str(existing["comment"])  
                except KeyError:
                    # this is because the item doesn't exist in the df
                    saved_follow_up = False
                    saved_comment = ""
                    
                follow_up_value = saved_follow_up
                comment_value = saved_comment
                #print(follow_up_value)
                with ui.row().classes("w-full items-center justify-between"):
                    web_path = img #img.replace('static/images', '/images')
                    ui.image(web_path).classes("max-w-[80%] h-auto object-contain")
                    #img_path = ui.label(img).classes("text-h3")
                    with ui.column().classes("items-center"):
                        ui.label(f"{img.split('_')[-1].split('.')[0].replace('r', 'r ').replace('s', 'S')}").classes("text-h4")
                        ui.label("Follow up?").classes("text-sm text-gray-600")
                        checkbox = ui.checkbox(
                            value=follow_up_value,
                            on_change=lambda e, img=img: update_check(img, e.sender, galaxyname)
                        )
                        comment_input = ui.input(label='Comments', value=comment_value)
                        # Use partial to bind img, checkbox, comment_input values at definition time
                        comment_input.on("blur", partial(update_comment, img, comment_input, galaxyname))


