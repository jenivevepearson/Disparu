import os, glob
import pandas as pd
from nicegui import ui
from .theme import frame
from functools import partial
from nicegui import app
from .util import (
    update_check,
    update_comment,
    _post_table,
    _generate_table,
    load_annotations,
    save_annotations,
    CSV_PATH
)

print("Defining /candidates route")
@ui.page("/candidates")
async def followup_pages():
    # global annotations
    annotations = load_annotations()
    imsize = 72
    #print('follow up loading')
    
    with frame():
        ui.label(f"Candidates for Follow-up").classes("text-h1")
        followup_df = annotations[annotations["follow_up"]==True]
        img_paths = followup_df['image']
        #print(img_paths)
        with ui.grid(columns=1).classes("w-full"):
            for img in img_paths:
                try:
                    existing = annotations.loc[img]
                    saved_follow_up = bool(existing["follow_up"])
                    saved_comment = str(existing["comment"])
                    galaxyname = str(existing["galaxy"])
                except KeyError:
                    # this is because the item doesn't exist in the df
                    #saved_follow_up = False
                    #saved_comment = ""
                    print('error: trying to pull source not in dataframe')
                    continue
                follow_up_value = saved_follow_up
                comment_value = saved_comment
                #print(follow_up_value)     
                with ui.row().classes("w-full items-center justify-between"):
                    web_path = img.replace('static/images', '/images')
                    ui.image(web_path).classes("max-w-[80%] h-auto object-contain")
                    #img_path = ui.label(img).classes("text-h3")
                    with ui.column().classes("items-center gap-0"):
                        ui.label(f"{img.split('_')[-4].split('/')[-1]}").classes("text-h5")
                        ui.label(f"{img.split('_')[-3].split('/')[-1][:2]}: {img.split('_')[-3].split('/')[-1][2:]}").classes("text-sm  m-0 p-0")
                        ui.label(f"{img.split('_')[-2].split('/')[-1][:3]}: {img.split('_')[-2].split('/')[-1][3:]}").classes("text-sm  m-0 p-0")
                        ui.label("Follow up?").classes("text-sm text-gray-600")
                        checkbox = ui.checkbox(
                                value=follow_up_value,
                                on_change=lambda e, img=img: update_check(img, e.sender, galaxyname)
                                ) 
                        comment_input = ui.input(label='Comments', value=comment_value)
                        # Use partial to bind img, checkbox, comment_input values at definition time
                        comment_input.on("blur", partial(update_comment, img, comment_input, galaxyname))
