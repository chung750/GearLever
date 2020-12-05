def _init():#初始化
	global _global_dict = {}
    '''
	global _global_url = "" #影片網址(input)
	global _global_file_path = "" #: 下載後的影片要儲存的google drive位置(input)
	global _global_thread_num = "" #多執行緒數量(input)
	global _global_video_id = "" #:影片番號	
	global _global_file_name = "" #: 影片儲存名稱
	global _global_url_m3u8 = "" #: m3u8檔url
	global _global_ts_id = "" #: 分割檔ID
	global _global_partition_total_size = 0 #: 分割檔總數量
	global _global_id_inits = "" #: 開頭檔ID 
	global _global_url_ts = "" #: ts下載檔url 
	global _global_url_inits = "" #: 開頭檔的url
	'''

def set_value(key,value):
    """ 定義一個全域性變數 """
    _global_dict[key] = value
	
	'''
    _global_url = value
	_global_url = value
	_global_file_path = value
	_global_thread_num = value
	_global_video_id = value	
	_global_file_name = value
	_global_url_m3u8 = value
	_global_ts_id = value
	_global_partition_total_size = value
	_global_id_inits = value
	_global_url_ts = value
	_global_url_inits = value
	'''

def get_value(key,defValue=None):
　　""" 獲得一個全域性變數,不存在則返回預設值 """
    try:
        return _global_dict[key]
    except KeyError:
        return defValue