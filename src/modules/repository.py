import requests
import json
import shutil

from modules.style import info, warn, error, debug
from modules.spinner import Spinner
from modules.utils import exec_cmd
from modules.constants import CACHE_DIR, CONFIG_DIR, API_URL

from modules.projects import PythonProject, ValaProject

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
        
    def install(self, pkg: Package | str, pkg_name=None, clone=False):        
        github_pkg = self.get_package(pkg)
        if pkg_name is not None:
            if github_pkg["language"] != "python":
                error("Alias option is only available when installing python packages")
        
        package_name = pkg_name or pkg.lower()
        print(package_name)
            
        if github_pkg is None:
            error(f'No package named "{pkg}"')
            
        if shutil.which(package_name) is not None and clone is False:
            error("There's a executable in PATH with the same name of the package. Uninstall it, or specify the package name in the arguments")
            
        dest = CACHE_DIR / package_name
        if dest.exists() is False:
            info("Cloning repository...")
            exec_cmd(["git", "clone", github_pkg["url"], str(dest)])
            
        if clone is True:
            return
        else:
            if (dest / ".git").exists() is False:
                error(f"The repository exists, but it's not a git repo\nRemove this folder and execute the xpkg command again:\nRepo path: {dest}")
        
        match github_pkg["language"].lower():
            case "python":
                python = PythonProject(dest, package_name)
                python.setup()
                python.install()
    
            case 'vala':
                vala = ValaProject(dest, package_name)
                vala.setup()
                vala.install()
                build_dir = dest / "build"

                
        info(f'Installed package "{pkg}" with name "{package_name}"')
        
    def get_package(self, name) -> Package | None:
        pkg = list(filter(lambda pkg: name == pkg["name"], self.repo))
        if len(pkg) == 0:
            return None
        else:
            return pkg[0]
