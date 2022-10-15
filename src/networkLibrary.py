FIXED_SIZE = 1024
def sendMessage(conn,s):
    s+="%"
    p = ''
    for i in s:
        p += i
        if(len(p.encode('utf-16'))>=FIXED_SIZE):
            conn.send(p.encode('utf-16'))
            p = ''
    if len(p)==0:
        pass
    else:
        while len(p.encode('utf-16')) < FIXED_SIZE:
            p+='*'
        conn.send(p.encode('utf-16'))

def recieveMessage(conn):
    s = ''
    while True:
        curr = conn.recv(FIXED_SIZE).decode('utf-16')
        s+=curr
        if '%' in s:
            break
    return s.split('%')[0]