from screen_grabber import grab_screen
import cv2
import pyautogui
import numpy as np

def setup_get_hp():
    actual_zone = pyautogui.locateOnScreen('blustack.png')
    if actual_zone == None:
        raise Exception('Bluestacks Not found')

    region_of_ally = [actual_zone[0] + 222, actual_zone[1] + 98,
                      actual_zone[0] + 381, actual_zone[1] + 98]
    region_of_enemy = [actual_zone[0] + 446, actual_zone[1] + 98,
                       actual_zone[0] + 605, actual_zone[1] + 98]

    return region_of_ally, region_of_enemy


def detect_hp(region_of_ally, region_of_enemy):



    screen = grab_screen(region=(region_of_ally))
    screen2 = grab_screen(region=(region_of_enemy))

    count1 = dict(zip(*np.unique(screen, return_counts=True)))[142] if 142 in screen else 0
    count2 = dict(zip(*np.unique(screen2, return_counts=True)))[142] if 142 in screen2 else 0
#      print("Ally Percentage: " + str(count1 / screen.shape[1] * 100) + "%")
#     print("Enemy Percentage: " + str(count2 / screen2.shape[1] * 100) + "%")
    #reward = 1 / ((count2 / screen2.shape[1] * 100))
   # return reward
    remaining_ally_life = count1 / screen.shape[1]# * 100
    remaining_enemy_life = count2 / screen2.shape[1]# * 100
    if remaining_enemy_life == 0 or remaining_ally_life == 0:
        done = False
    else:
        done = True
    preprocessed_result = [remaining_ally_life if remaining_ally_life > 0 else 0,
                           remaining_enemy_life if remaining_enemy_life > 0 else 0,
                           done]

    result = [remaining_ally_life, remaining_enemy_life, done]
    return result

if __name__ == '__main__':
    region_of_ally, region_of_enemy = setup_get_hp()

    while True:
        print(detect_hp(region_of_ally, region_of_enemy))
