import argparse
import modules.style

from modules.style import warn, error
from modules.utils import is_nuitka_installed, is_installed
from modules.repository import Repository

parser = argparse.ArgumentParser(prog="xpkg", description="A package manager for all my projects")

parser.add_argument("-r", "--refresh", action="store_true", help="Refresh the database")
parser.add_argument("-c", "--clean", action="store_true", help="Cleans the cache")
parser.add_argument("-d", "--debug", action="store_true", help="Shows where info messages where called, also show debug messages")

subparser = parser.add_subparsers(help="The operation you wanna perform")

install = subparser.add_parser("install", help="Installs a package")

install.add_argument("PACKAGE", help="The package name you wanna install")
install.add_argument("-c", "--clone", action="store_true", help="Clone the package repository, but not installing it")
install.add_argument("-a", "--alias", help="The package alias")

args = parser.parse_args()

if __name__ == "__main__":
    repo = Repository()
    if args.debug:
        modules.style.DEBUG = True
        
    if args.refresh:
        repo.refresh_repo()
    
    if args.clean:
        repo.clear_cache()

    if (pkg:=getattr(args, "PACKAGE", "")) != "":
        if is_installed("git") is False:
            error("Git not installed")
        
        github_pkg = repo.install(pkg, args.alias, args.clone)