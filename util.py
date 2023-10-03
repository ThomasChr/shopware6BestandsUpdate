import os
import requests
import datetime

myPid = os.getpid()


def printLog(logtext, noNewline):
    if noNewline:
        print(datetime.datetime.now().astimezone().isoformat() + " (" + str(myPid) + ") => " + logtext, flush=True, end="")
    else:
        print(datetime.datetime.now().astimezone().isoformat() + " (" + str(myPid) + ") => " + logtext, flush=True)


def getShopwareToken(url, username, passwort):
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    payload = {"client_id": "administration", "grant_type": "password", "scopes": "write", "username": username, "password": passwort}
    r = requests.post(url + "/api/oauth/token", headers=headers, json=payload).json()
    return r["access_token"]


def getShopwareArticleId(url, shopwareToken, articleNo):
    shopwareID = ""
    headers = {"Accept": "application/json", "Authorization": "Bearer " + shopwareToken}
    payload = {"filter": [{"type": "equals", "field": "productNumber", "value": articleNo}], "includes": {}}
    payload["includes"]["product"] = ["id"]
    r = requests.post(url + "/api/search/product", json=payload, headers=headers).json()
    if 'errors' in r:
        raise ValueError(r)
    if 'data' in r and len(r['data']) == 1:
        shopwareID = r['data'][0]['id']
    return shopwareID


def updateArticleStock(url, shopwareToken, productID, stock):
    headers = {"Accept": "application/json", "Authorization": "Bearer " + shopwareToken}
    payload = {"stock": int(stock)}
    r = requests.patch(url + f"/api/product/{productID}", json=payload, headers=headers)
    return r.status_code
