import socket,sys
import threading
import os
from response import generateResponse 

#Ideally get this from the config file
documentRoot = '/home/anup08/Desktop/CNProj/mhttp-server/src'

def matchAccept(headers):
    k = headers.split(',')
    # for i in k:
        # print(i)



def parse_GET_Request(headers):
    # TODO
    # Implement Conditional Get
    # Implement Range Header
    # MIME Encoding response 
    params = {}
    for i in headers[1:]:
        try:
            headerField = i[:i.index(':')] 
            params[headerField] = i[i.index(':') + 2 : len(i) - 1]
        except :
            pass

    # print(params)
    # Return 406 on not getting file with desired accept
    matchAccept(params['Accept'])
    path = headers[0].split(' ')[1]
    try:
        if(path == "/"):
            path = 'index.html'
        else:
            path = documentRoot + path
        f = open(path,"r")
        # print("OK")
        res = generateResponse(200)
        return res #Proper data encoding and sending as a HTTP response
    except FileNotFoundError:
        res = generateResponse(404)
        return res #Change to proper HTTP response


def parse_POST_Request(headers):
    pass
def parse_PUT_Request(headers):
    pass
def parse_HEAD_Request(headers):
    pass
def parse_DELETE_Request(headers):
    pass

def process(data):
    try:
        headers = [i for i in data.split('\n')]
        tokens = headers[0].split(' ')
        method = tokens[0]
        
        if(method == 'GET'):
            return parse_GET_Request(headers)
        elif (method == 'POST'):
            parse_POST_Request(headers)
        # elif (method == 'PUT'):
        #     parse_PUT_Request(headers)
        # elif (method == 'HEAD'):
        #     parse_HEAD_Request(headers)
        # elif (method == 'DELETE'):
        #     parse_DELETE_Request(headers)
        return
    except:
        print("Return 400 Bad request")
        return "400"






if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('',int(sys.argv[1])))
    s.listen(90)

    print("Listening on port {}".format(sys.argv[1]))
    # TODO
    # Implement with multithreading 
    while 1:
        clientsocket, clientaddr = s.accept()
        # threading.Thread()
        try:
            while 1:
                data = clientsocket.recv(1024).decode('utf-8')
                res = process(data)
                print(res)
                if('\r\n\r\n' in data):
                    break
            res = res.encode('utf-8')
            clientsocket.sendall(res)
        except:
            print("err")
        finally:
            clientsocket.close()

