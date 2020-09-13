# -*- coding: utf-8 -*-

import requests
from concurrent.futures import ThreadPoolExecutor
import time
from bs4 import BeautifulSoup
import lxml




def urlname():
    url = input('Please input url:')
    #newurl = "'"+url+"'"
    newurl = url.strip()
    return newurl

def getUrltarget(url):
    # url = url
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
    with open('../lib/urldonelist',"r") as urlist:
            content = urlist.read()
            if content.find(url):
                urlscode = 1
            else:
                urlscode = 0
    if urlscode == 0:
        try:
            target = requests.get(url,headers=headers,timeout=5)
            if target.status_code == 200:
                with open('../lib/urldonelist',"a+") as urlist:
                            urlist.write(url)
                return target
        except Exception as e:
            with open("../log/log","a+") as log:
                log.write('\n')
                log.write(e)
                log.write('\n')
            #print("Get target failed.Retrying...")
            with open('../lib/urldonelist',"r") as urlist:
                content = urlist.read()
                if content.find(url):
                    urlscode = 1
                else:
                    urlscode = 0
            if urlscode == 0:
                k = 0
                for i in range(1,5):
                    #print('Retrying...No.%s' % i)
                    target = requests.get(url, headers=headers, timeout=5)
                    if target.status_code == 200:
                        with open('../lib/urldonelist',"a+") as urlist:
                            urlist.write(url)
                        return target
                    else:
                        k = k+1
                if k == 5:
                    print('Failed '+url)



def getSoup(target):
    soup = BeautifulSoup(target.content,'lxml')
    return soup


def getSigmaContent(soup):
    sigmaname = []
    sigmaurl = []
    body = soup.body
    main = body.main
    sigmatr = main.find_all('tr',attrs={"class":"litem dir"})
    k = [i.a['href'] for i in sigmatr]
    print(k)
    #print(sigmatr)
    return sigmaname,sigmaurl



m = getUrltarget('https://thetrove.net/Books/7th%20Sea%20Guides/index.html')
print(m)