import modules.style

from modules.style import error, pretty_string, colored_string, bold

from modules.utils import is_installed
from modules.repository import Repository
from modules.arguments import ParseArgs

from pathlib import Path

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
        if (n := args.install.bin_dir) is not None:
            bin_dir = Path(n)
            if bin_dir.exists() is False:
                error(f"Bin directory '{bin_dir}' doesn't exist")
            if bin_dir.is_dir() is False:
                error(f"Bin directory '{bin_dir}' is not a directory")

            LOCAL_BIN_DIR = bin_dir

        if (n := args.install.share_dir) is not None:
            share_dir = Path(n)
            if share_dir.exists() is False:
                error(f"Share directory '{share_dir}' doesn't exist")
            if share_dir.is_dir() is False:
                error(f"Share directory '{share_dir}' is not a directory")

            SHARE_DIR = share_dir

        if is_installed("git") is False:
            error("Git not installed")
        
        for pkg in args.install.packages:
            repo.install(pkg, args.install.alias_option, args.install.clone_flag, args.install.force_flag)

    if args.uninstall is not None:
        for pkg in args.uninstall.packages:
            repo.uninstall(pkg)
    
    if args.list_ is True:
        repo.display_installed_pkgs()

    repo.save_installed_pkgs()