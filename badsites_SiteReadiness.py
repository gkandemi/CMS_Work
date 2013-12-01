import os, sys, errno
import urllib2
import simplejson
from datetime import datetime
from datetime import timedelta
import time
from pprint import pprint
import string

#T1+T2
url = "http://dashb-ssb.cern.ch/dashboard/request.py/getsitereadinessrankdata?columnid=45&time=%s"
#only T2
#url = "http://dashb-ssb.cern.ch/dashboard/request.py/getsitereadinessrankdata?columnid=45&time=%s&sites=T2"
percentageThreshold = 0.6 #sitereadiness %60 dan kucuk olanlari getiriyordu waiting room a bu oran bunu sagliyor..


def getData(url, headers=None):  #tum site'lari cekip onlari dizi olarak dondurme islemini yapan fonksiyon...
    request = urllib2.Request(url, headers = headers)
    response = urllib2.urlopen(request)
    data = response.read()
    rows = simplejson.loads(data)
    return rows

def extractSitesUnderPercentage(dataRows, percentageThreshold):   #kotu site'lari ayirma fonksiyonu..
    sites = []
    for row in dataRows['data']:
	siteName = row[0].split(' ')[0]
	sitePercentage = float(row[1][0][1])
	if sitePercentage < percentageThreshold:  #kotu site'larin ayrilmasi icin gerekli olan kosul..
	    sites.append(siteName)
    return sites  # %60 dan kucuk olan site'larin tutuldugu degisken...

def main_function(outputfile_txt):
  oneWeekDataRows = getData(url % '48', headers={"Accept":"application/json"}) #168 7*24 ile elde ediliyor bu sekilde son haftanin verileri cekilebiliyor.. 
  threeMonthsDataRows = getData(url % '72', headers={"Accept":"application/json"}) # 2184 91*24 ile elde ediliyor bu da son 3 ayin verilerini getiriyor.. 

  oneWeekBadSites = extractSitesUnderPercentage(oneWeekDataRows, percentageThreshold)  #Son Haftalik kotu site'larin cekilmesi ve degiskene aktarilmasiii... 
  threeMonthsBadSites = extractSitesUnderPercentage(threeMonthsDataRows, percentageThreshold) # son 3 aylik kotu site'larin cekilmesi ve degiskene aktarilmasi..

  #all sites
  allSites = extractSitesUnderPercentage(threeMonthsDataRows, 10)  #Son 3 aylik tum site'lari cekmek icin tekrardan fonksiyonu cagiriyoruz.. bunun icin 10 yapip %100 olarak hepsini aliriz.. 
  print allSites 
    
  badSites = [val for val in oneWeekBadSites if val in threeMonthsBadSites]  #son haftada bad site lari son 3 ay da var mi diye kontrol edip badSites degiskenine aktarma.. 
  print badSites

  #write to file for SSB
  f1=open('./'+outputfile_txt, 'w+')
  now_write=(datetime.utcnow()).strftime("%Y-%m-%d %H:%M:%S")

  f1.write('# This txt goes into SSB and marks sites red when the following condition is true:\n')
  f1.write('# badSites = [val for val in oneWeekBadSites if val in threeMonthsBadSites]\n')
  f1.write('# with: site readiness percentage is < 60 % for both the last week as in the last 3 months\n')

  print "Local current time :", now_write
  for k in badSites:
    print k, 'red', 'red', url
    f1.write(now_write+' '+k+' red red '+url+'\n')
  for k in allSites: 
    if not k in badSites:
      print k, 'green', 'green', url 
      f1.write(now_write+' '+k+' green green '+url+'\n')

#ana programin basladigi bolum..
if __name__ == '__main__':
  outputfile_txt=sys.argv[1] #disaridan ciktinin verilecegi dosya parametre olarak aktarilir programa.. bunu gormek icin run_BadSites_SiteReadiness.sh scriptine bakabiliriz..
  main_function(outputfile_txt) #islemlere gidelim..
