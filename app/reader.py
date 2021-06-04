import pigpio,wiegand,json,time,threading


input = ''
keep_unlocked = False

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
    if pi.read(17) == 0:
        pi.write(17,1)
        lock_log(usr,'lock')
    else:
        pi.write(17,0)
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
            pi.write(17,1)
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
    global input, keep_unlocked
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
    else:
        input += str(btn)

pi = pigpio.pi()
pi.set_mode(17,pigpio.OUTPUT)
pi.write(17,1)
w = wiegand.decoder(pi,14,15,callback)

while True:
    time.sleep(5)
