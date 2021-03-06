from GearLever import gl_variable as gl
from GearLever import search_files
from GearLever import suppress_video
from GearLever import nfo_fetcher as nf
from GearLever import clone_drive
import urllib
import threading
import sys
import time

#參數
system_threads_num = 0  #紀錄系統本身的執行緒數量
url_ts = '' #下載網址
ts_id = ''   #下載分割檔ID
partition_total_size = ''  #總分割檔個數
threads = [] #多執行續
thread_switch = True  #執行續總開關
downloaded_num = 0  #紀錄目前完成下載的分割檔數量
downloaded_num_record_list = []   #記錄每5秒的下載檔案數
qos_waiting_time = 2  #流量控制的預設等待時間
current_partition = 0   #紀錄目前下載第幾分割檔
download_path = '' #分割檔下載路徑
#初始化參數
def initializeParameter():
	try:
		global system_threads_num
		global url_ts
		global ts_id
		global partition_total_size
		global threads
		global thread_switch
		global downloaded_num
		global downloaded_num_record_list
		global current_partition
		system_threads_num = threading.active_count() 
		url_ts = gl.get_value('url_ts') 
		ts_id = gl.get_value('ts_id') 
		partition_total_size = gl.get_value('partition_total_size') 
		threads.clear()
		thread_switch = True 
		downloaded_num = 0 
		downloaded_num_record_list.clear() 
		current_partition = 0 
	except Exception as e:
		print(e)
		print("[Error] 初始化參數失敗!")
	
#主要下載job
def doDownloadTs(list):
	try:
		global thread_switch
		#判斷多執行緒開關是否開啟
		if thread_switch == True:
			global current_partition
			global downloaded_num
			#判斷欲下載的分割檔ID是否超過最後一個
			if(current_partition <= partition_total_size-1):
				download_partition = current_partition
				current_partition = current_partition + 1 
				time.sleep(qos_waiting_time) #此暫停時間用於流量控管
				url_go = url_ts+ts_id+str(download_partition)+'.ts'
				urllib.request.urlretrieve(url_go, download_path+ts_id+str(download_partition)+'.ts')
				downloaded_num = downloaded_num+1
				nowtime = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()+28800)))
				print(">>>>> ["+nowtime+"] 下載進度: "+str(downloaded_num)+"/"+str(partition_total_size)+" (多執行緒總數:"+str(threading.active_count()-system_threads_num)+")")
				doDownloadTs(list) #下載完畢後執行下一個下載
			else:
				thread_switch = False
				print("[Info] 終止執行緒:"+threading.currentThread().name)
		else:
			print("[Info] 終止執行緒:"+threading.currentThread().name)
	except Exception as e:
		print(e)
		print("[Error] 下載分割檔"+str(download_partition)+"出現錯誤!")

#補下載job
def doReDownloadTs(miss_list):
	try:
		global thread_switch
		#判斷多執行緒開關是否開啟
		if thread_switch == True:
			global current_partition
			global downloaded_num
			#判斷欲下載的分割檔ID是否超過最後一個
			if current_partition <= len(miss_list)-1 :
				download_partition = miss_list[current_partition]
				current_partition = current_partition + 1 
				time.sleep(qos_waiting_time) #此暫停時間用於流量控管
				url_go = url_ts+ts_id+str(download_partition)+'.ts'
				urllib.request.urlretrieve(url_go, download_path+ts_id+str(download_partition)+'.ts')
				downloaded_num = downloaded_num+1
				nowtime = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()+28800)))
				print(">>>>> ["+nowtime+"] 補下載進度: "+str(downloaded_num)+"/"+str(len(miss_list))+" (多執行緒總數:"+str(threading.active_count()-system_threads_num)+")")
				doReDownloadTs(miss_list) #下載完畢後執行下一個下載
			else:
				thread_switch = False
				print("[Info] 終止執行緒:"+threading.currentThread().name)
		else:
			print("[Info] 終止執行緒:"+threading.currentThread().name)
	except Exception as e:
		print(e)
		print("[Error] 補下載分割檔"+str(download_partition)+"出現錯誤!")

#建立並執行多執行緒 
def startThreading(num, threads, func, miss_list):
	try:
		threads.clear()
		for i in range(num):
			threads.append(threading.Thread(target = func, args=[miss_list]))
			threads[i].start()
		print("[Info] 啟動多執行緒...")
	except Exception as e:
		print(e)
		print("[Error] 建立多執行緒失敗!")
#多執行管理
def ThreadingController(threads, target_rate, duration, func, miss_list):
	global thread_switch
	last_downloaded_num = 0
	try:
		while thread_switch:
			##維護多執行緒
			try:
				for i in range(len(threads)):
					if not threads[i].is_alive():
						threads[i] = threading.Thread(target = func, args=[miss_list])
						threads[i].start()
			except Exception as e:
				print(e)
				print("[Error] 維護多執行緒失敗!")
			##流量控管(目標維持每次控管階段時間內的平均下載數量為8)
			try:
				#每次控管階段紀錄一次下載檔案數
				if not downloaded_num_record_list: 
					downloaded_num_record_list.append(downloaded_num)
				else: 
					downloaded_num_record_list.append(downloaded_num - last_downloaded_num)
				last_downloaded_num = downloaded_num
			except Exception as e:
				print(e)
				print("[Error] 紀錄下載進度失敗!")
			try:
				if (len(downloaded_num_record_list)%5 == 0): #每5次控管階段QOS一次
					global qos_waiting_time
					download_rate = round(sum(downloaded_num_record_list[-5:])/(5*duration), 2) #計算最近的25秒的平均每秒下載數量
					#平均下載速率 < target_rate*0.5
					if (download_rate < target_rate*0.5): 
						qos_waiting_time = qos_waiting_time - 2
					#target_rate*0.5 <= 平均下載速率低於 < target_rate*0.625
					elif (download_rate >= target_rate*0.5 and download_rate < target_rate*0.625):
						qos_waiting_time = qos_waiting_time - 1.5
					#target_rate*0.625 <= 平均下載速率低於 < target_rate*0.75
					elif (download_rate >= target_rate*0.625 and download_rate < target_rate*0.75):
						qos_waiting_time = qos_waiting_time - 1
					#target_rate*0.75 <= 平均下載速率低於 < target_rate*0.875
					elif (download_rate >= target_rate*0.75 and download_rate < target_rate*0.875):
						qos_waiting_time = qos_waiting_time - 0.5
					#target_rate*1.125 <= 平均下載速率低於 < target_rate*1.25
					elif (download_rate >= target_rate*1.125 and download_rate < target_rate*1.25):
						qos_waiting_time = qos_waiting_time + 0.5
					#target_rate*1.25 <= 平均下載速率低於 < target_rate*1.375
					elif (download_rate >= target_rate*1.25 and download_rate < target_rate*1.375):
						qos_waiting_time = qos_waiting_time + 1
					#target_rate*1.375 <= 平均下載速率低於 < target_rate*1.5
					elif (download_rate >= target_rate*1.375 and download_rate < target_rate*1.5):
						qos_waiting_time = qos_waiting_time + 1.5
					#target_rate*1.5 <= 平均下載速率
					elif (download_rate >= target_rate*1.5):
						qos_waiting_time = qos_waiting_time + 2
					#qos_waiting_time值域: 0~6
					if qos_waiting_time < 0: qos_waiting_time = 0
					if qos_waiting_time > 6: qos_waiting_time = 6
					print("[Info] 流量控管: 目前平均下載速度("+str(download_rate)+"/s) 延遲時間("+str(qos_waiting_time)+"s) 預估剩餘時間("+str(time.strftime('%H時%M分%S秒', time.localtime(round((partition_total_size-downloaded_num)/download_rate, 0))))+")")
			except Exception as e:
				print(e)
				print("[Error] 流量管制失敗!")
			time.sleep(duration)
	except KeyboardInterrupt as k:
		print(k)
		thread_switch = False
		pass
#堵塞多執行緒
def joinThreading(num, threads):
	global thread_switch	
	for i in range(num):
		threads[i].join()
	thread_switch = False
	print("[Info] 多執行緒已全部終止!")
	
#main
def start(thread_num, path, path_drive):
	try:
		#初始化參數
		initializeParameter()
		#設定下載路徑
		global download_path
		download_path = path
		#設定遞迴上限，避免遞迴過多被擋
		sys.setrecursionlimit(1000000)
		#開始執行多執行緒
		print('[Info] 開始進行分割檔的下載...')
		starttime = time.time() #開始時間
		startThreading(thread_num, threads, doDownloadTs, [])
		#每5秒管控一次多執行緒，流量控制在下載速率為8
		ThreadingController(threads, 1.6, 5, doDownloadTs, [])
		#堵塞多執行緒結束
		joinThreading(thread_num, threads)
		print("[Info] 下載完成!")
		timeelapsed = time.time() - starttime #總共下載時間
		print('[Info] 共花費'+str(time.strftime('%H時%M分%S秒', time.localtime(timeelapsed))))
		if restart(thread_num, path, path_drive):
			return True
	except Exception as e:
		global thread_switch
		thread_switch = False
		print(e)

def restart(thread_num, path, path_drive):
	#初始化參數
	initializeParameter()
	#設定下載路徑
	global download_path
	download_path = path
	#查看是否有缺漏
	result = search_files.doSearch(ts_id, partition_total_size, path)
	if result:	
		try:
			#開始執行補下載
			print('[Info] 開始進行分割檔的補下載...')
			starttime = time.time() #開始時間
			startThreading(thread_num, threads, doReDownloadTs, result)
			#每5秒管控一次多執行緒，流量控制在下載速率為8
			ThreadingController(threads, 1.6, 5, doReDownloadTs, result)
			#堵塞多執行緒結束
			joinThreading(thread_num, threads)
			print("[Info] 補下載完成!")
			timeelapsed = time.time() - starttime #總共下載時間
			print('[Info] 共花費'+str(time.strftime('%H時%M分%S秒', time.localtime(timeelapsed))))
			if restart(thread_num, path, path_drive): return True
		except Exception as e:
			print(e)
			print("[Error] 補下載失敗!")
	else: #進行下一階段
		try:
			#nfo產生器
			file_name = gl.get_value('file_name')
			video_id = gl.get_value('video_id')
			output_path = nf.start(file_name, video_id)
			if output_path:
				#影片壓制
				if suppress_video.start(path, output_path):
					#轉存雲端
					if clone_drive.start(file_name, video_id, path_drive):
						return True
		except Exception as e:
			print(e)

#if __name__ == '__main__':		
#	main()		