import pigpio,wiegand,json,threading,time,megaio as m

input = ''
keep_unlocked = 'false'
lst_btn_tm = 0

def lock_log(usr,st):
    with open('lock_log') as f:
        a = f.readlines();
    if len(a) > 14:
        del a[0];
    a.append(time.strftime('%D - %H:%M')+' - '+usr+':'+st+"\n")
    with open("lock_log",'w') as f:
        f.write(''.join(a))

def lock_unl(usr):
    pi.write(17,0)
    time.sleep(0.5)
    pi.write(17,1)
    if '{0:08b}'.format(m.get_relays(0))[2] == '1':
        m.set_relay(0,6,0)
        lock_log(usr,'lock')
    else:
        m.set_relay(0,6,1)
        lock_log(usr,"unlock")
        with open('config.json') as f:
            cnf = json.load(f)
        if cnf['relock'] == 'false':
            return
        time.sleep(int(cnf['relock_delay']))
        if keep_unlocked == 'true':
            lock_log(usr,'no-relock')
            set_keep_unlocked('false')
            return
        else:
            m.set_relay(0,6,0)
            lock_log(usr,'relock')

def check_code(code):
    codes = []
    with open('allowed_codes.json') as f:
        codes = json.load(f)
    if 'new_card' in codes:
        with open('allowed_codes.json','w') as t:
            codes[code] = codes.pop('new_card')
            t.write(json.dumps(codes))
            return
    if code in codes:
        lock_unl(codes[code])

def set_keep_unlocked(state):
    global keep_unlocked
    keep_unlocked = state

def callback(bits,btn):
    global input, lst_btn_tm
    if btn == 11:
        t = threading.Thread(target=check_code, args=(input,))
        t.start()
        input = ''
    elif bits == 26:
        t = threading.Thread(target=check_code, args=(str(btn),))
        t.start()
        input = ''
    elif btn == 10:
        lock_log("test",'star pressed')
        set_keep_unlocked('true')
        input = ''
    else:
        timestamp = time.time()
        if timestamp - lst_btn_tm > 5:
            input = ''
            set_keep_unlocked('false')
        input += str(btn)
        lst_btn_tm = timestamp

pi = pigpio.pi()
pi.set_mode(17, pigpio.OUTPUT)
pi.write(17,1)
w = wiegand.decoder(pi,22,27,callback)
while True:
    time.sleep(5)
