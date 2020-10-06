import socket, sys
import threading
import os
from response import generateResponse

#Ideally get this from the config file
documentRoot = '/home/anup08/Desktop/CNProj/mhttp-server/src'
resource = None
f = None


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
            params[headerField] = i[i.index(':') + 2:len(i) - 1]
        except:
            pass

    # print(params)
    # Return 406 on not getting file with desired accept
    matchAccept(params['Accept'])
    path = headers[0].split(' ')[1]
    length = 0
    try:
        if (path == "/"):
            path = 'index.html'
        else:
            path = documentRoot + path
        global resource
        global f
        f = open(path, "r")
        resource = f.read()
        lastModified = os.path.getmtime(path)
        try:
            length = len(resource)
        except:
            pass
        res = generateResponse(length, 200, resource, lastModified)
        return res
    except FileNotFoundError:
        res = generateResponse(length, 404)
        return res


def parse_POST_Request(headers):
    # TODO
    # Annotation of existing resources
    # Posting message to an existing bulleting, news board etc
    # Providing a block of data, such as the result of submitting a form, to a data-handling process
    # Extending a database through an append operation.

    # For the purpose of the project, POST methods will write the incoming data into a logs file

    params = {}
    body = []
    for i in headers[1:]:

        try:
            headerField = i[:i.index(':')]
            params[headerField] = i[i.index(':') + 2:len(i) - 1]
        except:
            body.append(i)

    path = headers[0].split(' ')[1]
    path = documentRoot + path

    if (path == "/"):
        path = 'index.html'

    # Check if file at path is write-able else respond with FORBIDDEN response
    if os.path.exists(path):
        if os.access(path, os.W_OK):
            f1 = open(path, 'w+')
            response_code = 200
        else:
            response_code = 403
    else:
        f1 = open(path, 'w+')
        response_code = 201

    if response_code == 403:
        res = generateResponse(403)
        return res

    f2 = open('./logs/post_log.txt', 'w+')
    global resource
    resource = f1.read()
    # Handle application/x-www-form-urlencoded type of data
    content_type = params['Content-Type']
    if "application/x-www-form-urlencoded" in content_type:
        # example string name1=value1&name2=value2
        form_data = {}

        for line in body:
            line = line.split('&')
            for param in line:
                param = param.split('=')
                form_data[param[0]] = param[1]

        f2.write(str(form_data))

    res = generateResponse(len(resource), response_code, resource, None)
    return res


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

        if (method == 'GET'):
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
    except e:
        print(e)
        print("Return 400 Bad request")
        return generateResponse(0, 400)


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', int(sys.argv[1])))
    s.listen(90)

    print("Listening on port {}".format(sys.argv[1]))
    # TODO
    # Implement with multithreading
    while 1:
        clientsocket, clientaddr = s.accept()
        # threading.Thread()
        try:
            while 1:
                data = clientsocket.recv(5000).decode('utf-8')
                # print(data)
                res = process(data)
                if ('\r\n\r\n' in data):
                    break

            print(res)
            clientsocket.send(res.encode('utf-8'))

        except e:
            print(e)
            print("err")
        finally:
            clientsocket.close()
            f.close()
