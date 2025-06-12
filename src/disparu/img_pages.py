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
    #global annotations
    annotations = load_annotations()
    imsize = 72
    chunk_size=200
    #print('loading')

    #grab order of images, sorted by magnitude
    order_file = os.path.join(str(Path(__file__).parent), f"static/images/{galaxyname}/{galaxyname}_order.txt")
    
    # Get all image paths
    img_paths = glob.glob(os.path.join(str(Path(__file__).parent), f"static/images/{galaxyname}/*.png"))

    # Try to load order from file
    if os.path.exists(order_file):
        with open(order_file, 'r') as f:
            ordered_filenames = [line.strip() for line in f if line.strip()]
            img_paths_dict = {os.path.basename(p): p for p in img_paths}
            
            # Filter and sort using the mag order
            img_paths = [img_paths_dict[fn] for fn in ordered_filenames if fn in img_paths_dict]
    else:
        # Fallback: sort image paths by name
        img_paths = sorted(img_paths)

    # make image paths relative
    img_paths = [os.path.relpath(p, start=str(Path(__file__).parent)) for p in img_paths]

    total_pages = (len(img_paths) + chunk_size - 1) // chunk_size

    #current_page = ui.number(label='Current Page', value=1, min=1, max=total_pages, step=1).props('readonly').classes('hidden')
    #image_container = ui.column().classes("w-full")

    def render_page():
        image_container.clear()
        start = (current_page.value - 1) * chunk_size
        end = start + chunk_size
        for img in img_paths[start:end]:
            try:
                existing = annotations.loc[img]
                saved_follow_up = bool(existing["follow_up"])
                saved_comment = str(existing["comment"])
            except KeyError:
                saved_follow_up = False
                saved_comment = ""

            with image_container:
                with ui.row().classes("w-full items-center justify-between"):
                    web_path = img.replace('static/', '/')
                    ui.image(web_path).classes("max-w-[80%] h-auto object-contain")
                    with ui.column().classes("items-center"):
                        ui.label(f"{img.split('_')[-1].split('.')[0].replace('r', 'r ').replace('s', 'S')}").classes("text-h4")
                        ui.label("Follow up?").classes("text-sm text-gray-600")
                        ui.checkbox(
                            value=saved_follow_up,
                            on_change=lambda e, img=img: update_check(img, e.sender, galaxyname)
                        )
                        comment_input = ui.input(label='Comments', value=saved_comment)
                        comment_input.on("blur", partial(update_comment, img, comment_input, galaxyname))
    

    def pagination_controls():
        with ui.row().classes("justify-center items-center gap-4"):
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
        ui.label(f"{galaxyname.split('_')[-1]}").classes("text-h1")

        # Hidden value holder
        current_page = ui.number(value=1, min=1, max=total_pages, step=1).props('readonly').classes('hidden')

        # Top pagination
        pagination_controls()

        # Image block
        image_container = ui.column().classes("w-full")
        render_page()

        # Bottom pagination
        pagination_controls()   
