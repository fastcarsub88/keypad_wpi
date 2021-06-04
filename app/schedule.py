import pigpio,json
from time import sleep

def lock_log(st):
    with open("lock_log",'a') as f:
        f.write(time.strftime('%D - $H:%M')+' - schedule:'+st)

def lock_door():
    pi.write(17,1)
    lock_log('lock')


def unlock_door(arg):
    pi.write(17,0)
    lock_log('unlock')

def check_pause(pause_arr):
    for value in pause_arr:
        p = value.split('-')
        st = time.mktime(time.strptime(p[0],'%m/%d/%y'))
        et = time.mktime(time.strptime(p[1],'%m/%d/%y'))
        ct = time.time()
        if ct > st and ct < et:
            return True
    return False

def check__schedule(arg):
    global l_min
    c_min = time.strftime('%M')
    if l_min == c_min:
        return
    with open('schedule.json') as f:
        sch = json.load(f)
    if 'breaks' in sch:
        if check_pause(sch['breaks']):
            return
    day = time.strftime('%A')
    time = time.strftime('%H:%M')
    if day in sch:
        if time in sch[day]:
            if sch[day][time] == 'lock':
                lock_door()
            else:
                unlock_door()
    if 'weekday' in sch:
        if time in sch['weekday']:
            if sch['weekday'][time] == 'lock':
                lock_door()
            else:
                unlock_door()


while True:
    sleep(5)
    check_schedule()
