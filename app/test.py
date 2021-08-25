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

import time, threading

keep_unlocked = False

def check_code(str):
    lock_unl("str")


def lock_unl(var1):
    global keep_unlocked
    print keep_unlocked
    time.sleep(10)
    print keep_unlocked
    keep_unlocked = False


def callback(var1,var2):
    global keep_unlocked
    if var1 == 1:
        t = threading.Thread(target=check_code,args=('str', ))
        t.start()
    else:
        keep_unlocked = True
