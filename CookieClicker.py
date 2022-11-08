import pyautogui
import keyboard

pyautogui.FAILSAFE = True

i = 0

while(True):
    if keyboard.is_pressed('esc'):
        break
    if keyboard.is_pressed('e'):
        pyautogui.moveTo(140, 480)
        while(True):
            pyautogui.click(clicks=100, interval=0.00000005)
            i += 1
            print(i,i*100)
            if keyboard.is_pressed('w'):
                print('stoped')
                break
    if keyboard.is_pressed('q'):
        pyautogui.click(clicks=50, interval=0.00000005)