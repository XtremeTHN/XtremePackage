import argparse
import modules.style


from modules.style import info, warn, error
from modules.utils import is_nuitka_installed, is_installed
from modules.repository import Repository

parser = argparse.ArgumentParser(prog="xpkg", description="A package manager for all my projects")

parser.add_argument("-r", "--refresh", dest="refresh", action="store_true", help="Refresh the database")
parser.add_argument("-d", "--debug", action="store_true", help="Shows where info messages where called, also show debug messages")

subparser = parser.add_subparsers(help="The operation you wanna perform")

install = subparser.add_parser("install", help="Installs a package")

install.add_argument("PACKAGE", help="The package name you wanna install")

args = parser.parse_args()

if __name__ == "__main__":
    repo = Repository()
    if args.debug:
        modules.style.DEBUG = True
        
    if args.refresh:
        repo.refresh_repo()

    if (pkg:=getattr(args, "PACKAGE", "")) != "":
        if is_nuitka_installed() is False:
            warn("Python compiler (nuitka) not installed. If a python package doesn't have a build script, the install will fail")
        
        if is_installed("git") is False:
            error("Git not installed")
        
        github_pkg = repo.install(pkg)