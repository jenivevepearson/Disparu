import os, glob
import pandas as pd
from nicegui import ui
from theme import frame
from functools import partial

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
    annotations = load_annotations()
    imsize=256

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

                with ui.row().classes("w-full items-center justify-between"):
                    ui.image(img).classes("max-w-[80%] h-auto object-contain")
                    with ui.column().classes("items-center"):
                        ui.label("Follow up?").classes("text-sm text-gray-600")
                        follow_up = ui.checkbox(value=saved_follow_up)
                        comment = ui.input(label='Comments', value=saved_comment)

                        # Save on change
                        def update_annotation(image, checkbox, inputbox):
                            nonlocal annotations
                            new_row = {
                                "galaxy": galaxyname,
                                "image": img,
                                "follow_up": checkbox.value,
                                "comment": inputbox.value
                            }

                            # Debugging: Check the new values before saving
                            print(f"Updating annotation for {image}: {new_row}")

                            # Remove existing row if any
                            annotations = annotations[
                                ~((annotations["galaxy"] == galaxyname) &
                                  (annotations["image"] == img))
                            ]
                            annotations = pd.concat([annotations, pd.DataFrame([new_row])], ignore_index=True)
                            save_annotations(annotations)

                            # Debugging: Print the saved DataFrame
                            print(annotations)

                        follow_up.on("change", partial(update_annotation, img, follow_up, comment))
                        comment.on("blur", partial(update_annotation, img, follow_up, comment))  # Save when user finishes typing
        #with ui.grid(columns=10, rows=len(img_paths)).classes("gap-1 w-full"):
        #    for img in img_paths:
        #        ui.image(img).classes(f"w-full h-auto object-contain col-span-9")
        #        ui.checkbox().classes("col-span-1")
        
##################################
# HELPER FUNCTIONS FOR THE PAGES #
##################################
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
