from screen_grabber import grab_screen
import cv2
import pyautogui
import numpy as np
import time
import os
from keras.models import load_model

timer_model = load_model('time_reader.hdf5')

def setup_get_hp():
    actual_zone = pyautogui.locateOnScreen('blustack.png')
    if actual_zone == None:
        raise Exception('Bluestacks Not found')

    actual_zone = [actual_zone[0], actual_zone[1]]

    region_of_ally = [actual_zone[0] + 222, actual_zone[1] + 98,
                      actual_zone[0] + 381, actual_zone[1] + 98]
    region_of_enemy = [actual_zone[0] + 446, actual_zone[1] + 98,
                       actual_zone[0] + 605, actual_zone[1] + 98]

    return region_of_ally, region_of_enemy, actual_zone


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
        done = True
    else:
        done = False
    preprocessed_result = [remaining_ally_life if remaining_ally_life > 0 else 0,
                           remaining_enemy_life if remaining_enemy_life > 0 else 0,
                           done]

    result = [remaining_ally_life, remaining_enemy_life, done]
    return result


def get_visual_input(bluestacks_position, delay=0.0, for_nn=False, show=False):
    time.sleep(delay)
    region = [bluestacks_position[0] + 10, bluestacks_position[1] + 42,
              bluestacks_position[0] + 820, bluestacks_position[1] + 500]

    if for_nn is False:

        result = grab_screen(region)

        if show:

            cv2.imshow('test', result)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()

        return result
    else:
        result = []
        result1 = grab_screen(region)
        if show:
            cv2.imshow('frame1', result1)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()

        result.append(result1)
        result2 = grab_screen(region)
        if show:
            cv2.imshow('frame2', result2)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
        result.append(result2)
        result3 = grab_screen(region)
        if show:
            cv2.imshow('frame3', result3)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
        result.append(result3)
        result4 = grab_screen(region)
        if show:
            cv2.imshow('frame4', result4)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
        result.append(result4)

        result = np.array(result)

 #       print(result.shape)
#        time.sleep(999)

        return result

def detect_start(visual_input, level):

    template = cv2.imread('{}.png'.format(level), 0)

    w, h = template.shape[::-1]

    result = cv2.matchTemplate(visual_input, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.85

    loc = np.where(result >= threshold)

    for pt in zip(*loc[::-1]):
        cv2.rectangle(visual_input, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)
        return True

    return False


def detect_paused(visual_input):

    template = cv2.imread('pause.png', 0)

    w, h = template.shape[::-1]

    result = cv2.matchTemplate(visual_input, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.85

    loc = np.where(result >= threshold)

    for pt in zip(*loc[::-1]):
        cv2.rectangle(visual_input, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)
        return False

    return True


def actually_act(chosen_action, bluestacks_position, verbose=1, lock=False):
        if chosen_action == 0:
            chosen_action = 'block'
        elif chosen_action == 1:
            chosen_action = 'jump_left'
        elif chosen_action == 2:
            chosen_action = 'punch_once'
        elif chosen_action == 3:
            chosen_action = 'move_right'
        elif chosen_action == 4:
            chosen_action = 'move_left'
        elif chosen_action == 5:
            chosen_action = 'punch_twice'
        elif chosen_action == 6:
            chosen_action = 'right_dash_punch_once'
        elif chosen_action == 7:
            chosen_action = 'left_dash_punch'
        elif chosen_action == 8:
            chosen_action = 'upper_punch'
        elif chosen_action == 9:
            chosen_action = 'lower_punch'
        elif chosen_action == 10:
            chosen_action = 'kick'
        elif chosen_action == 11:
            chosen_action = 'front_kick'
        elif chosen_action == 12:
            chosen_action = 'back_kick'
        elif chosen_action == 13:
            chosen_action = 'jump_kick'
        elif chosen_action == 14:
            chosen_action = 'jump_right'
        elif chosen_action == 15:
            chosen_action = 'sweep'
        elif chosen_action == 16:
            chosen_action = 'double_sweep'
        elif chosen_action == 17:
            chosen_action = 'spinning_step'
        elif chosen_action == 18:
            chosen_action = 'horse_kick'
        elif chosen_action == 19:
            chosen_action = 'dash_right'
        elif chosen_action == 20:
            chosen_action = 'dash_left'
        elif chosen_action == 21:
            chosen_action = 'roll_left'
        elif chosen_action == 22:
            chosen_action = 'roll_right'



        if verbose == 1:
            print(chosen_action)
        action_converter(chosen_action, bluestacks_position, lock=True)

def get_timer_area(bluestacks_position, direction='left', show=False, save=False, save_dir=None):
    count = 0

    region = [bluestacks_position[0] + 390, bluestacks_position[1] + 60,
              bluestacks_position[0] + 415, bluestacks_position[1] + 100]

    if direction is 'right':
        region = region[0]+25, region[1], region[2]+25, region[3]

    if show or save:
        result = grab_screen(region)

    if show:
        cv2.imshow('test', result)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()

    if save:
        for _ in os.listdir(save_dir):
            count = count + 1
        cv2.imwrite('{}/{}.png'.format(save_dir, count), result)

    return region

def detect_time(bluestacks_position, model, not_paused, detect_start=False):
    if not_paused:
        right = get_timer_area(bluestacks_position, direction='right')
        left = get_timer_area(bluestacks_position)
        left = grab_screen(left)
        right = grab_screen(right)
      #  right = np.reshape(right, (1, 1, right[0], right[1]))
        #right = np.expand_dims(right, axis=3)
       # right = get_visual_input(bluestacks_position)
        try:
            right = np.reshape(right, (1, right.shape[0], right.shape[1], 1))
            left = np.reshape(left, (1, left.shape[0], left.shape[1], 1))

            prediction_right = model.predict(right)
            prediction_right = np.argmax(prediction_right)

            prediction_left = model.predict(left)
            prediction_left = np.argmax(prediction_left)

            final_prediction = prediction_left*10 + prediction_right

            if detect_start == True:
                if final_prediction == 98:
                    return True
                else:
                    return False

            return final_prediction
        except ValueError as e:
            print(e)
            print(right.shape)
            print(left.shape)
            quit()
       # model.predict()
    else:
        print('paused')
        time.sleep(0.1)

def action_converter(action, bluestacks_position, lock=False):
    come_back = pyautogui.position()
    pyautogui.click(bluestacks_position[0] + 200, bluestacks_position[1] + 200)
    if action == 'block':  # 0
        pass
    elif action == 'punch_once':  # 2
        pyautogui.press('i')
    elif action == 'move_right':  # 3
        pyautogui.keyDown('d')
        pyautogui.keyUp('d')
    elif action == 'move_left':  # 4
        pyautogui.keyDown('a')
        pyautogui.keyUp('a')
    elif action == 'punch_twice':  # 5
        pyautogui.press('i')
        pyautogui.press('i')
    elif action == 'right_dash_punch_once':  # 5
        pyautogui.keyDown('d')
        pyautogui.press('i')
        pyautogui.keyUp('d')
    elif action == 'right_dash_punch_twice':  # 6
        pyautogui.keyDown('d')
        pyautogui.press('i')
        pyautogui.press('i')
        pyautogui.keyUp('d')
    elif action == 'left_dash_punch':  # 7
        pyautogui.keyDown('a')
        pyautogui.press('i')
        pyautogui.keyUp('a')
    elif action == 'upper_punch':  # 8
        pyautogui.keyDown('w')
        pyautogui.press('i')
        pyautogui.keyUp('w')
    elif action == 'lower_punch':  # 9
        pyautogui.keyDown('s')
        pyautogui.press('i')
        pyautogui.keyUp('s')
    elif action == 'kick':  # 10
        pyautogui.press('j')
    elif action == 'front_kick':  # 11
        pyautogui.keyDown('d')
        pyautogui.press('j')
        pyautogui.keyUp('d')
    elif action == 'back_kick':  # 12
        pyautogui.keyDown('a')
        pyautogui.press('j')
        pyautogui.keyUp('a')
    elif action == 'jump_kick':  # 13
        pyautogui.keyDown('w')
        pyautogui.press('j')
        pyautogui.keyUp('w')
    elif action == 'sweep':  # 15
        pyautogui.keyDown('s')
        pyautogui.press('j')
        pyautogui.keyUp('s')
    elif action == 'double_sweep':  # 16
        pyautogui.keyDown('s')
        pyautogui.press('j')
        pyautogui.press('j')
        pyautogui.keyUp('s')
    elif action == 'spinning_step':  # 17
        pyautogui.keyDown('d')
        pyautogui.keyDown('s')
        pyautogui.press('j')
        pyautogui.keyUp('d')
        pyautogui.keyUp('s')
    elif action == 'horse_kick':  # 18
        pyautogui.keyDown('a')
        pyautogui.keyDown('s')
        pyautogui.press('j')
        pyautogui.keyUp('a')
        pyautogui.keyUp('s')
    elif action == 'dash_right':  # 19
        pyautogui.keyDown('d')
        pyautogui.keyUp('d')
        pyautogui.keyDown('d')
        pyautogui.keyUp('d')
    elif action == 'dash_left':  # 20
        pyautogui.keyDown('a')
        pyautogui.keyUp('a')
        pyautogui.keyDown('a')
        pyautogui.keyUp('a')
    elif action == 'roll_left':  # 21
        pyautogui.keyDown('a')
        pyautogui.keyDown('s')
        pyautogui.keyUp('a')
        pyautogui.keyUp('s')
    elif action == 'roll_right':  # 22
        pyautogui.keyDown('d')
        pyautogui.keyDown('s')
        pyautogui.keyUp('d')
        pyautogui.keyUp('s')
    elif action == 'jump_left':  # 1
        pyautogui.keyDown('a')
        pyautogui.keyDown('w')
        pyautogui.keyUp('a')
        pyautogui.keyUp('w')
    elif action == 'jump_right':  # 14
        pyautogui.keyDown('d')
        pyautogui.keyDown('w')
        pyautogui.keyUp('d')
        pyautogui.keyUp('w')
    if not lock:
        pyautogui.moveTo(come_back)

    time.sleep(0.3)  # 0.3

if __name__ == '__main__':
    region_of_ally, region_of_enemy, bluestacks_position = setup_get_hp()
    current_time = time.time()

    while True:
        visual_input = get_visual_input(bluestacks_position, for_nn=True, show=True, delay=0.3)
        print("time elapsed", float(-current_time+time.time()))
        current_time = time.time()
     #   time.sleep(999)
       # visual_input = np.array(visual_input / 255)
        #print(visual_input.shape)
        #print(float(time.time() - current_time))

        #print(detect_hp(region_of_ally, region_of_enemy))
        #visual_input = get_visual_input(bluestacks_position)

        #result = detect_paused(visual_input)




'''
list of moves:
0  = block
1  = jump_left
2  = punch_once
3  = move_right
4  = move_left
5  = right_dash_punch_once
6  = right_dash_punch_twice
7  = left_dash_punch
8  = upper_punch
9  = lower_punch
10 = kick
11 = front_kick
12 = back_kick
13 = jump_kick
14 = jump_right
15 = sweep
16 = double_sweep
17 = spinning_step
18 = horse_kick
19 = dash_right
20 = dash_left
21 = roll_left
22 = roll_right
23 = jump_left


#note there are more block moves because I remvove useless moves
'''


