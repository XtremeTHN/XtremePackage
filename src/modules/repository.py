import requests
import json
import pathlib
import shutil

import venv

from modules.style import info, warn, error
from modules.spinner import Spinner
from modules.utils import get_main_file_python, check_exit_successfully, exec_on_venv

from typing import TypedDict

from subprocess import Popen

CONFIG_DIR = pathlib.Path.home() / ".local" / "share" / "xtremepkg"
CONFIG_DIR.mkdir(exist_ok=True)

CACHE_DIR = pathlib.Path.home() / ".cache" / "xtremepkg"
LOCAL_BIN_DIR = pathlib.Path.home() / ".local" / "bin"

API_URL="https://api.github.com/users/XtremeTHN/repos"

class Package(TypedDict):
    name: str
    url: str
    description: str
    language: str
    last_update_date: str

class Repository:
    def __init__(self):
        self.file = CONFIG_DIR / "xtreme_repo.json"
        
        self.repo = None
        if not self.file.exists():
            self.refresh_repo()
        
        self.repo: list[Package] = self.repo or json.loads(self.file.read_text())
    
    def refresh_repo(self):
        info("Refreshing repo...")

        with Spinner("Waiting github response...") as spin:
            try:
                res = requests.get(API_URL).json()
            except:
                return
            
            spin.text = "Filtering data..."
            
            repo_content = []
            for repo in res:
                repo_content.append({
                    "name": repo["name"],
                    "url": repo["html_url"],
                    "description": repo["description"],
                    "language": repo["language"],
                    "last_update_date": repo["updated_at"]
                })
            
            with self.file.open("w") as f:
                json.dump(repo_content, f)
            
            self.repo = repo_content
            
        info("Done")
        
    def install(self, pkg: str):
        github_pkg = self.get_package(pkg)
        if github_pkg is None:
            error(f'No package named "{pkg}"')
            
        package_name = pkg.lower()
            
        dest = CACHE_DIR / package_name
        if dest.exists() is False:
            info("Cloning repository...")
            if check_exit_successfully(["git", "clone", github_pkg["url"], dest]) is False:
                error("Git returned non-zero exit code")
                
        else:
            if (dest / ".git").exists() is False:
                error(f"The repository exists, but it's not a git repo\nRemove this folder and execute the xpkg command again:\nRepo path: {dest}")
        
        match github_pkg["language"].lower():
            case "python":
                venv_dir = dest / ".venv"
                
                if venv_dir.exists() is False:
                    info("Making virtual environment...")
                    venv.create(str(venv_dir), symlinks=True, with_pip=True)
                
                info("Installing dependencies...")
                if exec_on_venv(["python3", "-m", "pip", "install", "nuitka", "-r", f'{dest}/requirements.txt'], venv_dir, dest) is False:
                    error("pip returned non-zero exit code")
                
                info("Detecting entry file...")
                entry_file = get_main_file_python(dest)
                info("Compiling python project with nuitka...")
                if exec_on_venv(["python3", "-m", "nuitka", "--follow-imports", entry_file, '--output-dir=build', f'--output-file={package_name}'], venv_dir, dest) is False:
                    error("nuitka returned non-zero exit code")
                
                info("Successfully compiled")
                info('Moving to ~/.local/bin ...')
                shutil.move(dest / package_name, LOCAL_BIN_DIR / package_name)
                
                info(f'Installed package "{pkg}" with name "{package_name}"')
                return
    
    def get_package(self, name) -> Package | None:
        pkg = list(filter(lambda pkg: name == pkg["name"], self.repo))
        if len(pkg) == 0:
            return None
        else:
            return pkg[0]