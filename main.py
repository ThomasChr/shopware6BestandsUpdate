import csv
import argparse

from util import printLog, getShopwareToken, getShopwareArticleId, updateArticleStock


def main():
    shopwareToken = getShopwareToken(args.url, args.username, args.passwort)
    with open(args.datei) as csv_file:
        articles = list(csv.reader(csv_file, delimiter=','))
        aktArticle = 1
        totArticle = len(articles)
        for row in articles:
            artNo = row[0]
            bestand = row[1]
            printLog(f"{artNo}: {bestand} ({aktArticle}/{totArticle})")
            artId = getShopwareArticleId(args.url, shopwareToken, artNo)
            updateArticleStock(args.url, shopwareToken, artId, bestand)
            aktArticle += 1


if __name__ == '__main__':
    printLog("**********************************START**********************************************")
    argParser = argparse.ArgumentParser()
    argParser.add_argument("--url", help="URL zum Shop", required=True)
    argParser.add_argument("--username", help="Username", required=True)
    argParser.add_argument("--passwort", help="Passwort", required=True)
    argParser.add_argument("--datei", help="Pfad zur .csv-Datei", required=True)
    args = argParser.parse_args()
    main()
    printLog("***********************************END***********************************************")
