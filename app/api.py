import cgi,json,pigpio
from time import sleep
def put_codes(jsn):
    with open('allowed_codes.json','w') as f:
         f.write(jsn)
    r = {}
    r['status'] = 200
    return json.dumps(r)

def get_codes():
    with open('allowed_codes.json') as f:
        codes = f.read()
    r = {}
    r['status'] = 200
    r['codes'] = codes
    return json.dumps(r)

def get_schedule():
    with open('schedule.json') as f:
        sch = f.read()
    r = {}
    r['status'] = 200
    r['schedule'] = sch
    return json.dumps(r)

def put_schedule(js):
    with open('schedule.json','w') as f:
        sch = f.write(js)
    r = {}
    r['status'] = 200
    return json.dumps(r)

def get_status():
    global pi
    r = {}
    r['status'] = 200
    if pi.read(17) == 1:
        r['d_status'] =  "locked"
    else:
        r['d_status'] = "unlocked"
    return json.dumps(r)

def lock_unl():
    global pi
    if pi.read(17) == 1:
        pi.write(17,0)
        lock_log('lock')
    else:
        pi.write(17,1)
        lock_log('unlock')
    return get_status()

def lock_log(st):
    with open("lock_log",'a') as f:
        f.write(time.strftime('%D - $H:%M')+' - web:'+st)

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
            response = get_schedule()
        elif post.getvalue("method") == 'put_schedule':
            response = put_schedule(post.getvalue('schedule'))
        else:
            response = get_codes()
    else:
        response = '{"error":"not allowed"}'
    start_response('200',[('Content-Type','text/html'),('Access-Control-Allow-Origin','*')])
    return[response]
pi = pigpio.pi()
