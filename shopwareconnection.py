import time
import typing
import datetime
import threading

import requests

tokenlock = threading.Lock()


class ShopwareConnection:
    def __init__(self, url: str, username: str, password: str) -> None:
        self.url = url
        self.username = username
        self.password = password
        self.htaccessUsername: str = ""
        self.htaccessPassword: str = ""
        self.token: str = ""
        self.refreshToken: str = ""
        self.tokenExpiry: datetime = datetime.datetime.now()
        self.requestsSession = requests.Session()

    def login(self) -> bool:
        self.token, self.refreshToken, self.tokenExpiry = self.__getToken()
        if self.token != "":
            return True
        return False

    def __getToken(self) -> (str, str, datetime):
        requrl = "/api/oauth/token"
        payload = {"client_id": "administration", "grant_type": "password", "scopes": "write", "username": self.username, "password": self.password}
        r = self.makeUnAuthenticatedRequest(requrl, payload)
        if "access_token" in r:
            return r["access_token"], r["refresh_token"], datetime.datetime.now() + datetime.timedelta(seconds=int(r["expires_in"]))
        else:
            return "", "", datetime.datetime.now()

    def __getRefreshToken(self) -> (str, str, datetime):
        requrl = "/api/oauth/token"
        payload = {"client_id": "administration", "grant_type": "refresh_token", "refresh_token": self.refreshToken}
        r = self.makeUnAuthenticatedRequest(requrl, payload)
        if "access_token" in r:
            return r["access_token"], r["refresh_token"], datetime.datetime.now() + datetime.timedelta(seconds=int(r["expires_in"]))
        else:
            return "", "", datetime.datetime.now()

    def makeUnAuthenticatedRequest(self, requrl: str, payload: dict) -> dict:
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        if self.htaccessUsername or self.htaccessPassword:
            return self.requestsSession.post(self.url + requrl, headers=headers, json=payload, auth=(self.htaccessUsername, self.htaccessPassword)).json()
        else:
            return self.requestsSession.post(self.url + requrl, headers=headers, json=payload).json()

    def makeAuthenticatedRequest(self, requrl: str, func: typing.Callable, payload: dict | None = None, data: typing.Any | None = None, returnType = "json") -> dict:
        with tokenlock:
            if (datetime.datetime.now() + datetime.timedelta(minutes=1)) > self.tokenExpiry:
                self.token, self.refreshToken, self.tokenExpiry = self.__getRefreshToken()
        r = self.__makeAuthenticatedRequest(requrl, func, payload, data, returnType)
        # Deadlock, wait and try again
        if "errors" in r and len(r["errors"]) > 0 and isinstance(r["errors"], list) and r["errors"][0]["status"] == '500' and r["errors"][0]["code"] == '1213':
            for _ in range(10):
                time.sleep(0.010)
                r = self.__makeAuthenticatedRequest(requrl, func, payload, data, returnType)
                if "errors" not in r:
                    break
        return r

    def __makeAuthenticatedRequest(self, requrl: str, func: typing.Callable, payload: dict | None, data: typing.Any | None = None, returnType = "json") -> dict:
        if data:
            headers = {"Accept": "application/json", "Authorization": "Bearer " + self.token}
            r = func(self.url + requrl, headers=headers, data=data)
        elif payload:
            headers = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": "Bearer " + self.token}
            r = func(self.url + requrl, headers=headers, json=payload)
        else:
            headers = {"Accept": "application/json", "Authorization": "Bearer " + self.token}
            r = func(self.url + requrl, headers=headers)
        if returnType == "json":
            try:
                retVal = r.json()
            except:
                retVal = r.text
        else:
            retVal = r
        return retVal
