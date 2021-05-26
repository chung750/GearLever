#####自動輸入欄位#####
import argparse
from bs4 import BeautifulSoup
import requests
import urllib
from GearLever import gl_variable as gl
from GearLever import ts_download
'''
video_id = "" #:影片番號	
file_name = "" #: 影片儲存名稱
url_m3u8 = "" #: m3u8檔url
ts_id = "" #: 分割檔ID
partition_total_size = 0 #: 分割檔總數量
id_inits = "" #: 開頭檔ID 
url_ts = "" #: ts下載檔url 
url_inits = "" #: 開頭檔的url
'''

def doParser(url):
	try:
		
		#透過beautiful soup進行網頁資訊爬蟲
		soup_jable = BeautifulSoup(requests.get(url).text, features="html.parser") #抓取整個html原始碼
		#抓.m3u8 url
		poster_selector = "section.pb-e-lg-30 link" #塞選器
		poster_src = soup_jable.select(poster_selector)[1].text.split("'")[1]
		url_m3u8 = poster_src
		file_name = soup_jable.find("meta",  property="og:title")["content"]
		video_id = file_name.split(' ')[0]
		if (len(file_name) > 70) : file_name = file_name[:-(len(file_name)-70)] #避免檔名過長
		#url轉換
		ts_id = url_m3u8[:-5].split('/')[-1]
		print('[Info] 影片番號: '+ video_id )
		print('[Info] 影片名稱: '+ file_name)
		print('[Info] m3u8檔url: '+ url_m3u8)
		print('[Info] 分割檔ID:'+ ts_id)
		return video_id, file_name, url_m3u8, ts_id
	except Exception as e:
		print("[Error] 網頁資訊擷取失敗!")
		print(e)
		
def doDownload(url_m3u8, ts_id, download_path): 
	try:
		try:
			#下載m3u8檔
			urllib.request.urlretrieve(url_m3u8, download_path+ts_id+".m3u8")
			print('[Info] m3u8下載完成!')
		except Exception as e:
			print("[Error] m3u8下載失敗!")
			print(e)
		try:
			#從.m3u8抓取id_inits、partition_total_size
			m3u8_file_path = download_path+ ts_id +".m3u8"
			with open(m3u8_file_path, "r") as m3u8_file:
				#FileContent = m3u8_file.read()
				FileasList = m3u8_file.readlines()
				try:
					id_inits = FileasList[4].split('"')[1][:-3]
				except:
					id_inits = ''
				partition_total_size = int(FileasList[-2][len(ts_id):-4])+1
				print('[Info] 分割檔總數:'+ str(partition_total_size))
				print('[Info] 開頭檔ID:'+ id_inits)
		except IOError as e1:
			print(e1)
		except Exception as e:
			print("[Error] "+ts_id +".m3u8讀取失敗!")
			print(e)
		try:
			url_ts = url_m3u8[:-5].strip(url_m3u8[:-5].split('/')[-1])
			if id_inits:
				try:
					url_inits = url_ts + id_inits + '.ts'
					print('[Info] ts下載檔url:'+ url_ts )
					print('[Info] 開頭檔url:'+ url_inits)
					#下載開頭檔
					urllib.request.urlretrieve(url_inits, download_path+id_inits+".ts")
					print('[Info] 開頭檔下載完成!')
				except Exception as e:
					print(e)
					print("[Error] 開頭檔下載失敗!")
			else : url_inits = ''
		except Exception as e:
			print(e)		
		return partition_total_size, id_inits, url_ts, url_inits
	except :
		print("[Error] 檔案下載失敗!")

def start(url, thread_num, path, path_drive):
	try:
		gl._init()
		#輸入要處理的影片網址
		download_url = url
		download_path = path
		#擷取url資訊
		print("[Info] 開始進行網址解析...")
		result = doParser(download_url)
		gl.set_value('video_id', result[0])
		gl.set_value('file_name', result[1])
		gl.set_value('url_m3u8', result[2])
		gl.set_value('ts_id', result[3])

		#下載m3u8&開頭檔
		result_2 = doDownload(gl.get_value('url_m3u8'), gl.get_value('ts_id'), download_path)
		gl.set_value('partition_total_size', result_2[0])
		gl.set_value('id_inits', result_2[1])
		gl.set_value('url_ts', result_2[2])
		gl.set_value('url_inits', result_2[3])
	except :
		print("[Error] 網址解析失敗!")	
		return
	#開始分割檔的下載
	if ts_download.start(thread_num, path, path_drive):
		return True
	
		
def MainArgs():
	try:
		gl._init()
		#參數
		parser = argparse.ArgumentParser()
		parser.add_argument("url", help="Write the url on here")
		args = parser.parse_args()
		#輸入要處理的影片網址
		url = args.url
		#擷取url資訊
		print("[Info] 開始進行網址解析...")
		result = doParser(url)
		gl.set_value('video_id', result[0])
		gl.set_value('file_name', result[1])
		gl.set_value('url_m3u8', result[2])
		gl.set_value('ts_id', result[3])
		'''
		video_id = result[0]
		file_name = result[1]
		url_m3u8 = result[2]
		ts_id = result[3]
		'''
		#下m3u8&開頭檔
		result_2 = doDownload(gl.get_value('url_m3u8'), gl.get_value('ts_id'))
		gl.set_value('partition_total_size', result_2[0])
		gl.set_value('id_inits', result_2[1])
		gl.set_value('url_ts', result_2[2])
		gl.set_value('url_inits', result_2[3])
		'''
		partition_total_size = result_2[0]
		id_inits  = result_2[1]
		url_ts  = result_2[2]
		url_inits  = result_2[3]
		'''
	except Exception as e:
		print(e)
		print("[Error] 網址解析失敗!")	
if __name__ == '__main__':		
	MainArgs()




	
	