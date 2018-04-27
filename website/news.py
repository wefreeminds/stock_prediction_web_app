import csv
from lxml import etree
import requests
from time import strftime, sleep
from datetime import datetime
from dateutil import parser
# import MySQLdb
# from goose import Goose

def get_news(query):
    parser = etree.HTMLParser()



    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

  
    results=[]
    
    query = "https://www.google.com/search?sa=X&q='"+query+"+stock'&tbm=nws&source=univ&tbo=u&num=100&ved=0ahUKEwj9y_K_gNfaAhWRT98KHZsHDwcQt8YBCEIoAQ&biw=1517&bih=653"
    try:
        resp = requests.get(query, headers=headers).content
       
    except Exception,e:
        print "failed url: " + query
       
        sleep(5)
        

    tree = etree.fromstring(resp, parser)
    path='//h3'
    path+="[@class='"+tree.xpath(path)[0].get('class')+"']/a"
    h3=tree.xpath(path)

    blurbs=tree.xpath("//div[@class='st']") 
    for h,b in zip(h3,blurbs):
       
        if b.text is not None and h.text is not None and len(h.text.split(' '))>4:
            results.append({'excerpt':b.text,'title':h.text,'link':h.get('href')})
    return results

    

    
    
 