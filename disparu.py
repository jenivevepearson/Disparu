import os, glob
import pandas as pd
from nicegui import ui
from theme import frame

################################
# THE NICEGUI PAGE DEFINITIONS #
################################

@ui.page("/")
async def home():
    galaxy_df = _generate_table("static/images/*")
    with frame():
        ui.label("Welcome to Disparu!").classes("text-h1")
        
        _post_table(galaxy_df)
                
@ui.page("/{galaxyname}")
async def galaxy_pages(galaxyname):

    imsize=128
    with frame():
        ui.label(f"{galaxyname}").classes("text-h1")

        img_paths = glob.glob(f"static/images/{galaxyname}/*")
        with ui.grid(columns=16, rows=len(img_paths)).classes("gap-0 no-wrap w-full"):
            for img in img_paths:
                ui.image(img).classes(f"w-full col-span-14")
                ui.checkbox().classes("col-span-2")
        
##################################
# HELPER FUNCTIONS FOR THE PAGES #
##################################
def _post_table(galaxy_df):

    table = ui.table.from_pandas(galaxy_df).classes('width-100')
    table.add_slot(
        'body-cell-title',
        r'<td><a :href="props.row.url">{{ props.row.title }}</a></td>'
    )
    table.on(
        'rowClick',
        lambda e : ui.navigate.to(
               f'/{e.args[1]["Galaxy Name"]}'
            )
    )

def _generate_table(images_dir):

    data = {"Galaxy Name":[]}
    for dirname in glob.glob(images_dir):
        data["Galaxy Name"].append(os.path.basename(dirname))

    return pd.DataFrame(data)
