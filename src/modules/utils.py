import threading
import sys
import os

from shutil import which
from pathlib import Path
from subprocess import Popen
from modules.style import error, warn, pretty_string

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

def exec_cmd(args: list, wd=None, env=None, exit_on_error=True):
    if isinstance(wd, Path):
        wd = str(wd)
        
    with Popen(args=args, cwd=wd, stdout=sys.stdout, stderr=sys.stderr, env=env) as proc:
        print(pretty_string("+", "green"), " ".join(args))
        proc.communicate()
        if (exit_code:=proc.poll()) > 0:
            if exit_on_error is True:
                error(args[0],  "returned", exit_code)
            else:
                return exit_code
    