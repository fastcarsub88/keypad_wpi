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
