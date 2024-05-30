import sys
from modules.style import underlined, bold, info, error

class Debug:
    ...
    
class InstallArguments(Debug):
    clone_flag: bool
    alias_option: str | None
    help_flag: bool
    
    packages: list[str]

class Arguments:
    refresh_flag: bool
    clean_flag: bool
    clone_flag: bool
    debug_flag: bool
    
    install: InstallArguments | None
    
    def __init__(self) -> None:
        pass
    
def print_usage():
    print(f"{underlined(bold('Usage:'))} [-h] [-r] [-c] [-d] OPERATION")

def print_help():
    print_usage()
    print("\nA package manager for all my projects\n")
    
    print(bold(underlined("Commands:")))
    print("\tinstall: Installs a package")
    print("\trepository: Repository related utilities\n")
    
    print(bold(underlined("Flags:")))
    print("\t-h, --help         Prints this help message.")
    print("\t-r, --refresh      Refresh the repository.")
    print("\t-c, --clean        Cleans the cache (Removes ~/.cache/xtremepkg).")
    print("\t-d, --debug        Shows where info messages were called, also show debug messages.")
    sys.exit(0)


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
                install_args.packages = []
                
                double_continue = False
                iargs = args[index + 1:]
                for _index, arg in enumerate(iargs):
                    if double_continue is True:
                        double_continue = False
                        continue
                    
                    match arg:
                        case "-a" | "--alias":
                            value_index = _index + 1
                            if len(iargs) - 1 < value_index:
                                error("Expected alias")
                                
                            install_args.alias_option = iargs[value_index]
                            double_continue = True
                            continue
                        
                        case "-c" | "--clone":
                            install_args.clone_flag = True
                            
                        case _:
                            install_args.packages.append(arg)
                res.install = install_args
                break
            
            case "repository":
                for arg in args[index + 1:]:
                    print(arg)
                break
    return res