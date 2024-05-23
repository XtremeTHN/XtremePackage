import sys
import traceback

from colorama import Fore, Style
# from pystyle import Colorate, Colors

DEBUG=False

def bold(msg) -> str:
    return f"{Style.BRIGHT}{msg}{Style.RESET_ALL}"

def underlined(msg) -> str:
    return '\033[4m' + msg + Style.RESET_ALL

def color(string, color) -> str:
    return color + string + Style.RESET_ALL

def info(*args):
    func = traceback.extract_stack()[-2]
    print(
        underlined(
            bold(
                color(f"{func.name} > INFO:" if DEBUG is True else "INFO:", Fore.GREEN)
                )
            ), *args
        )

def debug(*args):
    func = traceback.extract_stack()[-2]
    
    if "--debug" in sys.argv:
        print(
            underlined(
                bold(
                    color(
                        f"{func.filename.split('/')[-1]}:{func.lineno} > {func.name} > DEBUG:", Fore.BLUE
                        )
                    )
                ), *args
            )

def warn(*args):
    func = traceback.extract_stack()[-2]
    print(
        underlined(
            bold(
                color(
                    f"{func.filename.split('/')[-1]}:{func.lineno} > {func.name} > WARNING:" if DEBUG is True else "WARNING:", Fore.LIGHTRED_EX
                    )
                )
            ), *args
        )

def error(*args, exit_code=1):
    func = traceback.extract_stack()[-2]
    print(
        underlined(
            bold(
                color(
                    f"{func.filename.split('/')[-1]}:{func.lineno} > {func.name} > ERROR:" if DEBUG is True else "ERROR:", Fore.RED
                    )
                )
            ), *args
        )
    
    sys.exit(exit_code)