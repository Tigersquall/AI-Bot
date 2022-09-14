import time

import PIL.Image
import pyautogui as p
import torch

screenWidth, screenHeight = p.size()

enemy_searchPosition = 1018, 42
enemy_searchColor = 86, 73, 67

barEmpty_searchColor = 0, 0, 51

barHP_searchPosition = 127, 125
barDS_searchPosition = 130, 141

model = torch.hub.load("D:\\Neural\\yolov5-master", 'custom', path=".\\best.pt", source='local')


def heal_loop():
    if p.pixel(barHP_searchPosition[0], barHP_searchPosition[1]) == barEmpty_searchColor:
        p.press('f7')
    if p.pixel(barDS_searchPosition[0], barDS_searchPosition[1]) == barEmpty_searchColor:
        p.press('f8')


def search_loop():
    counter = 0
    while p.locateOnScreen(PIL.Image.open('.\\reference')):
        heal_loop()
        p.press('4')
        if counter < 3:
            if p.pixel(enemy_searchPosition[0], enemy_searchPosition[1]) == enemy_searchColor:
                while p.pixel(enemy_searchPosition[0], enemy_searchPosition[1]) == enemy_searchColor:
                    heal_loop()
                    p.press('f1')
                    p.press('f2')
                    p.press('1')
                    p.press('4')
                    counter = 0
            else:
                p.press('tab')
                counter += 1
        else:
            img = p.screenshot()
            res = model(img)
            dataset = res.pandas().xyxy[0]
            if dataset.size > 0:
                xmin = res.pandas().xyxy[0].iat[0, 0]
                ymin = res.pandas().xyxy[0].iat[0, 1]
                xmax = res.pandas().xyxy[0].iat[0, 2]
                ymax = res.pandas().xyxy[0].iat[0, 3]
                pos = (xmin + xmax)/2, (ymin + ymax)/2
                p.moveTo(pos)
                p.mouseDown()
                p.mouseUp()
            else:
                p.moveTo(screenWidth/2, screenHeight/2)
                p.drag(15, 0, 1.5, button='right')
            counter = 0


if __name__ == '__main__':
    time.sleep(2)
    search_loop()
