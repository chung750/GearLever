def _init():#初始化
	global _global_dict
	_global_dict = {}


def set_value(key,value):
	#""" 定義一個全域性變數 """
	_global_dict[key] = value
	

def get_value(key,defValue=None):
	#""" 獲得一個全域性變數,不存在則返回預設值 """
	try:
		return _global_dict[key]
	except KeyError:
		return defValue