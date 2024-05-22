import argparse
from modules.repository import Repository
parser = argparse.ArgumentParser(prog="xpkg", description="A package manager for all my projects")

parser.add_argument("-r", "--refresh", dest="refresh", help="Refresh the database")

subparser = parser.add_subparsers(help="The operation you wanna perform")

install = subparser.add_parser("install", help="Installs a package")

install.add_argument("PACKAGE", nargs=1, help="The package name you wanna install")

args = parser.parse_args()

if __name__ == "__main__":
    if args.refresh:
        Repository().refresh_repo()
