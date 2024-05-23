import threading

def non_blocking(func):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()

        return thread
    
    return wrapper

def is_nuitka_installed():
    try:
        import nuitka
        return True
    except ModuleNotFoundError:
        return False