from shutil import which
from subprocess import Popen
import sys
import os

def exec_on_venv(args: list, venv_path: str):
    # args = [which(args[0]) or args[0], *args]
    _env = {
        "VIRTUAL_ENV": venv_path,
        "PATH": f"{venv_path}/bin:{os.environ['PATH']}"
    }
    
    with Popen(args=args, stdout=sys.stdout, stderr=sys.stderr, env=_env) as proc:
        proc.communicate()
        return proc.poll() == 0
    
    
exec_on_venv(["python3", "-m", "pip", "install", "halo"], "/home/axel/Documents/Projects/LinuxProjects/XtremePackage/.venv")