from pynput.keyboard import Listener, Key
import threading
import time
import random
import keyboard
import json

def on_press(key):
    if hasattr(key, 'char') and key.char == "c":
        st = time.time()
        time.sleep(4.17)
        keyboard.press("s")
        time.sleep(0.01)
        keyboard.release("s")
        print(time.time() - st)

with Listener(on_press=on_press) as listener:
    listener.join()