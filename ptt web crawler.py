import requests
from bs4 import BeautifulSoup
from flask import Flask, request, abort
#from requests.packages.urllib3.exceptions import InsecureRequestWarningrequests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def getPageNumber(content):   #取得網頁最新的一頁
    startIndex = content.find('index')
    endIndex = content.find('.html')
    pageNumber = content[startIndex+5: endIndex]
    print(content)
    print(int(pageNumber) + 1)
    return int(pageNumber) +1


#c = 'https://www.ptt.cc/bbs/movie/index.html'
cc='https://www.ptt.cc/bbs/movie/index8937.html'
r = getPageNumber(cc)


'''def crawlHotActicle(res):
    soup = BeautifulSoup(res.text, 'html.parser') #用beautifulSoup解析html代碼並存入變數soup中
    articleList = []
    for r_ent in soup.find_all(class_='r-ent'): #找出這網址內所有class_='r-ent' 找出...
        #print("***********************************************")
        #print(r_ent)
        if (r_ent.find(class_='h1 f1')):
            hot = r_ent.find(class_='h1 f1').text.strip() #取的推文'爆' h1 f2 則是推文數
            try:
                #先的到每篇文章的ur1
                link = r_ent.find('a')['href'] #link是網頁網址 
                if link:
                    #確定得到ur1再去抓 標題 以及 推文數
                    title = r_ent.find(class_='title').text.strip() #取得標題
                    ur1_link = 'https://www.ptt.cc' + link #取的連結 完整網址
                    articleList.append({
                            'ur1_link': ur1_link,        #將連接放到串列中
                            'title': title,              #將標題放在串列中
                            'hot': hot                   #推文數放到串列中
                            })
            except Exception as e:                       #如果連不上這網址可能被刪文了 e是變數
                 #print (u'crawPage function error:',r_ent.find(class_='title').text.strip())
                 #print('本文已被刪除')
                 #print('delete',e)
        if (r_ent.find(class_='h1 f3')):
            #class是python的保留字  class_代表html的class屬性
    
            hot = r_ent.find(class_='h1 f3').text.strip()
            #print(r_ent.find(class_='h1 f3').text.strip)
            print(hot)
            try :
                link=r_ent.find('a')['href']
                if link:
                    title=r_ent.find(class_='title').text.strip()
                    url_link='https://www.ptt.cc'+link
                    articleList.append({
                            'url_link': url_link,
                            'title': title,
                            'hot':   hot  
                            })
            except Exception as e:
                print('delete',e)
                
                return articleList'''

def crawlHotActicle(res):
    soup = BeautifulSoup(res.text, 'html.parser')
    #print('**************************************************1')
    #print(soup)
    articleList=[]
    for r_ent in soup.find_all(class_="r-ent"):
        print('**************************************************2')
        print(r_ent)
        if r_ent.find(class_="hl f1") or r_ent.find(class_="hl f3"):
            print('**************************************************3')
            if (r_ent.find(class_='hl f1')):
                hot = r_ent.find(class_='hl f1').text.strip()
                try:
                    link = r_ent.find('a')['href']
                    #print('**************************************************4')
                    if link:
                        title = r_ent.find(class_='title').text.strip()
                        url_link = 'https://www.ptt.cc' + link
                        articleList.append({
                               'url_link': url_link,         
                               'title': title,
                                'hot': hot
                                })
                        #print('**************************************************5')
                        #print(url_link)
                except Exception as e:
                    #print('**************************************************6')
                    print('delete', e)
            
            if (r_ent.find(class_='hl f3')):
                hot = r_ent.find(class_='hl f3').text.strip()  
                try:
                    link = r_ent.find('a')['href']
                    if link:
                        title = r_ent.find(class_='title').text.strip()
                        url_link = 'https://www.ptt.cc' + link
                        articleList.append({
                                'url_link': url_link,
                                'title': title,
                                'hot': hot
                                })
                except Exception as e:
                    print('delete', e)
        #print('**************************************************')
        #print(articleList)
    return articleList
    





def sortHot(content):
    return content['hot']





def crawPtt(plate):
    hotArticle = []
    rs = requests.session()
    load = {
         'from': '/bbs/'+plate+'/index.html', #plate=看板
         'yes': 'yes'
            }
    res = rs.post('https://www.ptt.cc/ask/over18',verify=False, data=load) #用post方法通過驗證
    soup = BeautifulSoup(res.text,'html.parser') #用beautifulSoup解析HTML代碼存入變數'soup'中 parser是解析器 res.text是html程式碼
    '''print('\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\')
    print(res)
    print('||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\\')
    print(soup)'''
    allPageURL = soup.select('.btn.wide')[1]['href'] #取得新頁面上一頁的網址 例如: /bbs/joke/index6148.html
    startPage = getPageNumber(allPageURL) #讓函式把 /bbs/joke/index6148.html 變成6148+1 最新的一頁
    indexList=[] #將網址列串淨空
    for page in range(startPage, startPage-9,-1): # 把最新一頁往前8頁加入搜尋列表
        pageURL = 'https://www.ptt.cc/bbs/'+plate+'/index{}.html'.format(page) #爬取的網址
        indexList.append(pageURL) #放入網址串列
        content = '' #內容清空
        count= 0 #計算文章數
        
    while indexList:
        index = indexList.pop(0)
        res = rs.get(index, verify = False)
        if res.status_code != 200:  #如果網頁忙線中,則先將網頁放入indexList 並休息0.5秒後再連接
            indexList.append(index)
            #print(u'error_URL:',index)
            #time.sleep(0.5)
        else: #順利連接
            #print('\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\')
            #print(crawlHotActicle(res))
            hotArticle += crawlHotActicle(res)
            #print(u'OK_URL:', index)
            #time.sleep(0.06)
            
    hotArticle = sorted(hotArticle, key=sortHot,reverse = True)#將文章以推文數排列
    
    for article in hotArticle: #將文章依序列出
        if count == 15: #只列出前15筆
            return content #15筆就結束for
        data = '{}.{}\n人氣:{}\n{}\n\n'.format(count+1,article.get('title',None),article.get('hot', None),article.get('url_link', None))
        content += data
        count +=1
        
    return content

        
    
print(crawPtt('joke'))
    
    
