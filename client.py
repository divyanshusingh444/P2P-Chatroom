import select
import socket
from threading import Thread
SPACE = 10

client = None

def getLoginInfo(IP, PORT, username, error):
    global client

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((IP, PORT))
    except Exception as e:
        error(f"Error {str(e)}")
        return False

    username = username.encode('utf-8')
    usernameSpace = f"{len(username):<{SPACE}}".encode('utf-8')
    client.send(usernameSpace + username)
    return True


def sendMsg(msg):
    msg = msg.encode('utf-8')
    msgSpace = f"{len(msg):<{SPACE}}".encode('utf-8')
    client.send(msgSpace+msg)


def listenThread(incomingMsg, error):
    _ = Thread(target=listen, args=(incomingMsg, error))
    _.start()


def listen(incomingMsg, error):
    while True:
        try:
            while True:
                usernameSpace = client.recv(SPACE)

                if not len(usernameSpace):
                    error("Connection Closed By Sever")

                usernameLength = int(usernameSpace.decode('utf-8').strip())
                username = client.recv(usernameLength).decode('utf-8')

                msgSpace = client.recv(SPACE)
                msgLength = int(msgSpace.decode('utf-8').strip())
                msg = client.recv(msgLength).decode('utf-8')

                incomingMsg(username, msg)

        except Exception as e:
            error(f"Error: {str(e)}")















