#####自動輸入欄位#####
import argparse
from bs4 import BeautifulSoup
import requests
import wget

url = "" #影片網址(input)
file_path = "" #: 下載後的影片要儲存的google drive位置(input)
thread_num = "" #多執行緒數量(input)
video_id = "" #:影片番號	
file_name = "" #: 影片儲存名稱
url_m3u8 = "" #: m3u8檔url
ts_id = "" #: 分割檔ID
partition_total_size = 0 #: 分割檔總數量
id_inits = "" #: 開頭檔ID 
url_inits = "" #: 開頭檔的url

def doParser(url):
	try:
		video_id = url.split('/')[-2]
		#透過beautiful soup進行網頁資訊爬蟲
		soup_jable = BeautifulSoup(requests.get(url).text, features="html.parser") #抓取整個html原始碼
		#抓.m3u8 url
		poster_selector = "section.pb-e-lg-30 link" #塞選器
		poster_src = [i.get("href") for i in soup_jable.select(poster_selector)][0]
		url_m3u8 = poster_src
		file_name = soup_jable.find("meta",  property="og:title")["content"]
		#url轉換
		ts_id = url_m3u8[:-5].split('/')[-1]
		print('[影片番號: '+ video_id +']')
		print('[影片名稱: '+ file_name +']')
		print('[m3u8檔url: '+ url_m3u8 +']')
		print('[分割檔ID:'+ ts_id +']')
		return video_id, file_name, url_m3u8, ts_id
	except Exception as e:
		print("網頁資訊擷取失敗!")
		print(e)
		
def doDownload(url_m3u8, ts_id): 
	try:
		try:
			#下載m3u8檔
			wget.download(url_m3u8)
			print('\nm3u8下載完成!')
		except Exception as e:
			print("m3u8下載失敗!")
			print(e)
		try:
			#從.m3u8抓取id_inits、partition_total_size
			m3u8_file_path = "/content/"+ ts_id +".m3u8"
			with open(m3u8_file_path, "r") as m3u8_file:
				#FileContent = m3u8_file.read()
				FileasList = m3u8_file.readlines()
				id_inits = FileasList[4].split('"')[1][:-3]
				partition_total_size = int(FileasList[-2][len(ts_id):-4])
				print('[分割檔總數:'+ str(partition_total_size) +']')
				print('[開頭檔ID:'+ id_inits +']')
		except IOError as e1:
			print(e1)
		except Exception as e:
			print(ts_id +".m3u8讀取失敗!")
			print(e)
		try:
			url_inits = url_m3u8[:-5].strip(url_m3u8[:-5].split('/')[-1]) + id_inits + '.ts'
			print('[開頭檔url:'+ url_inits +']')
			#下載開頭檔
			wget.download(url_inits)
			print('\n開頭檔下載完成!')
		except Exception as e:
			print("開頭檔下載失敗!")
			print(e)	
		return partition_total_size, id_inits, url_inits
	except :
		return

def Start(args_1):
	try:
		global url #影片網址(input)
		global video_id #:影片番號	
		global file_name #: 影片儲存名稱
		global url_m3u8 #: m3u8檔url
		global ts_id #: 分割檔ID
		global partition_total_size #: 分割檔總數量
		global id_inits #: 開頭檔ID 
		global url_inits #: 開頭檔的url
		#輸入要處理的影片網址
		url = args_1
		#擷取url資訊
		print("開始進行網址解析...")
		result = doParser(url)
		video_id = result[0]
		file_name = result[1]
		url_m3u8 = result[2]
		ts_id = result[3]
		#下m3u8&開頭檔
		result_2 = doDownload(url_m3u8, ts_id)
		partition_total_size = result_2[0]
		id_inits  = result_2[1]
		url_inits  = result_2[2]
	except :
		print("網址解析失敗!")
		
def MainArgs():
	try:
		global url #影片網址(input)
		global video_id #:影片番號	
		global file_name #: 影片儲存名稱
		global url_m3u8 #: m3u8檔url
		global ts_id #: 分割檔ID
		global partition_total_size #: 分割檔總數量
		global id_inits #: 開頭檔ID 
		global url_inits #: 開頭檔的url
		#參數
		parser = argparse.ArgumentParser()
		parser.add_argument("url", help="Write the url on here")
		args = parser.parse_args()
		#輸入要處理的影片網址
		url = args.url
		#擷取url資訊
		print("開始進行網址解析...")
		result = doParser(url)
		video_id = result[0]
		file_name = result[1]
		url_m3u8 = result[2]
		ts_id = result[3]
		#下m3u8&開頭檔
		result_2 = doDownload(url_m3u8, ts_id)
		partition_total_size = result_2[0]
		id_inits  = result_2[1]
		url_inits  = result_2[2]
	except Exception as e:
		print(e)
		print("網址解析失敗!")	
		
#MainArgs()




	
	