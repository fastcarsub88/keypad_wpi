import json, time, megaio as m
l_min = ''

def lock_log(st):
    with open("lock_log",'a') as f:
        f.write(time.strftime('%D - %H:%M')+' - schedule:'+st+'\n')

def lock_door():
    m.set_relay(0,6,0)
    lock_log('lock')


def unlock_door():
    m.set_relay(0,6,1)
    lock_log('unlock')

def lock_log_trucate():
    with open("lock_log", "r+") as f:
        for x in xrange(50):
            f.readline()
        f.truncate()

def check_pause(pause_arr):
    for value in pause_arr:
        p = value.split('-')
        st = time.mktime(time.strptime(p[0],'%m/%d/%y'))
        et = time.mktime(time.strptime(p[1],'%m/%d/%y'))
        ct = time.time()
        if ct > st and ct < et:
            return True
    return False

def keepunlock(sched):
    times = sched['Weekday']['keepunlock'].split('-')
    t = int(ctime.replace(':',''))
    t1 = int(times[0].replace(':',''))
    t2 = int(times[1].replace(':',''))
    if t > t1 and t < t2:
        return True
    return False

def check_schedule():
    global l_min
    c_min = time.strftime('%M')
    if l_min == c_min:
        return
    l_min = c_min
    with open('schedule.json') as f:
        sch = json.load(f)
    if 'Breaks' in sch:
        if check_pause(sch['Breaks']):
            return
    day = time.strftime('%A')
    ctime = time.strftime('%H:%M')
    if ctime == '00:01':
        lock_log_trucate()
    if day in sch:
        if "keepunlock" in sch[day]:
            if keepunlock(sch):
                return
        if ctime in sch[day]:
            if sch[day][ctime] == 'lock':
                lock_door()
            else:
                unlock_door()
    if 'Weekday' in sch:
        if day == 'Saturday' or day == 'Sunday':
            return
        if "keepunlock" in sch['Weekday']:
            if keepunlock(sch):
                return
        if ctime in sch['Weekday']:
            if sch['Weekday'][ctime] == 'lock':
                lock_door()
            else:
                unlock_door()


while True:
    time.sleep(5)
    check_schedule()
