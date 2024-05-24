import threading
import sys
import os

from shutil import which
from pathlib import Path
from subprocess import Popen

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

def get_main_file_python(path: Path) -> str:
    # files = list(filter(lambda x: x.split("/")[-1] == "main.py", glob.glob(str(path / "**" / "*.py"), recursive=True)))
    files = [str(p) for p in path.glob("**/*.py") if p.name == "main.py"]
    if len(files) > 1:
        # k = list(map(lambda x: len(x.split("/")), files))
        k = [len(x.split("/")) for x in files]
        return files[k.index(min(k))]
    
    return files[0]

def check_exit_successfully(args: list, wd=None) -> bool:
    # args = [which(args[0]) or args[0], *args]
    with Popen(args=args, cwd=wd, stdout=sys.stdout, stderr=sys.stderr) as proc:
        proc.communicate()
        return proc.poll() == 0
    
def exec_on_venv(args: list, venv_path: str, wd: str):
    _env = {
        "VIRTUAL_ENV": venv_path,
        "PATH": f"{venv_path}/bin:{os.environ['PATH']}"
    }
    
    with Popen(args=args, cwd=wd, stdout=sys.stdout, stderr=sys.stderr, env=_env) as proc:
        proc.communicate()
        return proc.poll() == 0
    