#####Jable元數據獲取#####
#建立資料夾
from bs4 import BeautifulSoup
from PIL import Image
import argparse
import os
import requests
import shutil

def NfoProcedure(file_name, video_id):
	try: 
		#透過beautiful soup進行網頁資訊爬蟲
		javbus_url = 'https://www.javbus.com/'+ video_id
		jable_url = 'https://jable.tv/videos/'+ video_id+'/'
		soup_javbus = BeautifulSoup(requests.get(javbus_url).text,features="html.parser") #抓取整個html原始碼
		soup_jable = BeautifulSoup(requests.get(jable_url).text,features="html.parser") #抓取整個html原始碼
		try:
			info_selector = "div.container div.info p" #塞選器
			dict_info = {} #影片資訊
			list_string = []
			for i in soup_javbus.select(info_selector):
				t = i.get_text().replace('\n','').replace(' ','').split(':')
				for j in t:
					list_string.append(j)
					if len(t) == 1: list_string.append('')
			for i in range(len(list_string)): 
				if( i%2 == 0): dict_info[list_string[i]] = list_string[i+1]
			#nfo各個標籤
			try:
				nfo_title = soup_javbus.title.string
			except:
				print('[Error] cannot get: nfo_title')
				nfo_title = ''
			try:	
				nfo_studio = dict_info['製作商']
			except:
				print('[Error] cannot get: nfo_studio')
				nfo_studio = ''
			try:
				nfo_year = dict_info['發行日期'].strip()[0:4]  
			except:
				print('[Error] cannot get: nfo_year')
				nfo_year = ''
			try:
				nfo_outline = soup_jable.find("meta", property="og:title")["content"]
			except:
				print('[Error] cannot get: nfo_outline')
				nfo_outline = ''
			try:
				nfo_plot = nfo_outline
			except:
				print('[Error] cannot get: nfo_plot')
				nfo_plot = ''
			try:
				nfo_runtime = dict_info['長度']
			except:
				print('[Error] cannot get: nfo_runtime')
				nfo_runtime = ''
			try:
				nfo_director = dict_info['發行商'] 
			except:
				print('[Error] cannot get: nfo_director')
				nfo_director = ''
			try:
				nfo_poster = video_id + '-poster.jpg'
			except:
				print('[Error] cannot get: nfo_poster')
				nfo_poster = ''
			try:
				nfo_thumb = video_id + '-thumb.jpg'
			except:
				print('[Error] cannot get: nfo_thumb')
				nfo_thumb = ''
			try:
				nfo_fanart = video_id + '-fanart.jpg'
			except:
				print('[Error] cannot get: nfo_fanart')
				nfo_fanart = ''
			try:
				nfo_name = [k.string for k in soup_javbus.select("div.container div.info div.star-name")]
				if (len(nfo_name) == 0): nfo_name = ['素人']
			except:
				print('[Error] cannot get: nfo_name')
				nfo_name = ''
			try:
				nfo_maker = nfo_studio  
			except:
				print('[Error] cannot get: nfo_maker')
				nfo_maker = ''
			try:
				nfo_tag = [j.replace(' ','') for j in list(filter(None,[g.string for g in soup_javbus.select("div.container div.info span.genre")]))] + [h.string.replace(' ','') for h in soup_jable.select("h5.tags a")]
			except:
				print('[Error] cannot get: nfo_tag')
				nfo_tag = ''
			try:
				nfo_genre = nfo_tag 
			except:
				print('[Error] cannot get: nfo_genre')
				nfo_genre = ''
			try:
				nfo_num = dict_info['識別碼']
			except:
				print('[Error] cannot get: nfo_num')
				nfo_num = ''
			try:
				nfo_release = dict_info['發行日期']
			except:
				print('[Error] cannot get: nfo_release')
				nfo_release = ''
			try:
				nfo_premiered = nfo_release
			except:
				print('[Error] cannot get: nfo_premiered')
				nfo_premiered = ''
			try:
				nfo_cover = soup_javbus.select("div.container div.screencap a")[0].get("href")
			except:
				print('[Error] cannot get: nfo_cover')
				nfo_cover = ''
			try:
				nfo_website = javbus_url
			except:
				print('[Error] cannot get: nfo_website')
				nfo_website = ''
			#整合字串
			text_up = '<?xml version="1.0" encoding="UTF-8" ?>\n<movie>\n <title>'+nfo_title+'</title>\n  <set>\n  </set>\n  <studio>'+nfo_studio+'</studio>\n  <year>'+nfo_year+'</year>\n  <outline>'+nfo_outline+'</outline>\n  <plot>'+nfo_plot+'</plot>\n  <runtime>'+nfo_runtime+'</runtime>\n  <director>'+nfo_director+'</director>\n  <poster>'+nfo_poster+'</poster>\n  <thumb>'+nfo_thumb+'/thumb>\n  <fanart>'+nfo_fanart+'</fanart>'
			text_middle = "  <maker>"+nfo_maker+"</maker>\n  <label>\n  </label>"
			text_down = "  <num>"+nfo_num+"</num>\n  <release>"+nfo_release+"</release>\n  <premiered>"+nfo_premiered+"</premiered>\n  <cover>"+nfo_cover+"</cover>\n  <website>"+nfo_website+"</website>\n</movie>"
			#寫入.nfo & images
			WriteNfo(file_name, video_id, text_up, text_middle, text_down, nfo_name, nfo_tag, nfo_genre)
			ImageDownload(file_name, video_id,  nfo_cover, soup_jable.find("meta", property="og:image")["content"])
		except 	Exception as e2:	
			print(e2)
			print("[Error] 字串擷取失敗!")
	except : 
		print("[Error] 網頁資訊擷取失敗!")
		
##寫入.nfo
def WriteNfo(file_name, video_id, text_up, text_middle, text_down, nfo_name, nfo_tag, nfo_genre):
	try:
		with open("/content/"+file_name+"/"+video_id+".nfo", "wt", encoding='UTF-8') as code:
			print(text_up, file=code)
			print("  <actor>", file=code)
			if type(nfo_name) == list:
				for nfo_name_fetch in nfo_name:
					print("   </name>"+nfo_name_fetch+"</name>", file=code)
			else: print("   <name>"+nfo_name+"</name>", file=code)
			print("  </actor>", file=code)
			print(text_middle, file=code)
			for nfo_tag_fetch in nfo_tag:
			  print("  <tag>"+nfo_tag_fetch+"</tag>", file=code)
			for nfo_genre_fetch in nfo_genre:
			  print("  <genre>"+nfo_genre_fetch+"</genre>", file=code)
			print(text_down, file=code)
		print("[Info] "+video_id+".nfo 儲存完成!")
		#print(open("/content/"+file_name+"/"+video_id+".nfo",mode="r").read())		
	except Exception as e:
		print("[Error] "+video_id+".nfo 寫入失敗!")
		print(e)
	except IOError as e1:
		print("[Error] "+video_id+".nfo 寫入失敗!")
		print(e1) 

##存入圖片
def ImageDownload(file_name, video_id,  url_1, url_2):
	try:
		cover = requests.get(url_1).content
	except Exception:
		print('[Warning] JavBus找不到圖片，改以Jable尋找..')
		try:
			cover = requests.get(url_2).content
		except Exception: 
			print('[Error] 圖片下載失敗!')
	try: #儲存下載的圖片
		with open("/content/"+file_name+"/"+video_id+"-fanart.jpg", "wb") as code:
			code.write(cover)
		print("[Info] "+video_id+"-fanart.jpg 儲存完成!")	 	
		shutil.copyfile("/content/"+file_name+"/"+video_id+"-fanart.jpg", "/content/"+file_name+"/"+video_id+"-thumb.jpg")
		#os.copy("cp '/content/"+file_name+"/"+video_id+"-fanart.jpg' '/content/"+file_name+"/"+video_id+"-thumb.jpg'")
		print("[Info] "+video_id+"-thumb.jpg 儲存完成!")	
		try: #圖片切割
			img = Image.open("/content/"+file_name+"/"+video_id+"-fanart.jpg")
			#img.save("/content/"+file_name+"/"+video_id+"-thumb.jpg")
			img2 = img.crop((421, 0, 800, 538))
			img2.save("/content/"+file_name+"/"+video_id+"-poster.jpg")
			print("[Info] "+video_id+"-poster.jpg 儲存完成!")
		except Exception as e2:
			print(e2)
			print('[Error] 圖片切割失敗!') 
	except Exception as e1:
		print('[Error] 圖片儲存失敗!')
		print(e1) 

##建立資料夾  
def CreatFolder(folder):
	if not os.path.exists(folder):  # 新建failed文件夹
		try:
			os.makedirs(folder)
			print("[Info] 資料夾建立: "+folder)
		except:
			print("[Error] failed! can not be make folder")
	return   
  
#main
def MainArgs():
	try:
		print("[Info] 開始進行元數據擷取...")
		parser = argparse.ArgumentParser()
		parser.add_argument("file_name", help="Write the file name on here")
		parser.add_argument("video_id", help="Write the video id on here")
		args = parser.parse_args()
		file_name = args.file_name
		video_id = args.video_id	
		#建立資料夾
		path = "/content/" + file_name 
		CreatFolder(path)
		#nfo
		NfoProcedure(file_name, video_id)
	except Exception as e:
		print(e)
		print("[Error] 元數據擷取失敗!")

#main 2
def start(args_1, args_2):
	try:
		print("[Info] 開始進行元數據擷取...")
		file_name = args_1
		if (len(file_name) > 70) : file_name = file_name[:-(len(file_name)-70)] #避免檔名過長
		video_id = args_2	
		#建立資料夾
		path = "/content/" + file_name +"/"
		CreatFolder(path)
		#nfo
		NfoProcedure(file_name, video_id)
		return path
	except Exception as e:
		print(e)
		print("[Error] 元數據擷取失敗!")		
		
if __name__ == '__main__':		
	MainArgs()
