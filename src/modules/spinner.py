from threading import Thread, Event
from modules.style import info

from colorama import Fore, Style

import time

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
        self._text = txt
    
    def stop(self):
        self.should_stop.set()
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, *_):
        self.stop()
        print(CURSOR_SHOW, end="")
    
    def _render(self, frame):
        print(f"{self.prefix} {Fore.CYAN}{frame}{Fore.RESET} {self._text}".strip(), flush=False, end="\r")
    
    def clear(self):
        
        print(self.CLEAR_LINE, end="")
        
    def run(self):
        print(CURSOR_HIDE,end="")
        while self.should_stop.is_set() is False:
            for frame in SPINNER_FRAMES:
                # print(self.should_stop.is_set())
                if self.should_stop.is_set() is True:
                    break
                self._render(frame)
                self.clear()
                
                time.sleep(0.080)