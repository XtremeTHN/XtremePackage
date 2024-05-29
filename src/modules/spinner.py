from threading import Thread, Event
from modules.style import info

from colorama import Fore

CURSOR_HIDE = "\033[?25l"
CURSOR_SHOW = "\033[?25h"

SPINNER_FRAMES = [
    "⠁",
    "⠁",
    "⠉",
    "⠙",
    "⠚",
    "⠒",
    "⠂",
    "⠂",
    "⠒",
    "⠲",
    "⠴",
    "⠤",
    "⠄",
    "⠄",
    "⠤",
    "⠠",
    "⠠",
    "⠤",
    "⠦",
    "⠖",
    "⠒",
    "⠐",
    "⠐",
    "⠒",
    "⠓",
    "⠋",
    "⠉",
    "⠈",
    "⠈"
]

class Spinner(Thread):
    CLEAR_LINE = "\033[K"
    
    def __init__(self, text, prefix=""):
        super().__init__()
        self.prefix = prefix
        self._text = text
        self.should_stop = Event()
        
    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, txt):
        self._finish()
        self._text = txt
    
    def stop(self):
        self.should_stop.set()
        print(CURSOR_SHOW, end="")
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, *_):
        self.stop()
    
    def _render(self, frame):
        print(f"{self.prefix} {Fore.CYAN}{frame}{Fore.RESET} {self._text}".strip(), flush=False, end="\r")
    
    def _finish(self):
        print(f"{self.prefix} ✓ {self._text}".strip())
    
    def clear(self):
        print(self.CLEAR_LINE, end="")
        
    def run(self):
        print(CURSOR_HIDE,end="")
        while self.should_stop.is_set() is False:
            for frame in SPINNER_FRAMES:
                if self.should_stop.wait(0.080) is True:
                    self._finish()
                    break
                self._render(frame)
                self.clear()
                