import re
import os
import numpy as np
from utils import r_f,w_f,w_f_list,get_time_6,get_tmstp,cmp_float

def ma(file,ns):
    contents = r_f(file)
    info = {}
    times = []
    for content in contents:
        if re.match(r'^[0-9]{6}', content) is not None:
            line = content.split(' ')
            info[line[0]] = {'endpr':float(line[2]),'lowestpr':float(line[4])}
            times.append(line[0])
    for n in ns:
        for index in range(n-1,len(times),1):
            pr = 0
            for i in range(n):
                pr = pr + info[times[index-i]]['endpr']
            info[times[index]]['MA' + str(n)] = pr/n
    return info
result = []
def boll(file,n,id):
    contents = r_f(file)
    info = {}
    times = []
    for content in contents:
        if re.match(r'^[0-9]{6}', content) is not None:
            line = content.split(' ')
            info[line[0]] = {'endpr': float(line[2])}
            times.append(line[0])
    i=0
    try:
        while 1:
            if (info[list(info.keys())[i+1]]['endpr']/info[list(info.keys())[i]]['endpr']>1.11)|(info[list(info.keys())[i+1]]['endpr']/info[list(info.keys())[i]]['endpr']<0.89):
                return False
            i += 1
    except:
        pass
    i = n-1
    boll = []
    try:
        while 1:
            pr = []
            for index in range(n):
                pr.append(info[list(info.keys())[i-index]]['endpr'])
            info[list(info.keys())[i]]['boll_50'] = np.std(pr, ddof=1)
            boll.append(info[list(info.keys())[i]]['boll_50'])
            i += 1
    except:
        pass
    #print(boll)

    for rate in [1.7,1.6,1.5,1.4,1.3,1.2]:
        for index in range(len(boll)-1):
            if boll[index] / boll[index + 1] > rate:
                if boll[index] > boll[-1]:
                    if boll[-1]/boll[-2]<1.1:
                        if id not in result:
                            print(id)
                            result.append(id)
    #return info
    #print(list(info.keys())[n-1],info[list(info.keys())[n-1]])

def goldx(info,ns):
    times = list(info.keys())
    try:
        i = 0 #金叉判断条件
        for index in range(len(times)-1,-1,-1):
            if cmp_float(info[times[index]]['MA' + str(ns[0])],info[times[index]]['MA' + str(ns[1])]): #假定金叉后回踩MA12
                if cmp_float(info[times[index]]['MA' + str(ns[1])],info[times[index]]['lowestpr']):
                    i = 1 #时效内金叉且回踩MA12且最低价高于金叉点
            elif (get_tmstp(get_time_6()) - get_tmstp(times[index]) < 30*24*60*60)&(get_tmstp(get_time_6()) - get_tmstp(times[index]) >= 0*24*60*60)&(i == 1)&(cmp_float(info[times[index]]['lowestpr'],info[times[index]]['MA' + str(ns[0])])):
                info['goldw'] = times[index]
                return info
            else:
                return False
        return False
    except Exception as e:
        #print(repr(e))
        return False

def goldxx(info,ns,time):
    try:
        times = list(info.keys())
        for index in range(len(times) - 1, -1, -1):
            if time == times[index]:
                i = 0
                if len(times) > index + 5:
                    for index1 in range(index+5,index-2,-1):
                        if (cmp_float(info[times[index1]]['MA' + str(ns[0])],info[times[index1]]['MA' + str(ns[1])]))&(cmp_float(info[times[index1]]['MA' + str(ns[1])],info[times[index1]]['MA' + str(ns[2])])):
                            i = 1
                        elif i == 1:
                            return True
                        else:
                            return False
                else:
                    for index1 in range(len(times)-1,index-2,-1):
                        if (cmp_float(info[times[index1]]['MA' + str(ns[0])],info[times[index1]]['MA' + str(ns[1])]))&(cmp_float(info[times[index1]]['MA' + str(ns[1])],info[times[index1]]['MA' + str(ns[2])])):
                            i = 1
                        elif i == 1:
                            return True
                        else:
                            return False
                return False
    except Exception as e:
        print(repr(e))
        return False

# 设置数据所在文件夹
#path_dir = 'D:\\JDBDIR\\vipdoc\\sz\\lday\\'
path_dir = 'db/'
# 读取文件夹下的文件
listfile = os.listdir(path_dir)
uids = []
uids_1 = []
for fname in listfile:
    if re.search(r'[0-9]{6}',fname) is not None:
        uid = re.search(r'[0-9]{6}',fname).group()
        if uid not in uids:
            uids.append(uid)
    else:
        print(fname)

for uid in uids:
    boold = boll(path_dir + uid + '_daily', 50, uid)
    if boold == True:
        print(uid)
    #print(boold)
    '''maw = goldx(maw, [6, 12])
    if maw is not False:
        mad = ma(path_dir + uid + '_daily', [5,10,20])
        mad = goldxx(mad, [5,10,20], maw['goldw'])
        if mad:
            uids_1.append(uid)'''
'''olds = r_f('5.23-6.23.txt')
uids_2 = []
for uid in uids_1:
    if uid not in olds:
        uids_2.append(uid)
w_f_list('out.txt',uids_2)'''
print(result)