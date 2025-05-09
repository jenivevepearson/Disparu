import os, glob
import pandas as pd
from nicegui import ui
from theme import frame
from functools import partial
from nicegui import app
app.add_static_files('/images', 'static/images')

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
                existing = annotations[
                    (annotations["galaxy"] == galaxyname) &
                    (annotations["image"] == img)
                ]
                saved_follow_up = bool(existing["follow_up"].values[0]) if not existing.empty else False
                saved_comment = str(existing["comment"].values[0]) if not existing.empty else ""

                # Variables that store current values for this image
                follow_up_value = saved_follow_up
                comment_value = saved_comment

                with ui.row().classes("w-full items-center justify-between"):
                    web_path = img.replace('static/images', '/images')
                    ui.image(web_path).classes("max-w-[80%] h-auto object-contain")
                    with ui.column().classes("items-center"):
                        ui.label("Follow up?").classes("text-sm text-gray-600")
                        check_update_func = partial(update_annotation, img_path=img, comment_input=comment_value, galaxyname=galaxyname)
                        checkbox = ui.checkbox(value=follow_up_value, on_change=lambda e: check_update_func(value=e.sender.value))
                        comment_input = ui.input(label='Comments', value=comment_value)


                        # Use partial to bind img, checkbox, comment_input values at definition time
                        #checkbox.on("change", partial(update_annotation, img, checkbox, comment_input))
                        comment_input.on("blur", partial(update_annotation, img, checkbox.value, comment_input, galaxyname))


##################################
# HELPER FUNCTIONS FOR THE PAGES #
##################################
def update_annotation(img_path, value, comment_input, galaxyname):
    global annotations
    if type(comment_input) is str:
        comment_value=comment_input
    else:
        comment_value = comment_input.value
    new_row = {
                "galaxy": galaxyname,
                "image": img_path,
                "follow_up": value,
                "comment": comment_value}
    print(f"Updating annotation for {img_path}: {new_row}")
    annotations = annotations[
                    ~((annotations["galaxy"] == galaxyname) &
                    (annotations["image"] == img_path))
                    ]
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

CSV_PATH = "./annotations.csv"

def load_annotations():
    if os.path.exists(CSV_PATH):
        return pd.read_csv(CSV_PATH)
    else:
        return pd.DataFrame(columns=["galaxy", "image", "follow_up", "comment"])

def save_annotations(df):
    df.to_csv(CSV_PATH, index=False)
