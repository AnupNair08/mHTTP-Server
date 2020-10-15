import pytz
import datetime
from utils.statusCodes import codes
from utils.responseHeaders import responseHeaders
from utils.entityHeaders import entityHeaders

# Response = Status Line + Response Headers + Entity Headers + Entity Body

def metaData(code):
    date = datetime.datetime.now(tz=pytz.utc)
    time = " {}:{}:{} GMT".format(date.strftime("%H"), date.strftime("%M"),date.strftime("%S"))
    date = date.strftime("%a") + ', ' + str(date.strftime("%d")) + " " + date.strftime("%b") + " " + str(date.year) + time

    statusLine = "HTTP/1.1 {} {}\r\n".format(code, codes[code])
    responseheaders = "Server: mHTTP-Alpha1\r\n"
    return date, statusLine + responseheaders

def generateGET(headers):
    code = headers['code']
    if (code not in codes.keys()):
        return
    date, response = metaData(code)

    entityheaders = "Content-Type: {}\r\nDate: {}\r\nContent-Length: {}\r\nConnection: keep-alive\r\nSet-Cookie: anup=nair\r\nAllow: {}\r\nE-Tag: {}\r\n\r\n".format(
    headers['ctype'], date, headers['length'], entityHeaders['Allow'],headers['etag'])

    return response + entityheaders


def generateResponse(length,code,resource=None,lastModified=None,ctype="text/html;charset=UTF-8",method="",encoding="gzip",etag="changelater"):
    if (code not in codes.keys()):
        return
    
    date , response = metaData(code)

    # lastModified = datetime.datetime(int(lastModified))
    # if(ctype != "text/html;charset=UTF-8"):
    #     ctype = ctype
    # print(ctype)

    entityheaders = "Content-Type: {}\r\nDate: {}\r\nContent-Length: {}\r\nConnection: keep-alive\r\nSet-Cookie: anup=nair\r\nAllow: {}\r\nE-Tag: {}\r\n\r\n".format(
        ctype, date, length, entityHeaders['Allow'],etag)

    return response + entityheaders
