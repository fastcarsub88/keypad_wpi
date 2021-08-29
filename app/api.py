import cgi,json,pigpio,time,megaio as m

def put_codes(jsn):
    with open('allowed_codes.json','w') as f:
         f.write(jsn)
    r = {}
    r['status'] = 200
    return json.dumps(r)

def get_data(file,name):
    with open(file) as f:
        a = f.read()
    r = {}
    r['status'] = 200
    r[name] = a
    return json.dumps(r)

def put_schedule(js):
    with open('schedule.json','w') as f:
        sch = f.write(js)
    r = {}
    r['status'] = 200
    return json.dumps(r)

def get_status():
    r = {}
    r['status'] = 200
    if '{0:08b}'.format(m.get_relays(0))[2] == '0':
        r['d_status'] =  "locked"
    else:
        r['d_status'] = "unlocked"
    return json.dumps(r)

def lock_unl():
    if '{0:08b}'.format(m.get_relays(0))[2] == '1':
        m.set_relay(0,6,0)
        lock_log('lock')
    else:
        m.set_relay(0,6,1)
        lock_log("unlock")
    return get_status()

def lock_log(st):
    with open("lock_log",'a') as f:
        f.write(time.strftime('%D - %H:%M')+' - web:'+st+'\n')

def application(env, start_response):
    if env['REQUEST_METHOD'] == 'POST':
        post_env = env.copy()
        post_env['QUERY_STRING'] = ''
        post = cgi.FieldStorage(
            fp=env['wsgi.input'],
            environ=post_env,
            keep_blank_values=True
        )
        with open('apikey.json') as f:
            k = json.load(f)
        if post.getvalue("key") != k["key"]:
            response = '{"error":"Unauthorized"}'
        elif post.getvalue("method") == 'put_codes':
            response = put_codes(post.getvalue("codes"))
        elif post.getvalue("method") == 'lock_unl':
            response = lock_unl()
        elif post.getvalue("method") == 'get_status':
            response = get_status()
        elif post.getvalue("method") == 'get_schedule':
            response = get_data('schedule.json','schedule')
        elif post.getvalue("method") == 'get_lock_log':
            response = get_data('lock_log','lock_log')
        elif post.getvalue("method") == 'put_schedule':
            response = put_schedule(post.getvalue('schedule'))
        else:
            response = get_data('allowed_codes.json','codes')
    else:
        response = '{"error":"not allowed"}'
    start_response('200',[('Content-Type','text/html'),('Access-Control-Allow-Origin','*')])
    return[response]
pi = pigpio.pi()
