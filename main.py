version = "v1.0.0"

import csv
import argparse

from shopwareconnection import ShopwareConnection
from util import printLog, getShopwareArticleId, updateArticleStock


def main():
    shConn = ShopwareConnection(args.url, args.username, args.passwort)
    if not shConn.login():
        print("Logon failed")
        return
    with open(args.datei) as csv_file:
        articles = list(csv.reader(csv_file, delimiter=args.trennzeichen))
        aktArticle = 1
        totArticle = len(articles)
        for row in articles:
            artNo = row[0]
            bestand = row[1]
            printLog(f"{artNo}: {bestand} ({aktArticle}/{totArticle}) => ", True)
            artId = getShopwareArticleId(args.url, shConn, artNo)
            if artId:
                statusCode = updateArticleStock(args.url, shConn, artId, bestand)
                if statusCode == 200 or statusCode == 204:
                    print("OK")
                else:
                    print("FAIL")
            else:
                print("FAIL")
            aktArticle += 1


if __name__ == '__main__':
    printLog("**********************************START**********************************************")
    printLog(f"{version}")
    argParser = argparse.ArgumentParser()
    argParser.add_argument("--url", help="URL zum Shop", required=True)
    argParser.add_argument("--username", help="Username", required=True)
    argParser.add_argument("--passwort", help="Passwort", required=True)
    argParser.add_argument("--datei", help="Pfad zur .csv-Datei", required=True)
    argParser.add_argument("--trennzeichen", help="Trennzeichen welches in der csv-Datei genutzt wird", default=",")
    args = argParser.parse_args()
    main()
    printLog("***********************************END***********************************************")
