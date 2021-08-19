import pigpio, time
pi = pigpio.pi()
gpio_0 = 22
gpio_1 = 27
pi.set_mode(gpio_0, pigpio.INPUT)
pi.set_mode(gpio_1, pigpio.INPUT)

pi.set_pull_up_down(gpio_0, pigpio.PUD_UP)
pi.set_pull_up_down(gpio_1, pigpio.PUD_UP)

def cbf(gpio, level, tick):
   print(gpio, level, tick)

pi.callback(gpio_0, pigpio.EITHER_EDGE, cbf)
pi.callback(gpio_1, pigpio.EITHER_EDGE, cbf)
time.sleep(200)

from time import sleep
from threading import Thread
keep_unlocked = False

def check_code():
    lock_unl()


def lock_unl():
    global keep_unlocked
    print keep_unlocked
    sleep(10)
    print keep_unlocked


def callback(var1,var2):
    global keep_unlocked
    if var1 == 1:
        t = Thread(target=check_code)
        t.start()
    else:
        keep_unlocked = True
