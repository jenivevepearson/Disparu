import os, sys
from nicegui import app
from pathlib import Path

from .disparu import *
from .candidates import *
from .util import *
from .theme import *
from .img_pages import *

if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "otter-web"
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

app.add_static_files("/images", str(Path(__file__).parent / "static/images"))

print(f"The app.route_path is set to {app.root_path}")
