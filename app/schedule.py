import pigpio,json
import time
l_min = ''

def lock_log(st):
    with open("lock_log",'a') as f:
        f.write(time.strftime('%D - $H:%M')+' - schedule:'+st)

def lock_door():
    pi.write(17,1)
    lock_log('lock')


def unlock_door():
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

def check_schedule():
    global l_min
    c_min = time.strftime('%M')
    if l_min == c_min:
        return
    with open('schedule.json') as f:
        sch = json.load(f)
    if 'Breaks' in sch:
        if check_pause(sch['Breaks']):
            return
    day = time.strftime('%A')
    ctime = time.strftime('%H:%M')
    if day in sch:
        if ctime in sch[day]:
            if sch[day][ctime] == 'lock':
                lock_door()
            else:
                unlock_door()
    if 'Weekday' in sch:
        if ctime in sch['Weekday']:
            if sch['Weekday'][ctime] == 'lock':
                lock_door()
            else:
                unlock_door()


while True:
    time.sleep(5)
    check_schedule()
