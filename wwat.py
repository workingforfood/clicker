from pynput.keyboard import Listener, Key
import threading
import time
import random
import keyboard
import json

p = None
spam_e = False
trun_on = False

def clicker(mean_delay_between_clicks, mean_pressed_time, num_of_clicks, id):
    while True:
        time.sleep(mean_delay_between_clicks + random.random() * 0.2)
        if config["setups"][id]["activated"] and \
                ((config["setups"][id]["current_clicks"] < num_of_clicks) or (num_of_clicks == -1)):
            keyboard.press(config["setups"][id]["send_key"])
            time.sleep(mean_pressed_time + random.random() * 0.05)
            keyboard.release(config["setups"][id]["send_key"])
            if num_of_clicks != -1:
                config["setups"][id]["current_clicks"] += 1
        if (config["setups"][id]["current_clicks"] >= num_of_clicks) and (num_of_clicks != -1):
            config["setups"][id]["current_clicks"] = 0
            config["setups"][id]["activated"] = False


def deterministic_clicker(mean_delay_between_clicks, mean_pressed_time, num_of_clicks, id):
    while True:
        time.sleep(0.002)
        if config["setups"][id]["activated"] and \
                ((config["setups"][id]["current_clicks"] < num_of_clicks) or (num_of_clicks == -1)):
            st = time.time()
            print(st)
            time.sleep(mean_delay_between_clicks)
            keyboard.press(config["setups"][id]["send_key"])
            time.sleep(mean_pressed_time)
            keyboard.release(config["setups"][id]["send_key"])
            print(time.time() - st)
            if num_of_clicks != -1:
                config["setups"][id]["current_clicks"] += 1
        if (config["setups"][id]["current_clicks"] >= num_of_clicks) and (num_of_clicks != -1):
            config["setups"][id]["current_clicks"] = 0
            config["setups"][id]["activated"] = False

def e_spamer():
    while True:
        time.sleep(0.7+random.random()*0.2)
        if spam_e:
            keyboard.press('e')
            time.sleep(0.02+random.random()*0.05)
            keyboard.release('e')


def on_press(key):
    global trun_on
    if key == Key.f2:
        trun_on = (trun_on != True)
        if not trun_on:
            for i, command in enumerate(config["setups"]):
                config["setups"][i]["activated"] = False
                config["setups"][i]["current_clicks"] = 0
    if trun_on:
        for i, command in enumerate(config["setups"]):
            if hasattr(key, 'char') and key.char == command['activate_key']:
                config["setups"][i]["activated"] = (config["setups"][i]["activated"] != True)
                if not config["setups"][i]["activated"]:
                    config["setups"][i]["current_clicks"] = 0


with open("clicker.cfg") as file:
    config = json.load(file)

for i, command in enumerate(config["setups"]):
    command["activated"] = False
    command["current_clicks"] = 0
    command["thread"] = threading.Thread(target=deterministic_clicker,
                                         args=(command["mean_delay_between_clicks"],
                                               command["mean_pressed_time"],
                                               command["num_of_clicks"],
                                               i
                                               ))
    command["thread"].start()

print(config)

# p = threading.Thread(target=e_spamer)
# p.start()
# # Collect events until released
with Listener(on_press=on_press) as listener:
    listener.join()