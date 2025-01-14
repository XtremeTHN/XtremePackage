import sys
import traceback

DEBUG=False

class Colors:
    RED = "\x1B[31m"
    RED_C = "31"
    BLUE = "\x1B[34"
    BLUE_C = "34"
    GREEN = "\x1B[32m"
    GREEN_C = "32"
    LIGHTRED_EX = "\x1B[91m"
    WHITE = "\x1B[37m"
    WHITE_C = "37"
    LIGHTRED_EX_C = "91"

class Style:
    BOLD = "\x1B[1m"
    UNDERLINED= "\x1B[4m"
    RESET = "\x1B[0m"
    ALL = "\x1B[1;4;{}m"
    
def bold(msg) -> str:
    return f"{Style.BOLD}{msg}{Style.RESET}"

def underlined(msg) -> str:
    return Style.UNDERLINED + msg + Style.RESET

def color(string, color) -> str:
    return color + string + Style.RESET

def colored_string(string, color: str) -> str:
    """
    Colors a string

    Args:
        string (str): The string to be colored.
        color (str): The color name to apply to the string. 
                     If the color is not found, defaults to red.

    Returns:
        str: The colored string wrapped with reset style.
    """

    return f"{getattr(Colors, color.upper(), Colors.RED)}{string}{Style.RESET}"
def pretty_string(string, color: str) -> str:
    """Underlines, bolds and colors a string

    Args:
        string (str): The string
        color (str): The color

    Returns:
        str: The formatted string
    """
    return f"{Style.ALL.format(getattr(Colors, (color + "_c").upper(), Colors.RED))}{string}{Style.RESET}"

def info(*args, **kwargs):
    func = traceback.extract_stack()[-2]
    print(pretty_string(f"{func.name} > INFO:" if DEBUG is True else "INFO:", "green"), *args, **kwargs)

def debug(*args):
    func = traceback.extract_stack()[-2]
    if "--debug" in sys.argv:
        print(pretty_string(f"{func.filename.split('/')[-1]}:{func.lineno} > {func.name} > DEBUG:", "blue"), *args)

def warn(*args, **kwargs):
    func = traceback.extract_stack()[-2]
    print(pretty_string(f"{func.filename.split('/')[-1]}:{func.lineno} > {func.name} > WARNING:" if DEBUG is True else "WARNING:", "lightred_ex"), *args, **kwargs)

def error(*args, exit_code=1, **kwargs):
    func = traceback.extract_stack()[-2]
    print(pretty_string(f"{func.filename.split('/')[-1]}:{func.lineno} > {func.name} > ERROR:" if DEBUG is True else "ERROR:", "red"), *args, **kwargs)
    
    sys.exit(exit_code)