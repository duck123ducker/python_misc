import time
from decimal import Decimal
def w_f( file_save , raw ):
	with open(file_save, "a", encoding='utf-8') as file:#存入新信息
		file.write(str(raw) + '\n')

def w_f_list( file_save , raws ):
	with open(file_save, "a", encoding='utf-8') as file:#存入新信息
		for raw in raws:
			file.write(str(raw) + '\n')

def r_f( file_read ):
	with open(file_read, "r", encoding='utf-8') as file:#读取信息
		contents = [line.rstrip() for line in file]
	return contents

def get_beijin_time():
	return time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(time.time() + 28800))

def get_time_6():
	return time.strftime('%y%m%d',time.gmtime(time.time() + 28800))

def get_tmstp(tm):
	return time.mktime(time.strptime(tm, '%y%m%d'))

def cmp_float(a,b):
	if Decimal(a)>Decimal(b):
		return True
	else:
		return False