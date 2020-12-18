import os

#檢索path內所有檔案，確認所有分割檔
def search(ts_id, total_size, path):
	try:
		files = os.listdir(path)
		listd = []
		#將缺漏的存入listd[]
		for i in range(total_size):
			if not ts_id+str(i)+'.ts' in files:
				listd.append(i)
		#確認是否有多下載的
		if not len(files) == total_size+2:
			print("[Warning] 下載的分割檔有重複!")
		return listd
	except Exception as e:
		print(e)
		print("[Error] 搜尋檔案錯誤!")

def doSearch(ts_id, total_size, path):
	try:
		print("[Info] 開始查驗下載檔案....")
		#搜尋有無缺漏
		result = search(ts_id, total_size, path)
		print("[Info] 查驗完畢!") 
		if(len(result) == 0):
			print("[Info] "+str(total_size)+"個分割檔已完整下載") 
			return []
		else:
			print("[Info] 缺少以下分割檔:")
			for i in result:
				print("[Info] "+str(i))
			return result
	except Exception as e:
		print(e)
		print("[Error] 查驗下載檔案發生錯誤!")