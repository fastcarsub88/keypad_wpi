import pigpio,wiegand,json,threading,time,megaio as m

input = ''
keep_unlocked = False
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
    global keep_unlocked
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
        if keep_unlocked == True:
            lock_log(usr,'no-relock')
            keep_unlocked = False
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

def callback(bits,btn):
    global input, keep_unlocked, lst_btn_tm
    if btn == 11:
        t = threading.Thread(target=check_code, args=(input,))
        t.start()
        input = ''
    elif bits == 26:
        t = threading.Thread(target=check_code, args=(str(btn),))
        t.start()
        input = ''
    elif btn == 10:
        keep_unlocked = True
        input = ''
    else:
        if time.time() - lst_btn_tm > 15:
            input = ''
        input += str(btn)
        lst_btn_tm = time.time()

pi = pigpio.pi()
w = wiegand.decoder(pi,22,27,callback)
while True:
    time.sleep(5)
