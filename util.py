import os
import requests
import datetime

from shopwareconnection import ShopwareConnection

myPid = os.getpid()

requestsSession = requests.Session()


def printLog(logtext, noNewline=False):
    if noNewline:
        print(datetime.datetime.now().astimezone().isoformat() + " (" + str(myPid) + ") => " + logtext, flush=True, end="")
    else:
        print(datetime.datetime.now().astimezone().isoformat() + " (" + str(myPid) + ") => " + logtext, flush=True)


def getShopwareArticleId(url, shConn: ShopwareConnection, articleNo):
    shopwareID = ""
    payload = {"filter": [{"type": "equals", "field": "productNumber", "value": articleNo}], "includes": {}}
    payload["includes"]["product"] = ["id"]
    r = shConn.makeAuthenticatedRequest("/api/search/product", shConn.requestsSession.post, payload)
    if 'errors' in r:
        raise ValueError(r)
    if 'data' in r and len(r['data']) == 1:
        shopwareID = r['data'][0]['id']
    return shopwareID


def updateArticleStock(url, shConn, productID, stock):
    payload = {"stock": int(stock)}
    r = shConn.makeAuthenticatedRequest("/api/search/product", shConn.requestsSession.post, payload)
    return r.status_code
