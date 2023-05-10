import pyautogui
import random
from PIL import Image
import time


def screenshot(place):
    if place == 'all':
        im = pyautogui.screenshot()
        name = 'screenshot' + str(random.randint(1, 10000000)) + '.png'
        im.save(name)
        return name
    elif place == 'qr_tg':

        center_x = 2560 // 2
        center_y = 1600 // 2

        screenshot = pyautogui.screenshot(region=(center_x-60, center_y-360, 440, 440))

        name = 'screenshot' + str(random.randint(1, 10000000)) + '.png'
        screenshot.save(name)
        return name


def start_app(app_name):
    try:
        pyautogui.keyDown('command')
        pyautogui.keyDown('space')
        pyautogui.keyUp('space')
        pyautogui.keyUp('command')
        time.sleep(1)
        pyautogui.typewrite(app_name)
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(1)

        return 'success'
    except Exception as e:
        return 'failed'


if __name__ == '__main__':
   print(screenshot('all'))