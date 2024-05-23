import requests
import tqdm
import json
import pathlib
import time

from modules.style import info
from modules.spinner import Spinner

from thefuzz import process

from typing import TypedDict

CONFIG_DIR = pathlib.Path.home() / ".local" / "share" / "xtremepkg"
CONFIG_DIR.mkdir(exist_ok=True)

API_URL="https://api.github.com/users/XtremeTHN/repos"

class Package(TypedDict):
    name: str
    url: str
    description: str
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
                    "last_update_date": repo["updated_at"]
                })
            
            with self.file.open("w") as f:
                json.dump(repo_content, f)
            
            self.repo = repo_content
            
        info("Done")
    
    def get_package(self, name) -> Package | None:
        # pkg_names = list(map(lambda pkg: pkg["name"], self.repo))
        pkg = list(filter(lambda pkg: name == pkg["name"], self.repo))
        if len(pkg) == 0:
            return None
        else:
            return pkg