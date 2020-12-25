from GearLever import gl_variable as gl
import subprocess
import shlex
#壓制
def start(input_path, output_path):
	try:
		file_name = gl.get_value('file_name')
		ts_id = gl.get_value('ts_id')
		if (len(file_name) > 70) : 
			file_name = file_name[:-(len(file_name)-70)] #避免檔名過長
		command = "ffmpeg -i "+ input_path+ts_id +".m3u8 -c copy '"+output_path+ file_name +".mp4'"
		process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		for line in process.stdout.readlines():
			print(line.decode('utf-8'), end='')
		return True
	except Exception as e:
		print(e)
		print("[Error] 壓制影片失敗!")
		return False
