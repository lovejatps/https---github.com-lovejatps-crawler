#!/usr/bin/env python
#coding=utf-8

import urllib2 ,sys ,json,os
from bs4 import BeautifulSoup
from urlcontent import UrlContent

reload(sys)
sys.setdefaultencoding('utf-8')



#----建材商品主ＵＲＬ
SortUrl = 'http://mall.to8to.com/jiancai'
path = '/Users/huxiaoning/Downloads/tbt/'


# print '测试utf-8'


#-----所有建材商品分类－－－－
def getSort():
    page = UrlContent.getHtmlConnent(SortUrl)
    #page = urllib2.urlopen(SortUrl)
    adminsortlist = []
    if None != page:
        if page.getcode() ==200:
            soup = BeautifulSoup(page.read(),from_encoding="utf8")
            if None != soup:
                producers = soup.find_all("div", 'ps_bg_f7f7f7')
                for producer in producers:
                   adminSortmap = {}
                   if producer['name'] == 'jccCateContent':
                        sorts = producer.find("div","header_search_box")
                        adminSortName = sorts.h4.text
                        #print adminSortName
                        sortlist = sorts.find_all("a")
                        sortSet = []
                        for sort in sortlist:
                            sortmap = {}
                            sortmap['sortName'] = sort.text
                            sortmap['sortHref'] = sort['href']
                            sortSet.append(sortmap)
                        adminSortmap['adminSortName']= adminSortName
                        adminSortmap['sortSet']= sortSet
                        adminsortlist.append(adminSortmap)
                return adminsortlist

            else:
                print 'sortpage err!'
        else:
            print "The server returns :" +page.getcode()
    else:
        print "Sort err"
 


#获取每一类商品的页数            
def getpageNumber(pageConentd):
    try:
        pagedivs = pageConentd.find('div','global_wrap clear').find('div','wrapper_1180').find('div','list_container list_container1 mt10').find('div','pages_box mt20')
        pageNumber = pagedivs.em.b.text
        return pageNumber
    except Exception, e:
        print e
        return None

#下载图片    
def downloadImg(goodsUrl,goodsPath):
    goodsPage =  UrlContent.getHtmlConnent(goodsUrl)
    if goodsPage.getcode() == 200:
        soup = BeautifulSoup(goodsPage.read(),from_encoding="utf8")
        goodsImgUrl = soup.find('ul','carousel_diagram clear').find('a','focus').find('img')['bsrc']
        formatsrc = goodsImgUrl.split('.')
        if len(formatsrc)>0:
            format = formatsrc[len(formatsrc)-1]
            print format
            dir = goodsPath +'indexImg'+'.'+ format
            if os.path.exists(dir):
                 print '文件已经存在'
            else:
                outf =None
                img = UrlContent.getVoidConnent(goodsImgUrl, SortUrl)  #需要优化SortUrl
                try:
                    outf = open(dir,'wb')
                    outf.write(img.read())    
                    outf.flush()
                except Exception,e:
                     print e
                     print 'file err!'
                finally:
                    if None != outf:
                        outf.close()
        goodsExplainImgUrlDiv = soup.find('div','sec2_tab_detail')
        explainImglist = goodsExplainImgUrlDiv.input['value']
        imglist = explainImglist.split('>')
        i = 1
        for imgs in imglist:
            imgUrlStrs = imgs.split(' ',2)    
            if len(imgUrlStrs) >= 1:
                imgurls  =  imgUrlStrs[1:2]
                if len(imgurls) >0 :
                    imgurl = imgurls[0].split('"')
                    print imgurl
                    if len(imgurl) >= 1:
                        urlim = imgurl[1:2][0]
                        imgformats = urlim.split('.')
                        imgoutf =None
                        imgdir =''
                        imgformat=''
                        if len(imgformats) >0:
                            imgformat = imgformats[len(imgformats)-1]
                            try:
                                imgdir = goodsPath +str(i)+'.'+ imgformat
                                if os.path.exists(imgdir):
                                    print '文件已经存在'
                                else:
                                    esimg = UrlContent.getVoidConnent(urlim, SortUrl)  #需要优化SortUrl
                                    imgoutf = open(imgdir,'wb')
                                    imgoutf.write(esimg.read())    
                                    imgoutf.flush()
                                    imgoutf.close()
                                i = i + 1
                            except Exception ,e :
                                print e
                            finally:
                                if None != imgoutf:
                                    imgoutf.close()
                        


#获取每一页中的所有商品
def dealfileUrl(fileUrl,filePath):
    page = UrlContent.getHtmlConnent(fileUrl)
    if page.getcode() == 200:
        soup = BeautifulSoup(page.read(),from_encoding="utf8")
        pagedivs = soup.find('div','global_wrap clear').find('div','wrapper_1180').find('div','list_container list_container1 mt10').ul
        goodsli = pagedivs.find_all('li')
        for goods in goodsli:
            goodsUrl = goods.find('p','cur_msg').a['href']
            goodsName = goods.find('p','cur_msg').a.text.replace('/','_').replace(' ','')
            print filePath , goodsName
            goodsPath = filePath + goodsName + '/'
            if not os.path.exists(goodsPath):
                os.mkdir(goodsPath)
            downloadImg(goodsUrl,goodsPath)  ######下载图片
            
            


def  savefile(filelistUrl,filePath):
    print filelistUrl
    page = UrlContent.getHtmlConnent(filelistUrl)
    if page.getcode() == 200:
        soup = BeautifulSoup(page.read(),from_encoding="utf8")
        if None != soup:
            pageNumber = getpageNumber(soup)
            if None != pageNumber:
                number = int(pageNumber)
                for i in range(number):
                    fileUrl = filelistUrl +'&p='+str(i+1)
                    dealfileUrl(fileUrl,filePath)
    
    pass       
#总入口 
def getSortgoods():
    adminSortlist = getSort()
    for sort in adminSortlist:
        sortpath =''
        print sort.get('adminSortName')
        sortpath = path + sort.get('adminSortName')+'/'
        if not os.path.exists(sortpath):
            os.mkdir(sortpath)
        for sun_sort in sort.get('sortSet'):
            filepath= ''
            print sun_sort.get('sortName')
            sortName = sun_sort.get('sortName')
            name = sortName.replace('/','_')
            filepath =  sortpath + name +'/'
            if not os.path.exists(filepath):
                os.mkdir(filepath)
                #pass
            print sun_sort.get('sortHref')
            savefile(sun_sort.get('sortHref'),filepath)
 
 
 
getSortgoods()            
            
#downloadImg('http://mall.to8to.com/temai/16240.html?p=0.1','/Users/huxiaoning/Downloads/tbt/灯具灯饰/吸顶灯/奥朵奥朵水晶无极调光温馨浪漫田园led客厅餐厅主卧室吸顶灯具CL30250/')
#http://mall.to8to.com/temai/16240.html?p=0.1
#dealfileUrl('http://mall.to8to.com/search?c=50019940&p=1','/Users/huxiaoning/Downloads/tbt/灯具灯饰/吸顶灯/')        
#savefile("",'http://mall.to8to.com/search?c=50019940')
#getSortgoods()

