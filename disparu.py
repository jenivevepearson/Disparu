import os, glob
import pandas as pd
from nicegui import ui
from theme import frame
from functools import partial
from nicegui import app
app.add_static_files('/images', 'static/images')

CSV_PATH = "./annotations.csv"

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
    global annotations
    annotations = load_annotations()
    imsize = 256

    with frame():
        ui.label(f"{galaxyname}").classes("text-h1")
        
        img_paths = glob.glob(f"static/images/{galaxyname}/*")
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
                print(follow_up_value)
                with ui.row().classes("w-full items-center justify-between"):
                    web_path = img.replace('static/images', '/images')
                    ui.image(web_path).classes("max-w-[80%] h-auto object-contain")
                    img_path = ui.label(img).classes("text-h3")
                    with ui.column().classes("items-center"):
                        ui.label("Follow up?").classes("text-sm text-gray-600")
                        checkbox = ui.checkbox(
                            value=follow_up_value,
                            on_change=lambda e, img=img_path.text: update_check(img, e.sender, galaxyname)
                        )
                        comment_input = ui.input(label='Comments', value=comment_value)

                        # Use partial to bind img, checkbox, comment_input values at definition time
                        comment_input.on("blur", partial(update_comment, img, comment_input, galaxyname))


##################################
# HELPER FUNCTIONS FOR THE PAGES #
##################################
def update_check(img_path, check_value, galaxyname):
    """
    update the checkbox state in annotations
    """
    global annotations
    annotations = load_annotations()
    if img_path in annotations.index:
        annotations.loc[img_path, "follow_up"] = check_value.value
    else:
        new_row = {
            "galaxy": galaxyname,
            "image": img_path,
            "follow_up": check_value.value,
            "comment": ""
        }
        annotations = pd.concat([annotations, pd.DataFrame([new_row])], ignore_index=True)
    save_annotations(annotations)
    
def update_comment(img_path, comment_input, galaxyname):
    """
    update the comment in annotations
    """
    global annotations
    annotations = load_annotations()
    if img_path in annotations.index:
        annotations.loc[img_path, "comment"] = comment_input.value
    else:
        new_row = {
            "galaxy": galaxyname,
            "image": img_path,
            "follow_up": False,
            "comment": comment_input.value
        }
        annotations = pd.concat([annotations, pd.DataFrame([new_row])], ignore_index=True)
    save_annotations(annotations)
    
def _post_table(galaxy_df):

    table = ui.table.from_pandas(galaxy_df).classes('width-500')
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

def load_annotations():
    if os.path.exists(CSV_PATH):
        annotations = pd.read_csv(CSV_PATH)
        annotations.index = annotations.image
        return annotations
    else:
        return pd.DataFrame(columns=["galaxy", "image", "follow_up", "comment"])

def save_annotations(df):
    df.to_csv(CSV_PATH, index=False)
