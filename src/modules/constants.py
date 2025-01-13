import pathlib

CONFIG_DIR = pathlib.Path.home() / ".local" / "share" / "xtremepkg"
CONFIG_DIR.mkdir(exist_ok=True)

CACHE_DIR = pathlib.Path.home() / ".cache" / "xtremepkg"
LOCAL_BIN_DIR = pathlib.Path.home() / ".local" / "bin"
SHARE_DIR = pathlib.Path.home() / ".local" / "share"

API_URL="https://api.github.com/users/XtremeTHN/repos"