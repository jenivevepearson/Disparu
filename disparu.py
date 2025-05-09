from nicegui import ui
from theme import frame

################################
# THE NICEGUI PAGE DEFINITIONS #
################################

@ui.page("/")
async def home():
    with frame():
        ui.label("Welcome to Disparu!")

    
        
@ui.page("/{galaxyname}")
async def galaxy_pages(galaxyname):

    with frame():
        ui.label(f"{galaxyname}")
    
##################################
# HELPER FUNCTIONS FOR THE PAGES #
##################################
def _post_table(galaxy_df):

    table = ui.table.from_pandas(df).classes('max-h-40')
    table.add_slot(
        'body-cell-title',
        r'<td><a :href="props.row.url">{{ props.row.title }}</a></td>'
    )
    table.on(
        'rowClick',
        lambda e : ui.navigate.to(
               f'/{e.args[1]["name"]}'
            )
    )
