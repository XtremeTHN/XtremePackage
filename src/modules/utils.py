import threading
import sys
import os

from shutil import which
from pathlib import Path
from subprocess import Popen
from modules.style import error, warn

def non_blocking(func):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()

        return thread
    
    return wrapper

def is_nuitka_installed():
    try:
        import nuitka as _
        return True
    except ModuleNotFoundError:
        return False

def is_installed(cmd):
    return True if which(cmd) is not None else False

def check_pyversion():
    vi = sys.version_info
    version = int(f"{vi[0]}{vi[1]}")
    if version > 311:
        warn("Nuitka may compile incorrectly when python version is upper than 3.11. Downgrade python or use pyenv")

def get_main_file_python(path: Path) -> str:
    files = [str(p) for p in path.glob("**/*.py") if p.name == "main.py"]
    if len(files) > 1:
        # Gets the size of all file paths on project root
        k = [len(x.split("/")) for x in files]

        # Return the root main file
        return files[k.index(min(k))]
    
    return files[0]

def exec_cmd(args: list, wd=None, env=None) -> bool:
    with Popen(args=args, cwd=wd, stdout=sys.stdout, stderr=sys.stderr, env=env) as proc:
        proc.communicate()
        if (exit_code:=proc.poll()) > 0:
            error(args[0],  "returned", exit_code == 0)
    
def exec_on_venv(args: list, venv_path: str, wd: str, executable=None):
    _env = {
        "VIRTUAL_ENV": venv_path,
        "PATH": f"{venv_path}/bin:{os.environ['PATH']}"
    }
    
    exec_cmd(args, wd, env=_env)