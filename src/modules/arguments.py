import sys
from modules.style import underlined, bold, info, error
    
class InstallArguments:
    clone_flag: bool
    alias_option: str | None
    
    packages: list[str]

    def __init__(self) -> None:
        self.clone_flag = False
        self.alias_option = None
        self.packages = []

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
                
                double_continue = False
                iargs: list[str] = args[index + 1:]
                for _index, arg in enumerate(iargs):
                    if double_continue is True:
                        double_continue = False
                        continue
                    
                    match arg:
                        case "-a" | "--alias":
                            value_index = _index + 1

                            # value checking
                            if len(iargs) - 1 < value_index:
                                error("Expected alias")
                            
                            if iargs[value_index].startswith("-"):
                                error("Expected alias, not a flag")

                            install_args.alias_option = iargs[value_index]
                            double_continue = True
                            continue
                        
                        case "-c" | "--clone":
                            install_args.clone_flag = True
                            
                        case _:
                            install_args.packages.append(arg)
                if len(install_args.packages) == 0:
                    error("Expected at least one package")
                res.install = install_args
                break
            case _:
                error("Unknown command/option")     
    return res