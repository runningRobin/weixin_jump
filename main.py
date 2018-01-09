import os
from PIL import Image
import numpy
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

is_up = False

def get_screen_image():
    os.system('adb shell screencap -p /sdcard/screen.png')
    os.system('adb pull /sdcard/screen.png')
    return numpy.array(Image.open('screen.png'))

def click(event, coor=[]):
    global is_up
    coor.append((event.xdata, event.ydata))
    if len(coor) == 2:
        jump(coor.pop(), coor.pop())
        is_up = True

def jump(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    distance = ((x2-x1)**2 + (y2-y1)**2)**0.5
    os.system('adb shell input swipe 320 410 320 410 {}'.format(int(distance*1.35)))

def up_screen(frame):
    global is_up
    if is_up:
        time.sleep(1)
        axes_image.set_array(get_screen_image())
        is_up = False
    return axes_image

figure = plt.figure()
axes_image = plt.imshow(get_screen_image(), animated=True)
figure.canvas.mpl_connect('button_press_event', click)
ani = FuncAnimation(figure, up_screen, interval=50, blit=True)
plt.show()
