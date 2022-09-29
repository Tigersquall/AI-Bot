import time

import PIL.Image
import pyautogui as p
import pyscreeze
import torch

screenWidth, screenHeight = p.size()

enemy_searchPosition = 1018, 42
enemy_searchColor = 152, 142, 112
enemyHP_searchPosition = 829, 60
enemyHP_searchColor = 129, 34, 24

barEmpty_searchColor = 0, 0, 51
barEmpty_searchColor_combat = 69, 5, 54

barHP_searchPosition = 127, 125
barDS_searchPosition = 130, 141

reference_image = PIL.Image.open('.\\reference')
bar_image = PIL.Image.open('.\\bar.png')
#model = torch.hub.load(".\\yolov5-master", 'custom', path=".\\best.pt", source='local')


def heal_loop():
    if p.pixel(barHP_searchPosition[0], barHP_searchPosition[1]) == barEmpty_searchColor:
        p.press('f7')
    if p.pixel(barDS_searchPosition[0], barDS_searchPosition[1]) == barEmpty_searchColor:
        p.press('f8')
    if p.pixel(barHP_searchPosition[0], barHP_searchPosition[1]) == barEmpty_searchColor_combat:
        p.press('f7')
    if p.pixel(barDS_searchPosition[0], barDS_searchPosition[1]) == barEmpty_searchColor_combat:
        p.press('f8')


def search_loop():
    counter = 0
    while p.locateOnScreen(reference_image):
        heal_loop()
        p.press('4')
        if p.pixel(enemyHP_searchPosition[0], enemyHP_searchPosition[1]) == enemyHP_searchColor \
                and p.pixel(enemy_searchPosition[0], enemy_searchPosition[1]) == enemy_searchColor:
            p.press('1')
            p.press('4')
            heal_loop()
            counter = 0
        else:
            p.press('tab')
            counter += 1
        if counter > 1:
            target = p.locateOnScreen(bar_image)
            if target is not None:
                target = p.center(target)
                targetx, targety = target
                targety += 100
                p.moveTo(targetx, targety)
                if targetx < 1550 and targety < 980:
                    p.mouseDown()
                    p.mouseUp()
            else:
                p.moveTo(screenWidth/2, screenHeight/2)
                p.drag(400, 0, 0.15, button='right')


if __name__ == '__main__':
    time.sleep(2.5)
    search_loop()
