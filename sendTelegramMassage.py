"Author: Hamid Mahmoodabadi"

import schedule
import time
import requests
from bs4 import BeautifulSoup as soup
import requests as req
import html2text
import re
import time
filePath='logs.log'
phoneLogs='phoneLogs.log'

def getAdsURL(firstPageURL):# This function get all ads url adres's
    html =req.get(firstPageURL).text
    href =soup(html,'lxml').find_all('a',{'class':'kt-post-card kt-post-card--outlined kt-post-card--has-chat'})
    return href

def getShortURL(longURL):
    return 'https://divar.ir/v/'+longURL['href'].split('/')[-1]


def GetContent(shortURL):# This function Get phone, area and comment of ads
    html=req.get(shortURL).text
    text=soup(html,'lxml').find('p',{'class':'kt-description-row__text post-description kt-description-row__text--primary'})
    comments=str(text.text)
    price = ''.join([i.text+'\n' for i in soup(html,'lxml').find_all('div',{'class':'kt-base-row kt-base-row--large kt-unexpandable-row'})])
    return comments+'\n'+price


for item in getAdsURL('https://divar.ir/s/tehran'):
    shortURL = getShortURL(item)
    content = GetContent(shortURL)
    text = '___________________________________________' + '\n' + shortURL + "\n" + content + "\n"
    print(text)
    time.sleep(2)
























def mainFunc(channelAddress,divarURL,rentOrSale):
   try:
    token='402534967:AAH-vMKfI1OlpNnusY0HD5kpWDGn2QJl3AA'
    method='sendMessage'
    
    aaa=divarURL
    href=getAdsURL(firstPageURL=aaa)
    i=0
    for item in href:
     content=GetContent(item)
     shortURL=getShortURL(item.get('href'))
     i+=1
     if shortURL in open(str(filePath)).read().split():
         print('Exist Ads '+str(i))
         #with open(str(filePath), "a+") as text_file:
          #   text_file.write("\n"+str(shortURL))
         break
     if(contentNotExistInBlackList(content,shortURL,rentOrSale)):#send contetn for check in BlackList and URL for not exist
        print('Sending ...')
        try:
             with open(str(filePath), "a+") as text_file:
                text_file.write("\n"+str(shortURL))
        except Exception as e:
             print('cant Write exist ads to file ' + str(e))
        try:
             text='___________________________________________'+'\n'+shortURL+"\n"+content+"\n"
             response = requests.post(
             url='https://api.telegram.org/bot{0}/{1}'.format(token, method),
             data={'chat_id':channelAddress, 'text': text}
             ).json()
        except Exception as e:
            print('cant send data '+str(e))
   except Exception as e:
       print('cant execute code : '+ str(e))
       print(channelAddress)






    
