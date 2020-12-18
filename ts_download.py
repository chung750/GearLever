from GearLever import gl_variable as gl
import urllib
import threading
#參數
url_ts = gl.get_value('url_ts') #下載網址
ts_id = gl.get_value('ts_id') #下載分割檔ID
partition_total_size = gl.get_value('partition_total_size') #總分割檔個數
thread_num = 6
#check_duration = 5 #檢查下載進度間隔
threads = [] #多執行續
thread_switch = True #執行續總開關
#record_download_num = [] #記錄每5秒的下載檔案數
qos_waiting_time = 2 #流量控制的預設等待時間
#global 參數
current_partition = 0 #紀錄目前下載第幾分割檔

##當下載完成後call下一個下載job
def callbackfunc(blocknum, blocksize, totalsize):
	try:
		percent = 100.0 * blocknum * blocksize / totalsize
		if percent > 100:
			doDownloadTs()
	except Exception as e:
		print(e)
			
##主要下載job
def doDownloadTs():
	try:
		#判斷多執行緒開關是否開啟
		if thread_switch == True:
			global current_partition
			download_partition = current_partition
			current_partition = current_partition + 1 
			#判斷欲下載的分割檔ID是否超過最後一個
			if(download_partition <= int(partition_total_size)):
				time.sleep(qos_waiting_time) #此暫停時間用於流量控管
				url_go = url_ts+ts_id+str(download_partition)+'.ts'
				urllib.request.urlretrieve(url_go,ts_id+str(download_partition)+'.ts',callbackfunc)
				print("---分割檔: "+str(download_partition)+" 已完成下載(線程:"+threading.current_thread().name+"/"+str(threading.active_count())+")---")
		else:
			print("[Info] 執行緒終止:"+threading.currentThread().name)
	except Exception as e:
		print(e)
		print("[Error] 下載分割檔"+download_partition+"出現錯誤!")
	
##建立多執行緒 
def doThreading(num, threads):
	try:
		for i in range(num):
			threads.append(threading.Thread(target = doDownloadTs))
			threads[i].start()
		print("[Info] 啟動多執行緒進行下載...")
	except Exception as e:
		print(e)
		print("[Error] 建立多執行緒失敗!")
		
#main
def main():
	try:
		#設定遞迴上限，避免遞迴過多被擋
		sys.setrecursionlimit(1000000)
		#開始執行多執行緒
		print('開始進行分割檔的下載!')
		doThreading(thread_num, threads)
		#監看下載進度(每5秒鐘)
		#checkDownload(check_duration)  
	except Exception as e:
		thread_switch = False
		print(e)
		
if __name__ == '__main__':		
	main()		