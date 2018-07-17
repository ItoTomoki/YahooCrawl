#import urllib2, urllib.error
import urllib2
from bs4 import BeautifulSoup
import os
import gzip

#html = urllib2.urlopen("https://textream.yahoo.co.jp/thread/1835700")
#soup = BeautifulSoup(html)

#soup.find_all("a")[50]
#soup.find_all("a", attrs={"data-sec": "trdlst"})[0]
#soup.find_all("a")[50].get("href")
#soup.find_all("a")[50].string
#soup.find_all("a")[50].find("span")

#soup.find_all("a", attrs={"data-sec":"topnav", "data-slk":"ne"})
#NextURL = "https://textream.yahoo.co.jp" + soup.find("a", attrs={"data-sec":"topnav", "data-slk":"ne"}).get("href")
#NextSoup = BeautifulSoup(urllib2.urlopen(NextURL))
#ThreadList = soup.find_all("a", attrs={"data-sec": "trdlst"})

sector_url = "https://textream.yahoo.co.jp/thread/1835700"
def save_sector(sector_url):
	soup = BeautifulSoup(urllib2.urlopen(sector_url))
	ThreadList = soup.find_all("a", attrs={"data-sec": "trdlst"})
	for thread in ThreadList:
		if thread.get("href") != None:
			URL_Thread = thread.get("href")
			write_thread_before(URL_Thread)
	#save_cur_ThreadList(ThreadList)
	if soup.find("a", attrs={"data-sec":"topnav", "data-slk":"ne"}) != None:
		NextURL = "https://textream.yahoo.co.jp" + soup.find("a", attrs={"data-sec":"topnav", "data-slk":"ne"}).get("href")
		save_sector(NextURL)
	else:
		return 0


#url = "https://textream.yahoo.co.jp/thread/1835631?sort=0&start=101"

#def save_cur_ThreadList(ThreadList):
	#for thread in ThreadList:
		#try:
			#URL_Thread = thread.get("href")
			#html_Thread = urllib2.urlopen(URL_Thread)
			#soup_Thread = BeautifulSoup(html_Thread)
			#list(set(soup_Thread.find_all("li", attrs={"class":"prev"})))[0].find("a").get("href")
			#soup_Thread.find("a", attrs={"data-ylk": "slk:bo20;pos:0"}).get("href")
			#if soup_Thread.find("a", attrs={"data-ylk": "slk:bo20;pos:0"}).get("href") != None:
				#OldestPageURL = soup_Thread.find("a", attrs={"data-ylk": "slk:bo20;pos:0"}).get("href")
				#save_page_and_output_nexturl(OldestPageURL)
		#except:
			#f = open("error_list.txt", "a")
			#f.write(thread.prettify().encode("utf-8"))
			#f.write("\n")
			#f.close()

def save_cur_Thread(URL_Thread):
	#try:
		#URL_Thread = thread.get("href")
		html_Thread = urllib2.urlopen(URL_Thread)
		soup_Thread = BeautifulSoup(html_Thread)
		if soup_Thread.find("a", attrs={"data-ylk": "slk:bo20;pos:0"}).get("href") != None:
			OldestPageURL = soup_Thread.find("a", attrs={"data-ylk": "slk:bo20;pos:0"}).get("href")
			save_page_and_output_nexturl(OldestPageURL)
	#except:
		#f = open("error_list_url.txt", "a")
		#f.write(URL_Thread.encode("utf-8"))
		#f.write("\n")
		#f.close()


def write_thread_before(URL_Thread):
	print URL_Thread
	try:
		html_Thread = urllib2.urlopen(URL_Thread)
		soup_Thread = BeautifulSoup(html_Thread)
		#if (("2018" in soup_Thread.find("li", {"class":"threadUpdated"}).prettify()) or 
				#("2017" in soup_Thread.find("li", {"class":"threadUpdated"}).prettify())):
		if soup_Thread.find("li", {"class":"threadUpdated"}) != None:
			if ("2018" in soup_Thread.find("li", {"class":"threadUpdated"}).prettify()):
				try:
					save_cur_Thread(URL_Thread)
					if soup_Thread.find("li", {"class": "threadBefore"}) != None:
						if soup_Thread.find("li", {"class": "threadBefore"}).find("a") != None:
							older_thred_url = soup_Thread.find("li", {"class": "threadBefore"}).find("a").get("href")
							if older_thred_url != None:
								#save_cur_Thread(older_thred_url)
								write_thread_before(older_thred_url)
							else:
								return 0
						else:
							return 0
					else:
						return 0
				except:
					f = open("error_list_url.txt", "a")
					f.write(URL_Thread.encode("utf-8"))
					f.write("\n")
					f.close()
					return 0
			else:
				print "not in 2018:" + URL_Thread
				return 0
		else:
			print "not threadUpdated:" + URL_Thread
	except:
		print "Error (Not open)"
		f = open("error_list_url.txt", "a")
		f.write(URL_Thread.encode("utf-8"))
		f.write("\n")
		f.close()
		



def save_page_and_output_nexturl(PageURL):
	if PageURL.split("/")[-3] not in os.listdir("."):
		os.mkdir(PageURL.split("/")[-3])
	if PageURL.split("/")[-2] not in os.listdir(PageURL.split("/")[-3]):
		os.mkdir(PageURL.split("/")[-3] + "/" + PageURL.split("/")[-2])
	f_name = (PageURL.split("/")[-3] + "/" + PageURL.split("/")[-2] + "/" + PageURL.split("/")[-1])
	soup_Thread = BeautifulSoup(urllib2.urlopen(PageURL))
	#soup_commentlist = soup_Thread.find("ul", {"class": "commentList"})
	f = gzip.open(f_name + ".txt.gz", "w")
	#f.write(soup_commentlist.prettify().encode("utf-8"))
	f.write(soup_Thread.prettify().encode("utf-8"))
	f.close()
	NextURL_box = soup_Thread.find("li", attrs={"class":"next"}).find("a")
	if NextURL_box == None:
		return 0
	else:
		return save_page_and_output_nexturl(soup_Thread.find("li", attrs={"class":"next"}).find("a").get("href"))

#next_url = save_page_and_output_nexturl(OldestPageURL)

#NextURL = soup.find_all("a", attrs={"data-sec":"topnav", "data-slk":"ne"})

category_url = "https://textream.yahoo.co.jp/category/1834773"
category_soup = BeautifulSoup(urllib2.urlopen(category_url))
category_list = category_soup.find_all("a", attrs={"class":"cf"})
#soup = BeautifulSoup(html)

#sector_url = "https://textream.yahoo.co.jp/thread/1835700"
sector_url = "https://textream.yahoo.co.jp/thread/1835105"
sector_name = sector_url.split("/")[-1]
if sector_name not in os.listdir("."):
	os.mkdir(sector_name)

os.chdir(sector_name)	
save_sector(sector_url)


#for category in category_list:
	#sector_url = category.get("href")
	#sector_name = sector_url.split("/")[-1]
	#if sector_name not in os.listdir("."):
		#os.mkdir(sector_name)
	#os.chdir(sector_name)
	#save_sector(sector_url)


