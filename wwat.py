from pynput.keyboard import Listener
import threading
import time
import random
import keyboard
import json

p = None
spam_e = False

def e_spamer():
    while True:
        time.sleep(0.7+random.random()*0.2)
        if spam_e:
            keyboard.press('e')
            time.sleep(0.02+random.random()*0.05)
            keyboard.release('e')

def on_press(key):
    global spam_e
    if hasattr(key, 'char') and key.char == 'y':
        spam_e = (spam_e != True)

p = threading.Thread(target=e_spamer)
p.start()
# Collect events until released
with Listener(on_press=on_press) as listener:
    listener.join()
