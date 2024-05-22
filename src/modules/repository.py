import requests
import tqdm
import json
import pathlib

from halo import Halo

CONFIG_DIR = pathlib.Path.home() / ".local" / "share" / "xtremepkg"
CONFIG_DIR.mkdir(exist_ok=True)

API_URL="https://api.github.com/users/XtremeTHN/repos"

class Repository:
    def __init__(self):
        self.file = CONFIG_DIR / "xtreme_repo.json"
        if not self.file.exists():
            self.refresh_repo()
    
    def refresh_repo(self):
        print("Refreshing repo...")
        spinner = Halo(text="Waiting github response...", spinner="dots8")
        spinner.start()

        try:
            res = requests.get(API_URL).json()
        except:
            spinner.fail("Error when refreshing repo")
            return
         
        spinner.stop_and_persist(text="Filtering data...")
        
        repo_content = []
        for repo in res:
            repo_content.append({
                "name": repo["name"],
                "url": repo["html_url"],
                "description": repo["description"],
                "last_update_date": repo["updated_at"]
            })
        
        f = self.file.open("w")
        json.dump(repo_content, f)

        f.close()
        
        spinner.info("Done")
