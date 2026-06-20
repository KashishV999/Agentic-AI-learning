import sys

is_debug = False

def set_debug(value: bool):
    global is_debug
    is_debug = value

def debug_log(message: str):
    if is_debug:
        print(message, file=sys.stderr)