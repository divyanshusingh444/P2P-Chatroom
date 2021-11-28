import socket
import select

SPACE = 10

IP = ''
# IP = '127.0.0.1'
PORT = 42069


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((IP,PORT))
server.listen(15)

socketsList = [server]
clients = {}

print(f"Waiting for connection on {socket.gethostbyname(socket.gethostname())}")


def recv_msg(clientSocket):
    try:
        msgSpace = clientSocket.recv(SPACE)
        if not len(msgSpace):
            return False
        msgLength = int(msgSpace.decode('utf-8').strip())
        return {'space': msgSpace, 'msg': clientSocket.recv(msgLength)}
    except:
        return False


while True:
    incomingSockets, writeSockets, exceptionSockets = select.select(socketsList, [], socketsList)
    print(incomingSockets)
    for fromSocket in incomingSockets:

        if fromSocket == server:
            clientSocket, clientAddress = server.accept()
            user = recv_msg(clientSocket)
            if user is False:
                continue
            socketsList.append(clientSocket)
            clients[clientSocket] = user
            print(f"Connected to {clientAddress} as {clients[clientSocket]['msg'].decode('utf-8')}")
        else:
            msg = recv_msg(fromSocket)
            if msg is False:
                print(f"Connection closed by {clients[fromSocket]['msg'].decode('utf-8')}")
                socketsList.remove(fromSocket)
                del(clients[fromSocket])
                continue
            user = clients[fromSocket]
            print(f"Incoming message from {user['msg'].decode('utf-8')}")
            recipient = ""
            txt = msg['msg'].decode('utf-8')
            if msg['msg'].decode('utf-8')[0:3] == "!p!":
                for i in range(5,int(msg['space'].decode('utf-8'))):
                    if(txt[i]==" "):
                        break
                    else:
                        recipient+=txt[i]
            try:
                for each in clients:
                    if clients[each] == recipient:
                        recipient = each
            except:
                pass
            if recipient == "":
                for client in clients:
                    if client != fromSocket:
                        client.send(user['space'] + user['msg'] + msg['space'] + msg['msg'])
            else:
                for client in clients:
                    if client != fromSocket:
                        client.send(user['space'] + user['msg'] + msg['space'] + msg['msg'])
    for fromSocket in exceptionSockets:
        socketsList.remove(fromSocket)
        del clients[fromSocket]

















