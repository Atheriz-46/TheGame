FIXED_SIZE = 1024


def sendMessage(conn, s):
    """
    Used to send message s using Socket conn.
    Handles underflow and overflow of messages.
    Acts as a middle layer between networks buffers and higher level functions.

    Args:
            conn (Socket) : Socket over which message is to be sent
            s (str) : Message to be sent
    """

    s += "%"
    p = ""
    for i in s:
        p += i
        if len(p.encode("utf-16")) >= FIXED_SIZE:
            conn.send(p.encode("utf-16"))
            p = ""
    if len(p) == 0:
        pass
    else:
        while len(p.encode("utf-16")) < FIXED_SIZE:
            p += "*"
        conn.send(p.encode("utf-16"))


def recieveMessage(conn):
    """
    Used to receive messages over Socket conn

    Args:
            conn (Socket) : Socket over which messages are to be received
    """
    s = ""
    while True:
        curr = conn.recv(FIXED_SIZE).decode("utf-16")
        s += curr
        if "%" in s:
            break
    return s.split("%")[0]
