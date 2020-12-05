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
			#nfo各個標籤
			nfo_title = soup_javbus.title.string
			nfo_studio = soup_javbus.select(info_selector)[4].contents[2].string
			nfo_year = soup_javbus.select(info_selector)[1].contents[1].strip()[0:4]  
			nfo_outline = soup_jable.find("meta", property="og:title")["content"]
			nfo_plot = nfo_outline
			nfo_runtime = soup_javbus.select(info_selector)[2].contents[1]
			nfo_director = soup_javbus.select(info_selector)[5].contents[2].string 
			nfo_poster = video_id + '-poster.jpg'
			nfo_thumb = video_id + '-thumb.jpg'
			nfo_fanart = video_id + '-fanart.jpg'
			nfo_name = [k.string for k in soup_javbus.select("div.container div.info div.star-name")]
			nfo_maker = nfo_studio  
			nfo_tag = [j.replace(' ','') for j in list(filter(None,[g.string for g in soup_javbus.select("div.container div.info span.genre")]))] + [h.string.replace(' ','') for h in soup_jable.select("h5.tags a")]
			nfo_genre = nfo_tag 
			nfo_num = soup_javbus.select(info_selector)[0].contents[2].string
			nfo_release = soup_javbus.select(info_selector)[1].contents[1].strip()
			nfo_premiered = nfo_release
			nfo_cover = soup_javbus.select("div.container div.screencap a")[0].get("href")
			nfo_website = javbus_url
			#整合字串
			text_up = '<?xml version="1.0" encoding="UTF-8" ?>\n<movie>\n <title>'+nfo_title+'</title>\n  <set>\n  </set>\n  <studio>'+nfo_studio+'</studio>\n  <year>'+nfo_year+'</year>\n  <outline>'+nfo_outline+'</outline>\n  <plot>'+nfo_plot+'</plot>\n  <runtime>'+nfo_runtime+'</runtime>\n  <director>'+nfo_director+'</director>\n  <poster>'+nfo_poster+'</poster>\n  <thumb>'+nfo_thumb+'/thumb>\n  <fanart>'+nfo_fanart+'</fanart>'
			text_middle = "  <maker>"+nfo_maker+"</maker>\n  <label>\n  </label>"
			text_down = "  <num>"+nfo_num+"</num>\n  <release>"+nfo_release+"</release>\n  <premiered>"+nfo_premiered+"</premiered>\n  <cover>"+nfo_cover+"</cover>\n  <website>"+nfo_website+"</website>\n</movie>"
			#寫入.nfo & images
			WriteNfo(file_name, video_id, text_up, text_middle, text_down, nfo_name, nfo_tag, nfo_genre)
			ImageDownload(file_name, video_id,  nfo_cover, soup_jable.find("meta", property="og:image")["content"])
		except 	Exception as e2:	
			print(e2)
			print("字串擷取失敗!")
	except : 
		print("網頁資訊擷取失敗!")
		
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
		print(video_id+".nfo 儲存完成!")
		#print(open("/content/"+file_name+"/"+video_id+".nfo",mode="r").read())		
	except Exception as e:
		print(video_id+".nfo 寫入失敗!")
		print(e)
	except IOError as e1:
		print(video_id+".nfo 寫入失敗!")
		print(e1) 

##存入圖片
def ImageDownload(file_name, video_id,  url_1, url_2):
	try:
		cover = requests.get(url_1).content
	except Exception:
		print('JavBus找不到圖片，改以Jable尋找..')
		try:
			cover = requests.get(url_2).content
		except Exception: 
			print('圖片下載失敗!')
	try: #儲存下載的圖片
		with open("/content/"+file_name+"/"+video_id+"-fanart.jpg", "wb") as code:
			code.write(cover)
		print(video_id+"-fanart.jpg 儲存完成!")	 	
		shutil.copyfile("/content/"+file_name+"/"+video_id+"-fanart.jpg", "/content/"+file_name+"/"+video_id+"-thumb.jpg")
		#os.copy("cp '/content/"+file_name+"/"+video_id+"-fanart.jpg' '/content/"+file_name+"/"+video_id+"-thumb.jpg'")
		print(video_id+"-thumb.jpg 儲存完成!")	
		try: #圖片切割
			img = Image.open("/content/"+file_name+"/"+video_id+"-fanart.jpg")
			#img.save("/content/"+file_name+"/"+video_id+"-thumb.jpg")
			img2 = img.crop((421, 0, 800, 538))
			img2.save("/content/"+file_name+"/"+video_id+"-poster.jpg")
			print(video_id+"-poster.jpg 儲存完成!")
		except Exception as e2:
			print(e2)
			print('圖片切割失敗!') 
	except Exception as e1:
		print('圖片儲存失敗!')
		print(e1) 

##建立資料夾  
def CreatFolder(folder):
	if not os.path.exists(folder):  # 新建failed文件夹
		try:
			os.makedirs(folder)
			print("資料夾建立:"+folder)
		except:
			print("[-]failed!can not be make folder\n")
	return   
  
#main
def main():
	try:
		print("開始進行元數據擷取...")
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
		print("元數據擷取失敗!")

main()
