import pyautogui
import time
from file1 import setup_get_hp
import os


def click_on_thing(bluestacks_position , button, test=False, first=False):
    result = [bluestacks_position[0]+button[0], bluestacks_position[1]+button[1]]
    if test:
        pyautogui.moveTo(result)
        time.sleep(0.15)
    elif not test:
        pyautogui.click(result)
        time.sleep(0.15)
    if first:
        quit()

class Coordonates():
    pause_button = [425, 125]
    manual_exit = [225, 325]
    comfirm_manual_exit = [500, 375]
    regular_exit = [500, 475]
    start_button = [675, 425]
    bodyguard = [300, 275]
    chapter1 = [240, 480]
    settings = [675, 15]
    settings2 = [675, 50]
    settings_preferences = [150, 275]
    settings_on_top = [275, 400]
    settings_exit = [760, 30]
    energy = [325, 60]
    energy_refill = [550, 400]
    handle1 = [400, 380]
    menu = [100, 100]
    arena = [100, 200]

def exit(bluestacks_position, debug=False):
    print("Exiting")
    click_on_thing(bluestacks_position, Coordonates.pause_button)
    if debug:
        print("pause")
    click_on_thing(bluestacks_position, Coordonates.manual_exit)
    if debug:
        print("manual exit")
    click_on_thing(bluestacks_position, Coordonates.comfirm_manual_exit)
    if debug:
        print("comfirm")
    click_on_thing(bluestacks_position, Coordonates.regular_exit)
    if debug:
        print("regular")

    time.sleep(3)


def start_fight(bluestacks_position, chapter, enemy):
    print("Starting Fight")
    click_on_thing(bluestacks_position, Coordonates.menu)
    click_on_thing(bluestacks_position, Coordonates.arena)
    time.sleep(2)
    handler(bluestacks_position)
    click_on_thing(bluestacks_position, chapter)
    handler(bluestacks_position)
    click_on_thing(bluestacks_position, chapter)
    handler(bluestacks_position)
    click_on_thing(bluestacks_position, chapter)
    handler(bluestacks_position)
    click_on_thing(bluestacks_position, chapter)
    handler(bluestacks_position)
    click_on_thing(bluestacks_position, chapter)
    handler(bluestacks_position)
    click_on_thing(bluestacks_position, chapter)
    handler(bluestacks_position)
    click_on_thing(bluestacks_position, chapter)
    handler(bluestacks_position)
    click_on_thing(bluestacks_position, enemy)
    click_on_thing(bluestacks_position, Coordonates.start_button)


def start_AI():
    print("starting AI")
    os.system('file2.py')
    quit()

def handler(bluestacks_position):
    handler = pyautogui.locateOnScreen('handle1.png')
    if handler is not None:
        click_on_thing(bluestacks_position, Coordonates.handle1)

def toggle_bluestacks_on_top(bluestacks_position):
    click_on_thing(bluestacks_position, Coordonates.settings)
    click_on_thing(bluestacks_position, Coordonates.settings2)
    click_on_thing(bluestacks_position, Coordonates.settings_preferences)
    click_on_thing(bluestacks_position, Coordonates.settings_preferences)
    click_on_thing(bluestacks_position, Coordonates.settings_preferences)
    click_on_thing(bluestacks_position, Coordonates.settings_preferences)
    click_on_thing(bluestacks_position, Coordonates.settings_preferences)
    click_on_thing(bluestacks_position, Coordonates.settings_on_top)
    click_on_thing(bluestacks_position, Coordonates.settings_exit)


def reset_start(bluestacks_position, chapter=Coordonates.chapter1, fight=Coordonates.bodyguard):
    exit(bluestacks_position)
    handler(bluestacks_position)
    reset_energy(bluestacks_position)
    handler(bluestacks_position)
    start_fight(bluestacks_position, chapter, fight)


def reset_energy(bluestacks_position):
    click_on_thing(bluestacks_position, Coordonates.energy)
    click_on_thing(bluestacks_position, Coordonates.energy_refill)
    click_on_thing(bluestacks_position, Coordonates.energy_refill)



if __name__ == '__main__':
    _, _, bluestacks_position = setup_get_hp()

   # reset_start(bluestacks_position)
    start_fight(bluestacks_position, Coordonates.chapter1, Coordonates.bodyguard)






