import pyautogui
import time
from file1 import setup_get_hp
import os


def click_on_thing(bluestacks_position , button, test=False, first=False):
    result = [bluestacks_position[0]+button[0], bluestacks_position[1]+button[1]]
    if test:
        pyautogui.moveTo(result)
        time.sleep(0.05)
    elif not test:
        pyautogui.click(result)
        time.sleep(0.05)
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

def exit(bluestacks_position):
    print("Exiting")
    click_on_thing(bluestacks_position, Coordonates.pause_button)
    click_on_thing(bluestacks_position, Coordonates.manual_exit)
    click_on_thing(bluestacks_position, Coordonates.comfirm_manual_exit)
    click_on_thing(bluestacks_position, Coordonates.regular_exit)

def start_fight(bluestacks_position, chapter, enemy):
    print("Starting Fight")
    click_on_thing(bluestacks_position, chapter)
    click_on_thing(bluestacks_position, chapter)
    click_on_thing(bluestacks_position, chapter)
    click_on_thing(bluestacks_position, chapter)
    click_on_thing(bluestacks_position, chapter)
    click_on_thing(bluestacks_position, chapter)
    click_on_thing(bluestacks_position, chapter)
    click_on_thing(bluestacks_position, enemy)
    click_on_thing(bluestacks_position, Coordonates.start_button)


def start_AI():
    print("starting AI")
    os.system('file2.py')
    quit()

def toggle_bluestacks_on_top(bluetacks_position):
    click_on_thing(bluestacks_position, Coordonates.settings)
    click_on_thing(bluestacks_position, Coordonates.settings2)
    click_on_thing(bluestacks_position, Coordonates.settings_preferences)
    click_on_thing(bluestacks_position, Coordonates.settings_preferences)
    click_on_thing(bluestacks_position, Coordonates.settings_preferences)
    click_on_thing(bluestacks_position, Coordonates.settings_preferences)
    click_on_thing(bluestacks_position, Coordonates.settings_preferences)
    click_on_thing(bluestacks_position, Coordonates.settings_on_top)
    click_on_thing(bluestacks_position, Coordonates.settings_exit)




if __name__ == '__main__':
    _, _, bluestacks_position = setup_get_hp()

  #  toggle_bluestacks_on_top(bluestacks_position)
    exit(bluestacks_position)
    start_fight(bluestacks_position, Coordonates.chapter1, Coordonates.bodyguard)
  #  toggle_bluestacks_on_top(bluestacks_position)
    start_AI()
   # click_on_thing(bluestacks_position, Coordonates.regular_exit, test=True)









