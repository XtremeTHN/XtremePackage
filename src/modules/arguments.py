import sys
from pathlib import Path
from modules.constants import LOCAL_BIN_DIR, SHARE_DIR
from modules.style import underlined, bold, info, error

class InstallArguments:
    clone_flag: bool
    alias_option: str | None

    bin_dir: str
    share_dir: str
    
    packages: list[str]

    def __init__(self) -> None:
        self.clone_flag = False
        self.alias_option = None
        self.packages = []

        self.bin_dir = str(LOCAL_BIN_DIR)
        self.share_dir = str(SHARE_DIR)

class Arguments:
    refresh_flag: bool
    clean_flag: bool
    debug_flag: bool
    
    install: InstallArguments | None
    
    def __init__(self) -> None:
        self.install = None
        self.refresh_flag = False
        self.clean_flag = False
        self.debug_flag = False
    
def print_usage():
    print(f"{underlined(bold('Usage:'))} {sys.argv[0]} [-h] [-r] [-c] [-d] OPERATION")

def print_install_help():
    print(f"{underlined(bold('Usage:'))} {sys.argv[0]} [FLAGS] install [-a ALIAS] [--bin-directory PATH] [--share-directory PATH] [-c] PACKAGES")
    
    print(bold(underlined("Flags:")))
    print("\t-h, --help         Prints this help message.")
    print("\t-r, --refresh      Refresh the repository.")
    print("\t-c, --clone        Only clone the repository.")
    print("\t--bin-directory    Sets the bin directory. Default: ~/.local/bin")
    print("\t--share-directory  Sets the share directory. Default: ~/.local/share")

    print("Positional arguments:")
    print("\tPACKAGES          The packages to install.")

def print_help():
    print_usage()
    print("\nA package manager for all my projects\n")
    
    print(bold(underlined("Commands:")))
    print("\tinstall:           Installs a package\n")
    
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
            
            case "-r" | "--refresh":
                res.refresh_flag = True
            
            case "-c" | "--clean":
                res.clean_flag = True
            
            case "-d" | "--debug":
                res.debug_flag = True
                
            case "install":
                install_args = InstallArguments()
                
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

                            install_args.alias_option = value
                            double_continue = True
                            continue
                            
                        case "-h" | "--help":
                            print_install_help()
                        
                        case "-c" | "--clone":
                            install_args.clone_flag = True
                        
                        case "-r" | "--refresh":
                            res.refresh_flag = True
                            
                        case "-d" | "--debug":
                            res.debug_flag = True
                        
                        case "--bin-directory":
                            install_args.bin_dir = get_value(_index, iargs, err_msg="Expected bin directory")
                        
                        case "--share-directory":
                            install_args.share_dir = get_value(_index, iargs, err_msg="Expected share directory")
                        
                        case _:
                            install_args.packages.append(arg)
                if len(install_args.packages) == 0:
                    error("Expected at least one package")
                res.install = install_args
                break

            case _:
                error("Unknown command/option")     
    return res
