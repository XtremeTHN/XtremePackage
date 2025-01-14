import sys
from pathlib import Path
from modules.constants import LOCAL_BIN_DIR, SHARE_DIR
from modules.style import underlined, bold, info, error

class InstallArguments:
    clone_flag: bool
    force_flag: bool

    alias_option: str | None

    bin_dir: str
    share_dir: str
    
    packages: list[str]

    def __init__(self) -> None:
        self.clone_flag = False
        self.force_flag = False
        self.alias_option = None
        self.packages = []

        self.bin_dir = str(LOCAL_BIN_DIR)
        self.share_dir = str(SHARE_DIR)

class UninstallArguments:
    packages: list[str]

    def __init__(self) -> None:
        self.packages = []

class Arguments:
    refresh_flag: bool
    clean_flag: bool
    debug_flag: bool
    
    install: InstallArguments
    uninstall: UninstallArguments
    list_: bool
    
    def __init__(self) -> None:
        self.install = InstallArguments()
        self.uninstall = UninstallArguments()
        self.list_ = False
        self.refresh_flag = False
        self.clean_flag = False
        self.debug_flag = False
    
def print_usage():
    print(f"{underlined(bold('Usage:'))} {sys.argv[0]} [-h] [-r] [-c] [-d] OPERATION")

def print_install_help():
    print(f"{underlined(bold('Usage:'))} {sys.argv[0]} [FLAGS] install [-a ALIAS] [--bin-directory PATH] [--share-directory PATH] [-c] PACKAGES")

    print("\nInstalls a package from the repository.\n")
    print(bold(underlined("Flags:")))
    print("\t-h, --help         Prints this help message.")
    print("\t-r, --refresh      Refresh the repository.")
    print("\t-c, --clone        Only clone the repository.")
    print("\t-f, --force        Force the installation.")
    print("\t--bin-directory    Sets the bin directory. Default: ~/.local/bin")
    print("\t--share-directory  Sets the share directory. Default: ~/.local/share")

    print(bold(underlined("Positional arguments:")))
    print("\tPACKAGES          The packages to install.")

def print_uninstall_help():
    print(f"{underlined(bold('Usage:'))} {sys.argv[0]} [FLAGS] uninstall PACKAGES")

    print("\nUninstalls a package from the repository.\n")
    
    print(bold(underlined("Flags:")))
    print("\t-h, --help         Prints this help message.")

    print(bold(underlined("Positional arguments:")))
    print("\tPACKAGES          The packages to uninstall.")

def print_list_help():
    print(f"{underlined(bold('Usage:'))} {sys.argv[0]} [FLAGS] list")

    print("\nLists all installed packages.\n")
    
    print(bold(underlined("Flags:")))
    print("\t-h, --help         Prints this help message.")

def print_help():
    print_usage()
    print("\nA package manager for all my projects\n")
    
    print(bold(underlined("Commands:")))
    print("\tinstall:           Installs a package\n")
    print("\tuninstall:         Uninstalls a package\n")
    print("\tlist:              Lists all installed packages\n")
    
    print(bold(underlined("Flags:")))
    print("\t-h, --help         Prints this help message.")
    print("\t-r, --refresh      Refresh the repository.")
    print("\t-c, --clean        Cleans the cache (Removes ~/.cache/xtremepkg).")
    print("\t-d, --debug        Shows where info messages were called, also show debug messages.")
    
    print("\nThe repository resides in ~/.local/share/xtremepkg")
    
    sys.exit(0)

def get_value(index: int, args: list[str], err_msg="Expected value") -> str:
    if len(args) - 1 < index:
        error(err_msg)
    
    return args[index + 1]

# I know im reinventing the wheel, but i just wanted to create a customized argparser
def ParseArgs(args=sys.argv[1:]) -> Arguments:
    args = args
    if len(args) == 0:
        error("Specify one command")
    
    res = Arguments()
    for index, arg in enumerate(args):
        match arg:
            case "-h" | "--help":
                print_help()
                sys.exit(0)
            
            case "-r" | "--refresh":
                res.refresh_flag = True
            
            case "-c" | "--clean":
                res.clean_flag = True
            
            case "-d" | "--debug":
                res.debug_flag = True
            
            case "list":
                res.list_ = True
                iargs: list[str] = args[index + 1:]

                for _index, _arg in enumerate(iargs):
                    match _arg:
                        case "-h" | "--help":
                            print_uninstall_help()
                            sys.exit(0)
                        case _:
                            error("Unexpected argument")
                break
            
            case "uninstall":
                iargs: list[str] = args[index + 1:]

                for _index, _arg in enumerate(iargs):
                    match _arg:
                        case "-h" | "--help":
                            print_uninstall_help()
                            sys.exit(0)
                        case _:
                            res.uninstall.packages.append(_arg)
                if len(res.uninstall.packages) == 0:
                    error("Expected at least one package")
                
                break
                
            case "install":                
                double_continue = False
                iargs: list[str] = args[index + 1:]
                for _index, arg in enumerate(iargs):
                    if double_continue is True:
                        double_continue = False
                        continue
                    
                    match arg:
                        case "-a" | "--alias":
                            value = get_value(_index, iargs, err_msg="Expected alias")

                            if value.startswith("-"):
                                error("Expected alias, not a flag")

                            res.install.alias_option = value
                            double_continue = True
                            continue
                            
                        case "-h" | "--help":
                            print_install_help()
                            sys.exit(0)
                        
                        case "-c" | "--clone":
                            res.install.clone_flag = True
                        
                        case "-f" | "--force":
                            res.install.force_flag = True
                        
                        case "-r" | "--refresh":
                            res.refresh_flag = True
                            
                        case "-d" | "--debug":
                            res.debug_flag = True
                        
                        case "--bin-directory":
                            res.install.bin_dir = get_value(_index, iargs, err_msg="Expected bin directory")
                        
                        case "--share-directory":
                            res.install.share_dir = get_value(_index, iargs, err_msg="Expected share directory")
                        
                        case _:
                            res.install.packages.append(arg)
                if len(res.install.packages) == 0:
                    error("Expected at least one package")
                break

            case _:
                error("Unknown command/option")     
    return res
