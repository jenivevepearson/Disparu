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
    annotations = load_annotations()

    chunk_size = 100
    followup_df = annotations[annotations["follow_up"] == True]
    img_paths = followup_df['image'].tolist()    
    total_pages = (len(img_paths) + chunk_size - 1) // chunk_size

    def render_page():
        image_container.clear()
        start = (current_page.value - 1) * chunk_size
        end = start + chunk_size
        
        for img in img_paths[start:end]:
            try:
                existing = annotations.loc[img]
                saved_follow_up = bool(existing["follow_up"])
                saved_comment = str(existing["comment"])
                galaxyname = str(existing["galaxy"])
            except KeyError:
                print('error: trying to pull source not in dataframe')                
                continue

            with image_container:
                with ui.row().classes("w-full items-center justify-between"):
                    web_path = img.replace('static/images', '/images')
                    ui.image(web_path).classes("max-w-[80%] h-auto object-contain")
                    with ui.column().classes("items-center gap-0"):
                        ui.label(f"{img.split('_')[-4].split('/')[-1]}").classes("text-h5")
                        ui.label(f"{img.split('_')[-3].split('/')[-1][:2]}: {img.split('_')[-3].split('/')[-1][2:]}").classes("text-sm  m-0 p-0")
                        ui.label(f"{img.split('_')[-2].split('/')[-1][:3]}: {img.split('_')[-2].split('/')[-1][3:]}").classes("text-sm  m-0 p-0")
                        ui.label("Follow up?").classes("text-sm text-gray-600")
                        checkbox = ui.checkbox(
                                value=saved_follow_up,
                                on_change=lambda e, img=img: update_check(img, e.sender, galaxyname)
                                )
                        comment_input = ui.input(label='Comments', value=saved_comment)
                        comment_input.on("blur", partial(update_comment, img, comment_input, galaxyname))
                        
    def pagination_controls():
        with ui.row().classes("justify-center items-center gap-4 mt-4"):

            def prev_page():
                if current_page.value > 1:
                    current_page.value -= 1
                    render_page()
            def next_page():
                if current_page.value < total_pages:
                    current_page.value += 1                    
                    render_page()

            ui.button("Previous", on_click=prev_page).props('flat')
            ui.label().bind_text_from(current_page, 'value').classes("text-lg")
            ui.label(f"/ {total_pages}").classes("text-lg")            
            ui.button("Next", on_click=next_page).props('flat')
    
    with frame():
        ui.label(f"Candidates for Follow-up").classes("text-h1")

        # Hidden state holder
        current_page = ui.number(value=1, min=1, max=total_pages, step=1).props('readonly').classes('hidden')        
        
        pagination_controls()  # top

        image_container = ui.column().classes("w-full")        
        render_page()

        pagination_controls()  # bottom
