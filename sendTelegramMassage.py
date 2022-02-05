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
    href =soup(html,'html5lib').find_all('a',{'class':'kt-post-card kt-post-card--outlined kt-post-card--has-chat'})
    return href

def getShortURL(longURL):
    return 'https://divar.ir/v/'+longURL.split('/')[-1]


def GetContent(adsURL):# This function Get phone, area and comment of ads
    testH ='https://divar.ir'+adsURL.get('href')
    #Get comment area_________________________
    html=req.get(testH).text
    #print(html)
    temp=soup(html,'html5lib').find('div',{'class':'kt-base-row kt-base-row--large kt-description-row kt-description-row--padded'})
    comments=str(temp)
    comments=(html2text.html2text(comments))
    return comments



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






    
