

import argparse
import modules.style

from modules.style import error

from modules.utils import is_installed
from modules.repository import Repository
from modules.arguments import ParseArgs

if __name__ == "__main__":
    repo = Repository()

    args = ParseArgs()
    if args.debug_flag:
        modules.style.DEBUG = True
        
    if args.refresh_flag:
        repo.refresh()
    
    if args.clean_flag:
        repo.clear_cache()

    if args.install is not None:
        if is_installed("git") is False:
            error("Git not installed")
        
        for pkg in args.install.packages:
            repo.install(pkg, args.install.alias_option, args.install.clone_flag)
