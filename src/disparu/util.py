import os, glob
import pandas as pd
from nicegui import ui
from .theme import frame
from functools import partial
from nicegui import app
from pathlib import Path

CSV_PATH = os.path.join(str(Path(__file__).parent), "annotations.csv")

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
    galaxy_df = galaxy_df.sort_values("Galaxy Name", ascending=True)
    
    # Split into chunks of 10 rows
    num_rows = len(galaxy_df)
    chunk_size = 10
    num_chunks = int(num_rows / chunk_size)+1
    with ui.row().classes("w-full justify-start"):
        for i in range(num_chunks):
            chunk = galaxy_df.iloc[i*chunk_size:(i+1)*chunk_size]            
            table = ui.table.from_pandas(chunk).classes('w-1/5')  # Adjust width if needed

            table.add_slot(
                    'body-cell-title',
                    r'<td><a :href="props.row.url">{{ props.row.title }}</a></td>'
                    )
            table.on(
                    'rowClick',
                    lambda e: ui.navigate.to(
                        f'/sciimg_{e.args[1]["Galaxy Name"]}'
                        )                 
                    )

def _generate_table(images_dir):
    #print(images_dir)
    data = {"Galaxy Name":[]}
    for dirname in glob.glob(images_dir):
        data["Galaxy Name"].append(os.path.basename(dirname).split('_')[-1])

    return pd.DataFrame(data)

def load_annotations():
    if os.path.exists(CSV_PATH):
        annotations = pd.read_csv(CSV_PATH)
        annotations.index = annotations.image
        annotations = annotations.fillna('')
        return annotations
    else:
        return pd.DataFrame(columns=["galaxy", "image", "follow_up", "comment"])

def save_annotations(df):
    df.to_csv(CSV_PATH, index=False)
