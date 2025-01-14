import requests
import json
import shutil

from modules.style import info, error, colored_string, pretty_string, bold
from modules.spinner import Spinner
from modules.utils import exec_cmd
from modules.constants import CACHE_DIR, CONFIG_DIR, API_URL

from modules.projects import Project, BuildSystem
from typing import TypedDict
from pathlib import Path

class Package(TypedDict):
    name: str
    url: str
    path: Path | None
    alias: str | None
    description: str
    language: str
    last_update_date: str

class InstalledPackage(TypedDict):
    name: str
    path: str
    alias: str | None
    description: str
    language: str
    build_system: int
    last_update_date: str

class Repository:
    def __init__(self):
        self.repo_file = CONFIG_DIR / "xtreme_repo.json"
        self.installed_pkgs_file = CONFIG_DIR / "installed_packages.json"
        
        if self.installed_pkgs_file.exists() is False:
            self.installed_pkgs_file.write_text("[]")
        
        if not self.repo_file.exists():
            self.repo = self.refresh()
        else:
            self.repo: list[Package] = json.loads(self.repo_file.read_text())
        
        self.installed_pkgs: list[InstalledPackage] = json.loads(self.installed_pkgs_file.read_text())
    
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
                    "alias": None,
                    "path": None,
                    "url": repo["html_url"],
                    "description": repo["description"],
                    "language": repo["language"],
                    "last_update_date": repo["updated_at"]
                })
            
            with self.repo_file.open("w") as f:
                json.dump(repo_content, f)
            
            info("Done")
            return repo_content
            
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
        
    def install(self, pkg: str, pkg_name=None, clone=False, force=False):        
        github_pkg = self.get_package(pkg)
        if github_pkg is None:
            error(f'No package named "{pkg}"')
            
        github_pkg["name"] = pkg.lower()
        github_pkg["alias"] = pkg_name
        
        if self.get_installed_package(pkg) is not None:
            error(f'Package "{pkg}" is already installed')
        
        if force is False:
            if shutil.which(github_pkg["name"]) is not None and clone is False:
                error("There's a executable in PATH with the same name of the package. Uninstall it, or specify the package name in the arguments")

        dest = self.clone(github_pkg, dir_name=github_pkg["name"])
        if clone is True:
            return

        github_pkg["path"] = dest

        proj = Project.from_info(github_pkg)
        proj.setup()
        proj.install()
        
        self.installed_pkgs.append({
            "name": github_pkg["name"],
            "path": str(dest),
            "alias": github_pkg["alias"],
            "description": github_pkg["description"],
            "language": github_pkg["language"],
            "build_system": proj.build_system,
            "last_update_date": github_pkg["last_update_date"]
        })

        info(f'Installed package "{pkg}"')
    
    def uninstall(self, pkg_name: str):
        pkg = self.get_installed_package(pkg_name)
        if pkg is None:
            error(f'No package named "{pkg_name}"')

        pkg["path"] = Path(pkg["path"])
        proj = Project.from_info(pkg)
        proj.uninstall()

        self.installed_pkgs.remove(pkg)
        info(f'Uninstalled package "{pkg["name"]}"')
    
    def display_installed_pkgs(self):
        print(pretty_string("Installed packages:", "white"))
        for pkg in self.installed_pkgs:
            msg = ["\t" + colored_string(bold(pkg["name"]), "green"), "last update:", pkg["last_update_date"], "\n\t" + pkg["description"] + "\n"]
            if pkg["alias"] is not None:
                msg.insert(1, "-> " + colored_string(pkg["alias"], "green"))
                msg.pop(0)
                msg.insert(0, "\t" + pkg["name"])
            print(*msg)
    
    def save_installed_pkgs(self):
        with self.installed_pkgs_file.open("w") as f:
            json.dump(self.installed_pkgs, f)
    
    def __return_first_occurrence(self, name, _list):
        pkg = list(filter(lambda pkg: name == pkg["name"] or name == pkg["alias"], _list))
        if len(pkg) == 0:
            return None
        else:
            return pkg[0]
    
    def get_installed_package(self, name) -> InstalledPackage | None:
        return self.__return_first_occurrence(name, self.installed_pkgs)
        
    def get_package(self, name) -> Package | None:
        return self.__return_first_occurrence(name, self.repo)
