import shlex
import subprocess
import math
import os
import time

#傳換byte顯示
def convert_size(size_bytes):
	if size_bytes == 0:
		return "0B"
	size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
	i = int(math.floor(math.log(size_bytes, 1024)))
	p = math.pow(1024, i)
	s = round(size_bytes / p, 2)
	return "%s %s" % (s, size_name[i])
 
#檢查是否轉存成功
def search_drive(file_name, video_id, file_path):
	drive_dir = os.listdir(file_path)
	check = [False, False, False, False, False ]
	#確認是否存在資料夾
	file_name = [i for i in drive_dir if video_id.upper() in i][0]
	if file_name:
		subdir_path = file_path+file_name
		drive_subdir = os.listdir(subdir_path)
		subdir_video_name = file_name+'.mp4'
		subdir_fanart_name = video_id+'-fanart.jpg'
		subdir_thumb_name = video_id+'-thumb.jpg'
		subdir_poster_name = video_id+'-poster.jpg'
		subdir_nfo_name = video_id+'.nfo'
		#確認各檔案
		if subdir_video_name in drive_subdir:
			size = os.stat(subdir_path+'/'+subdir_video_name).st_size
			print("[Info] "+subdir_video_name+' > '+convert_size(size))
			check[0] = True
		else: print(subdir_video_name+' 轉存失敗!')
		if subdir_fanart_name in drive_subdir:
			size = os.stat(subdir_path+'/'+subdir_fanart_name).st_size
			print("[Info] "+subdir_fanart_name+' > '+convert_size(size))
			check[1] = True
		else: print(subdir_fanart_name+' 轉存失敗!')
		if subdir_thumb_name in drive_subdir:
			size = os.stat(subdir_path+'/'+subdir_thumb_name).st_size
			print("[Info] "+subdir_thumb_name+' > '+convert_size(size))
			check[2] = True
		else: print(subdir_thumb_name+' 轉存失敗!')
		if subdir_poster_name in drive_subdir:
			size = os.stat(subdir_path+'/'+subdir_poster_name).st_size
			print("[Info] "+subdir_poster_name+' > '+convert_size(size))
			check[3] = True
		else: print(subdir_poster_name+' 轉存失敗!')
		if subdir_nfo_name in drive_subdir:
			size = os.stat(subdir_path+'/'+subdir_nfo_name).st_size
			print("[Info] "+subdir_nfo_name+' > '+convert_size(size))
			check[4] = True
		else: print("[Info] "+subdir_nfo_name+' 轉存失敗!')
		if False in check: return False
		else:  return True
	else:
		print('[Error] 資料夾轉存失敗!')
		return False
	

#拷貝資料夾到GD
def start(file_name, video_id, path):
	try:
		print("[Info] 轉存到雲端資料夾...")
		command = "cp -r '/content/"+ file_name +"' "+ path 
		process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		for line in process.stdout.readlines():
			print(line)
		if search_drive(file_name, video_id, path): 
			return True
		else : 
			return False
	except Exception as e :
		print(e)
		print("[Error] 轉存雲端資料夾失敗!")
		return False