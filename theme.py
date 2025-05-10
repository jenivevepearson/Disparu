import os
from contextlib import contextmanager
from pathlib import Path
from nicegui import ui, app

@contextmanager
def frame(drawer=None):
    dark = ui.dark_mode()
    ui.query("body").style(
        "font-family: 'Inter var', -apple-system, BlinkMacSystemFont, Segoe UI, "
        "Roboto, Helvetica, Arial, sans-serif, Apple Color Emoji, "
        "Segoe UI Emoji, Segoe UI Symbol"
    )
    ui.query(".body--light").style(f"background-color: #f8f2ef")

    def _toggle_dark(*args):
        dark.toggle()

        if dark.value:
            ui.query(".body--dark").style(f"background-color: #121212")
            footer.classes(remove="text-dark", add="text-white")
        else:
            ui.query(".body--light").style(f"background-color: #f8f2ef")
            footer.classes(remove="text-white", add="text-dark")

    with ui.header(elevated=False).classes("q-pa-none").style("background-color: #7d170a; color: white"):
        with ui.element("q-toolbar").classes("background-color: #7d170a; color: white"):
            # with ui.element("q-img"):
            
            if drawer is not None:
                ui.button(on_click=drawer.toggle).props(
                    "flat round dense icon=menu"
                ).classes("text-white q-mr-sm")

                ui.separator().props("dark vertical inset").classes("q-mr-sm")

            with ui.button().props("flat").classes("text-white"):
                ui.link("Home", "/").classes(replace="")
    
            ui.element("q-space")

            #with ui.button().props("flat").classes("text-white"):
            #    ui.link("Log in", "/").classes(replace="")

            #with ui.button().props("flat").classes("text-white"):
            #    ui.link("Register", "/").classes(replace="")

            ui.separator().props("dark vertical inset").classes("q-mx-sm")

            ui.button(on_click=_toggle_dark).props(
                "flat round dense icon=dark_mode"
            ).classes("text-white")

    with ui.footer(fixed=False).classes(
        "transparent text-dark border-t flex-center"
    ) as footer:  # "transparent border-t text-dark q-px-md q-mx-md"):
        ui.label("Copyright Disparu 2025")

    with ui.column().classes("w-full p-8 lg:p-16 max-w-[1250px] mx-auto"):
        yield
