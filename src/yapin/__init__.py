"""yapin: the Yapin' bot library for Python.

This package is a thin layer over `yapper.py` (https://github.com/our-websites/yapper.py): `import yapin` gives you
everything `import yapper` does, so the two can be used interchangeably. On top of that it keeps the older
`YAPIN_BOT_TOKEN` variable and `YapinError` name working.
"""
import os as _os

# A .env next to your bot can hold YAPIN_BOT_TOKEN (or YAPPER_BOT_TOKEN); the folder you run from, and its parents,
# are searched. Variables already set in the environment win over the file.
try:
    from dotenv import find_dotenv as _find_dotenv, load_dotenv as _load_dotenv
except ImportError:
    pass
else:
    _load_dotenv(_find_dotenv(usecwd=True))

# yapper reads YAPPER_BOT_TOKEN; accept YAPIN_BOT_TOKEN as well.
if not _os.environ.get("YAPPER_BOT_TOKEN") and _os.environ.get("YAPIN_BOT_TOKEN"):
    _os.environ["YAPPER_BOT_TOKEN"] = _os.environ["YAPIN_BOT_TOKEN"]

# Import from yapper.main (not the yapper package): it lists the whole public API in __all__ in every release.
from yapper import main as _main
from yapper.main import *  # noqa: F401,F403
from yapper.main import YapperError, __version__

YapinError = YapperError  # the name this package used before it was built on yapper.py

__all__ = [*_main.__all__, "YapinError", "__version__"]
