import requests
import json
import shutil

from modules.style import info, warn, error, debug
from modules.spinner import Spinner
from modules.utils import exec_cmd
from modules.constants import CACHE_DIR, CONFIG_DIR, API_URL

from modules.projects import Project
from typing import TypedDict

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
            self.refresh()
        
        self.repo: list[Package] = self.repo or json.loads(self.file.read_text())
    
    def refresh(self):
        info("Refreshing repo...")

        with Spinner("Waiting github response...") as spin:
            try:
                res = requests.get(API_URL).json()
            except:
                error("Exception ocurred when trying to connect to github. Maybe you don't have internet?")
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
    
    def clear_cache(self):
        with Spinner(f"Removing {str(CACHE_DIR)}..."):
            shutil.rmtree(CACHE_DIR)
            CACHE_DIR.mkdir(exist_ok=True)
        info("Removed", str(CACHE_DIR))
    
    def clone(self, pkg: Package, dir_name=None):
        dest = CACHE_DIR / dir_name or pkg["name"]
        if dest.exists() is False:
            info("Cloning repository...")
            exec_cmd(["git", "clone", pkg["url"], str(dest)])

            if (dest / ".git").exists() is False:
                error(f"The repository exists, but it's not a git repo\nRemove this folder and execute the {__name__} command again:\nRepo path: {dest}")
        
        return dest
        
    def install(self, pkg: str, pkg_name=None, clone=False):        
        github_pkg = self.get_package(pkg)
        github_pkg["name"] = pkg.lower()
        github_pkg["alias"] = pkg_name
            
        if github_pkg is None:
            error(f'No package named "{pkg}"')
            
        if shutil.which(github_pkg["name"]) is not None and clone is False:
            error("There's a executable in PATH with the same name of the package. Uninstall it, or specify the package name in the arguments")

        dest = self.clone(github_pkg, dir_name=github_pkg["name"])
        if clone is True:
            return

        github_pkg["path"] = dest

        proj = Project.from_info(github_pkg)
        proj.setup()
        proj.install()

        info(f'Installed package "{pkg}" with name "{github_pkg["name"]}"')
        
    def get_package(self, name) -> Package | None:
        pkg = list(filter(lambda pkg: name == pkg["name"], self.repo))
        if len(pkg) == 0:
            return None
        else:
            return pkg[0]
